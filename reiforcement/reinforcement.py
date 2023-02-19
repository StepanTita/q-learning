from constants import Action
import numpy as np

OBSERVATION_SPACE = 100
EPOCHS = 100


class AsyncEnv:
    def __init__(self, env):
        self.initial_env = env.clone()
        self.env = env.clone()

    def reset(self):
        self.env = self.initial_env.clone()
        return 0

    async def step(self, action):
        while True:
            yield await anext(self.env.run_async(action))


class Agent:
    def __init__(self, alpha, gamma, epsilon, epsilon_decay, env):
        self.actions = len(Action)

        self.q_table = np.zeros([OBSERVATION_SPACE, self.actions])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

        self.env = env

    # TODO: penalize path
    async def training(self, epochs):
        for e in range(1, epochs + 1):
            print('*' * 30, f'Starting epoch: {e}...', '*' * 30)
            state = self.env.reset()

            steps, penalties, reward, = 0, 0, 0
            result_bonus = 10

            actions = []

            done = False
            while not done:
                if np.random.uniform(0, 1) < self.epsilon:
                    action = np.random.randint(0, self.actions)  # Explore action space
                else:
                    action = np.argmax(self.q_table[state])  # Exploit learned values

                actions.append(Action(action))
                next_state, reward, done = await anext(self.env.step(Action(action)))
                if next_state > len(self.q_table):
                    print('----> Failed to find the way...')
                    break

                if reward < -2:
                    penalties += reward

                old_value = self.q_table[state, action]
                next_max = np.max(self.q_table[next_state])

                new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                self.q_table[state, action] = new_value

                state = next_state
                steps += 1

            print('#' * 30, f'Completed epoch: {e}...\nSteps: {steps}', '#' * 30)
            print('>>>', 'epsilon:', self.epsilon)
            print('>>>', 'actions:', actions)
            print('>>>', 'penalties:', penalties)

            self.epsilon -= self.epsilon_decay
            self.epsilon = max(self.epsilon, 0)
