from block import *
from characters import *
import pygame
import pymunk
import pymunk.pygame_util
import math

class Game():
    def __init__(self, level):
        # Pygame related
        self.size = [1400, 800]
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        # Level related
        self.floor = 628
        self.block_list = []
        self.level = level
        self.level_list = [Level(self, "testing"), Level(self, "target"), Level(self, "basketball")]
        self.level_change_timer = 0
        self.level_change_delay = 500
        # Pymunk related
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.ticks_to_next_ball = 10
        self.lines = []
        self.pig_list = [Pig((100, 100))]


class Level():
    def __init__(self, game, name):
        self.name = name
        if name == "target":
            self.block_list = []
            self.target_pos = (1000, 275)
        elif name == "basketball":
            xpos = 500
            self.block_list = [Block((xpos + 400, 350), (10, 100), 100, 170, 'wood', False), # Rim
                               Block((xpos + 486, 350), (10, 100), 100, 10, 'wood', False), # Rim
                               Block((xpos + 500, game.floor / 2 + 100), (20, game.floor - 200), 100, 0, 'wood', False)] # Backboard
        elif name == "testing": # Desperately need to make a way of doing this that is simpler
            self.block_list = [
                            # Left bottom tower
                            Block((812, game.floor - (200 / 2)), (24, 200), 100, 0, 'wood', True),
                            Block((988, game.floor - (200 / 2)), (24, 200), 100, 0, 'wood', True),
                            Block((800 + (200 / 2), game.floor - (200) - 12), (200, 24), 100, 0, 'wood', True),
                            # Right bottom tower
                            Block((812 + 200, game.floor - (200 / 2)), (24, 200), 100, 0, 'wood', True),
                            Block((988 + 200, game.floor - (200 / 2)), (24, 200), 100, 0, 'wood', True),
                            Block((800 +200 + (200 / 2), game.floor - (200) - 12), (200, 24), 100, 0, 'wood', True),
                            # Top tower
                            Block((812 + 100, game.floor - (200 / 2) - 226), (24, 200), 100, 0, 'wood', True),
                            Block((988 + 100, game.floor - (200 / 2) - 226), (24, 200), 100, 0, 'wood', True),
                            Block((800 + 100 + (200 / 2), game.floor - (200) - 12 - 226), (200, 24), 100, 0, 'wood', True),
                               ]
            
class Slingshot:
    def __init__(self, pos):
        self.pos = pos
        self.max_stretch = 50
        self.spring_constant = 750
        self.stretch = 0

    def spring_potential_energy(self):
        return .5 * self.spring_constant * (self.stretch ** 2) # PEs = 1/2kx^2

class Player:
    def __init__():
        return