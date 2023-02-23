import pygame

from config import read_config
from game.game import Game
from reiforcement.reinforcement import Environment, Agent

import asyncio

alpha = 0.25
gamma = 0.8
epsilon = 0.1
epsilon_decay = 0
backpropogate_decay = 0.9
fail_path_penalty = 10

EPOCHS = 10000

# For plotting metrics
all_epochs = []
all_penalties = []


def init_env(func):
    def wrapper():
        pygame.init()
        func()
        pygame.quit()

    return wrapper


@init_env
def main():
    config = read_config('../config.json')
    game = Game('..', config)
    aenv = Environment(game)
    agent = Agent(alpha, gamma, epsilon, epsilon_decay, backpropogate_decay, fail_path_penalty, aenv,
                  weights_path='../weights/1.json')
    asyncio.run(agent.training(EPOCHS))


if __name__ == '__main__':
    main()
