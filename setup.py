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
    return screen, clock, running, slingshot, bird, game

def reset_game():
    game_size = [1400, 800]
    slingshot = Slingshot([200,600])
    bird = Bird(slingshot.pos, 10)
    game = Game(game_size)
    return slingshot, bird, game