import pygame
from slingshot import *
from bird import *
from game import *
from block import *

def initialize_game():
    pygame.init()
    game_size = [1400, 800]
    screen = pygame.display.set_mode(game_size)
    clock = pygame.time.Clock()
    running = True

    slingshot = Slingshot([200,600])
    bird = Bird(slingshot.pos, 10)
    game = Game(game_size)
    game.block_list = [Block([(50,50), (100,100)], "box", False), 
                       Block([(100,100), (200, 200)], "box", False)]

    return screen, clock, running, slingshot, bird, game

def reset_game():
    game_size = [1400, 800]
    slingshot = Slingshot([200,600])
    bird = Bird(slingshot.pos, 10)
    game = Game(game_size)
    game.block_list = [Block([(50,50), (100,100)], "box", False), 
                       Block([(100,100), (200, 200)], "box", False)]
    return slingshot, bird, game