from block import *
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
        self.floor = 625
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

        elif name == "basketball":
            self.hoop_pos = (1000, 200)
            xpos = self.hoop_pos[0]
            ypos = self.hoop_pos[1]
            self.block_list = [
                # Backboard
                Block([self.hoop_pos, (xpos, ypos + 435), (xpos + 25, ypos + 435),
                    (xpos + 25, ypos)], 0, 500, "line", False),
                # Hoop
                Block([(xpos - 130, ypos + 100), (xpos - 130, ypos + 200), 
                       (xpos - 120, ypos + 200), (xpos - 120, ypos + 100)], 160, 100, "line", False),
                Block([(xpos - 15, ypos + 100), (xpos - 15, ypos + 200), 
                       (xpos - 25, ypos + 200), (xpos - 25, ypos + 100)], 20, 100, "line", False)
             ]
        elif name == "testing":
            line1 = line_to_rectangle((100,100), (200, 200), 15)
            line2 = line_to_rectangle((700,300), (300, 700), 15)
            top_line = line_to_rectangle((800, 400), (900, 400), 20)
            side_line = line_to_rectangle((820, 420), (820, 500), 20)
            side_line2 = line_to_rectangle((880, 420), (880, 500), 20)
            self.block_list = [
                Block(line2, 20, 500, "box", False),
                Block([(500, 500), (600, 600), (600, 700)], 20, 100, "box", True),
                Block(line1, 0, 100, "box", True),
                Block([(300, 300), (300, 400), (400, 400), (400, 300)], 0, 250, "box", True),
                Block(top_line, 0, 100, "box", True),
                Block(side_line, 0, 100, "box", True),
                Block(side_line2, 0, 100, "box", True)
            ]
            top_line = line_to_rectangle((800, 400), (1000, 400), 20)
            side_line = line_to_rectangle((810, 410), (810, game.floor), 20)
            side_line2 = line_to_rectangle((990, 410), (990, game.floor), 20)
            self.block_list = [
                #Block(top_line, 0, 100, "box", True),
                Block(side_line, 45, 100, "box", True),
                Block(side_line2, 0, 100, "box", True)
            ]
            #self.block_list = [Block(top_line, 90, 100, "box", True)]
            
class Slingshot:
    def __init__(self, pos):
        self.pos = pos
        self.max_stretch = 50
        self.spring_constant = 100
        self.stretch = 0

    def spring_potential_energy(self):
        return .5 * self.spring_constant * (self.stretch ** 2) # PEs = 1/2kx^2

class Player:
    def __init__():
        return