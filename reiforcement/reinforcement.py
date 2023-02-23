import json

from common.numpy_json_serialize import NumpyArrayEncoder
from constants import Action, GameStatus
import numpy as np

OBSERVATION_SPACE = 1000


# [0, 0.5]
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# transform to the range [-1, 1]
def log_scale(x, min_val=0, max_val=100):
    return (x - min_val) / (max_val - min_val) * 2 - 1


class Environment:
    def __init__(self, env):
        self.initial_env = env.clone()
        self.env = env.clone()

    def reset(self):
        self.env = self.initial_env.clone()
        return 0

    def step(self, action):
        return self.env.run_async(action)


class Agent:
    def __init__(self, alpha, gamma, epsilon, epsilon_decay, backpropogate_decay, fail_path_penalty, env,
                 save_every=100, weights_path=None):
        self.actions = len(Action)

        self.q_table = np.zeros([OBSERVATION_SPACE, self.actions])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.backpropogate_decay = backpropogate_decay
        self.fail_path_penalty = fail_path_penalty
        self.save_every = save_every

        self.env = env

        if weights_path is not None:
            with open(weights_path, 'r') as f:
                weights_object = json.load(f)
                self.q_table = np.asarray(weights_object['weights'])

    def _backpropogate_path_reward(self, path, reward):
        decay = self.backpropogate_decay
        for state, action in reversed(path):
            self.q_table[state, action] += reward * (log_scale(decay, max_val=1) + 1) / 2
            if reward < 0:
                decay *= self.backpropogate_decay

    def _calc_path_reward(self, min_steps, steps, result):
        """

        :param min_steps: min_steps to win previously
        :param steps: steps to reach the result this iteration
        :param result: the result of the iteration
        :return: reward|penalty
        """
        reward = 5
        if result == GameStatus.LOST:
            reward *= -1
            reward = reward + self.alpha * reward * np.exp(self.fail_path_penalty / steps)
        elif result == GameStatus.WIN:
            reward = 10 * reward + self.alpha * reward * np.exp(steps / min_steps)
        elif result == GameStatus.PLAYING:
            reward *= -1
        return self.gamma * reward

    async def training(self, epochs):
        steps_history = []
        actions_chosen = {
            Action.STAY: 0,
            Action.JUMP: 0,
            Action.MOVE_LEFT: 0,
            Action.MOVE_RIGHT: 0,
        }
        min_steps = np.inf
        for e in range(1, epochs + 1):
            print('*' * 30, f'Starting epoch: {e}...', '*' * 30)
            state = self.env.reset()

            steps, penalties, reward, = 0, 0, 0

            path = []

            result = None
            while result not in [GameStatus.WIN, GameStatus.LOST]:
                if np.random.uniform(0, 1) < self.epsilon:
                    action = np.random.randint(0, self.actions)  # Explore action space
                else:
                    action = np.argmax(self.q_table[state])  # Exploit learned values

                actions_chosen[Action(action)] += 1

                next_state, reward, result = self.env.step(Action(action))
                if next_state >= len(self.q_table):
                    print('----> Failed to find the way...')
                    break

                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value
                path.append((state, action))

                state = next_state
                steps += 1

            steps_history.append(steps)

            if result == GameStatus.WIN:
                min_steps = min(min_steps, steps)

            path_reward = self._calc_path_reward(min_steps, steps, result)
            self._backpropogate_path_reward(path, path_reward)

            print('>>>', f'Steps: {steps}')
            print('>>>', 'epsilon:', self.epsilon)
            print('>>>', 'path reward:', path_reward)
            print('>>>', 'min steps:', min_steps)
            print('#' * 30, f'Completed epoch: {e}...', '#' * 30)

            if len(steps_history) % 100 == 0:
                print('>>>', 'Average steps per 100 iterations', np.mean(steps_history))
                for k, v in actions_chosen.items():
                    print(k, v / sum(actions_chosen.values()))
                steps_history = []

            self.epsilon -= self.epsilon_decay
            self.epsilon = max(self.epsilon, 0)

            if e % self.save_every == 0:
                weights_object = json.dumps({
                    'level': self.env.initial_env.config['start_level'],
                    'weights': self.q_table,
                }, indent=4, cls=NumpyArrayEncoder)

                with open(
                        f'{self.env.initial_env.base_path}/weights/{self.env.initial_env.config["start_level"]}.json',
                        'w') as f:
                    f.write(weights_object)
