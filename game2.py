from block2 import *
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


class Level():
    def __init__(self, game, name):
        self.name = name
        if name == "target":
            self.block_list = []
            self.target_pos = (1000, 275)
            self.block_list = [Block((500, 500), (100, 200), 100, 'wood')]
        elif name == "basketball":
            self.hoop_pos = (1000, 200)
            xpos = self.hoop_pos[0]
            ypos = self.hoop_pos[1]
            self.block_list = [Block((500, 500), (100, 200), 100, 'wood')]
        elif name == "testing":
            self.block_list = [Block((500, 500), (100, 200), 100, 'ice')]
            
class Slingshot:
    def __init__(self, pos):
        self.pos = pos
        self.max_stretch = 50
        self.spring_constant = 500
        self.stretch = 0

    def spring_potential_energy(self):
        return .5 * self.spring_constant * (self.stretch ** 2) # PEs = 1/2kx^2

class Player:
    def __init__():
        return