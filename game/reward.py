import numpy as np


def dist(pA, pB, metric='euclidean'):
    if metric == 'euclidean':
        return np.linalg.norm(np.array(pA) -
                              np.array(pB))
    elif metric == 'manhattan':
        return np.abs(np.array(pA) - np.array(pB)).sum()


class Reward:
    def __init__(self, metric='manhattan'):
        self.initial_dist = np.inf
        self.agent = None
        self.target = None
        self.last_dist = np.inf
        self.metric = metric

    def set_start_goal(self, agent, target):
        self.agent = agent
        self.target = target
        self.initial_dist = dist(agent.rect.center, target.rect.center, self.metric)
        self.last_dist = self.initial_dist

    def calc_reward(self):
        right_dir_bonus = 0

        curr_dist = dist(self.agent.rect.center, self.target.rect.center, self.metric)
        if curr_dist < self.last_dist:
            right_dir_bonus += 10
        self.last_dist = curr_dist
        return -dist(self.agent.rect.center, self.target.rect.center, self.metric) / self.initial_dist + right_dir_bonus
