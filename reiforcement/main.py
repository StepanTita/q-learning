import pygame

from config import read_config
from game.game import Game
from reiforcement.reinforcement import AsyncEnv, Agent

import asyncio

alpha = 0.1
gamma = 0.6
epsilon = 0.1
epsilon_decay = 0.0001

EPOCHS = 1000

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
    aenv = AsyncEnv(game)
    agent = Agent(alpha, gamma, epsilon, epsilon_decay, aenv)
    asyncio.run(agent.training(EPOCHS))


if __name__ == '__main__':
    main()
