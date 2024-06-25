import pygame
from bird2 import *
from game2 import *
import random
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util
import math

def initialize_game():
    # Pygame setup
    pygame.init()
    running = True
    game = Game(0)
    game.screen = pygame.display.set_mode(game.size)
    game, space, slingshot, bird = reset_game(game)
    
    # Pymunk setup
    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    # Game objects setup

    slingshot = Slingshot([200,490])

    bird = Bird(slingshot.pos)
    space.add(bird.body, bird.shape)

    # Ground setup
    ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground_shape = pymunk.Segment(ground_body, (0, game.floor), (game.size[0], game.floor), 0.0)
    ground_shape.elasticity = 0.8
    ground_shape.friction = .8
    space.add(ground_body, ground_shape)
    space.damping = .6

    # Block setup
    #for block in game.level_list[game.level].block_list:
    #    space.add(block.body, block.shape)

    return game, space, running, slingshot, bird

def reset_game(game):
    # Pymunk setup
    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    # Game objects setup

    slingshot = Slingshot([200,490])

    bird = Bird(slingshot.pos)
    space.add(bird.body, bird.shape)

    # Ground setup
    ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ground_shape = pymunk.Segment(ground_body, (0, game.floor), (game.size[0], game.floor), 0.0)
    ground_shape.elasticity = 0.8
    ground_shape.friction = 15
    space.add(ground_body, ground_shape)
    space.damping = .6

    # Block setup
    for block in game.level_list[game.level].block_list:
        space.add(block.body, block.shape)

    return game, space, slingshot, bird