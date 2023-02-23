import pygame.sprite

from constants import Action, action_to_direction, GameStatus
from field.field import GameField
from game.drawer import Drawer
from game.eventer import Eventer
from game.reward import Reward
from levels.levels import read_level
from physics.physics import Physics
from sprites.enemy import Enemy
from sprites.finish import Finish
from sprites.floor import Floor
from sprites.player import Player
from sprites.spike import Spike
from sprites.wall import Wall

FPS = 120


def state_iteration(f):
    def wrapper(ref, *args):
        if not hasattr(ref, 'next_state'):
            ref.next_state = 1
        else:
            ref.next_state += 1
        return f(ref, *args)

    return wrapper


class Game:
    def __init__(self, base_path, config):
        self.base_path = base_path
        self.config = config

        self.drawer = Drawer(config['drawer'])
        self.eventer = Eventer()

        self.level = read_level(base_path, config['start_level'])

        self.physics = Physics(config['physics'], config['drawer']['screen'])

        self._init_level(config)

        self.running = False

    def _init_level(self, config):
        self.player = Player(config['sprites']['player'], config['physics']['gravity'])
        self.finish = Finish(self.level['finish'])

        self._prebuild_borders()

        self.spikes = pygame.sprite.Group()
        self.spikes.add([Spike(cfg) for cfg in self.level['spikes']])

        self.enemies = pygame.sprite.Group()
        self.enemies.add([Enemy(cfg, self.physics.g) for cfg in self.level['enemies']])

        self.game_objects = pygame.sprite.Group()
        self.game_objects.add(self.spikes)
        self.game_objects.add(self.walls)
        self.game_objects.add(self.floors)
        self.game_objects.add(self.enemies)
        self.game_objects.add(self.player)
        self.game_objects.add(self.finish)

        self.reward = Reward(metric='manhattan')
        self.reward.set_start_goal(self.player, self.finish)

    def _prebuild_borders(self):
        self.floors = pygame.sprite.Group()
        self.floors.add([Floor(cfg) for cfg in self.level['floors']])

        self.walls = pygame.sprite.Group()
        self.walls.add([Wall(cfg) for cfg in self.level['walls']])

        new_walls = []
        for floor in self.floors:
            new_walls.append(Wall({
                'x': floor.rect.left,
                'y': floor.rect.top + 1,
                'width': 1,
                'height': floor.rect.height - 2,
                'color': 'red',
            }))
            new_walls.append(Wall({
                'x': floor.rect.right,
                'y': floor.rect.top + 1,
                'width': 1,
                'height': floor.rect.height - 2,
                'color': 'red',
            }))

        new_floors = []
        for wall in self.walls:
            new_floors.append(Floor({
                'x': wall.rect.left + 1,
                'y': wall.rect.top,
                'width': wall.rect.width - 2,
                'height': 1,
                'color': 'red',
            }))
            new_floors.append(Floor({
                'x': wall.rect.left + 1,
                'y': wall.rect.bottom,
                'width': wall.rect.width - 2,
                'height': 1,
                'color': 'red',
            }))
        self.walls = [*self.walls, *new_walls]
        self.floors = [*self.floors, *new_floors]

    def _run_step(self, game_state):
        self.running = game_state['running']

        game_field = GameField(self.walls, self.floors, self.spikes)

        self.player.move(game_state['player_move'], game_field)

        if game_state['player_jump'] or self.player.is_jumping:
            self.player.jump(game_field)

        for spike in self.spikes:
            spike.rotate()

        if self.finish.rect.colliderect(self.player.rect):
            self.running = False
            return GameStatus.WIN

        if pygame.sprite.spritecollideany(self.player, self.spikes):
            self.running = False
            return GameStatus.LOST

        game_state = self.physics.apply([self.player, *self.enemies], game_field)
        if game_state['out_bounds']:
            self.running = False
            return GameStatus.LOST

        self.drawer.draw(self.game_objects)
        return GameStatus.PLAYING

    def _action_to_game_state(self, action):
        return {
            'running': self.running,
            'player_move': action_to_direction(action),
            'player_jump': action == Action.JUMP,
        }

    def run(self):
        self.running = True

        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            game_state = self.eventer.listen()

            self._run_step(game_state)

    @state_iteration
    def run_async(self, action):
        self.running = True

        clock = pygame.time.Clock()

        if self.running:
            clock.tick(FPS)
            game_state = self._action_to_game_state(action)

            game_status = self._run_step(game_state)

            reward = self.reward.calc_reward()

            return self.next_state, reward, game_status

    def clone(self):
        return Game(self.base_path, self.config)
