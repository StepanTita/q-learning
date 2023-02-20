import numpy as np


def dist(pA, pB):
    return np.linalg.norm(np.array(pA) -
                          np.array(pB))


class Reward:
    def __init__(self):
        self.initial_dist = np.inf
        self.agent = None
        self.target = None

    def set_start_goal(self, agent, target):
        self.agent = agent
        self.target = target
        self.initial_dist = dist(agent.rect.center, target.rect.center)

    def calc_reward(self):
        return -dist(self.agent.rect.center, self.target.rect.center) / self.initial_dist
