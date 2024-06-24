import pygame
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import math

def draw(game, space, bird, slingshot):
    # Draw the background
    bg_image = pygame.image.load('assets/angryBirdsBackground.jpg')
    bg_image = pygame.transform.scale(bg_image, game.size)
    game.screen.blit(bg_image, (0,0))

    # Draw the slingshot bands
    if bird.in_slingshot:
        band1_pos = (slingshot.pos[0] - 15, slingshot.pos[1] - 15)
        band2_pos = (slingshot.pos[0] + 25, slingshot.pos[1] - 10)
        pygame.draw.line(game.screen, "brown4", band1_pos, bird.body.position, width = 20)
        pygame.draw.line(game.screen, "brown4", band2_pos, bird.body.position, width = 20)
    # Draw the actual slingshot
    slingshot_image = pygame.image.load('assets/Slingshot_Classic.png')
    newPos = (slingshot.pos[0] - 25, slingshot.pos[1] - 50)
    game.screen.blit(slingshot_image, newPos) 

    # Draw the bird
    pos = pymunk.pygame_util.to_pygame(bird.body.position, game.screen)
    angle_degrees = math.degrees(bird.body.angle)
    rotated_image = pygame.transform.rotate(bird.image, -angle_degrees)  # Pygame rotates counterclockwise, pymunk uses clockwise rotation
    new_pos = (pos[0] - rotated_image.get_width() / 2, pos[1] - rotated_image.get_height() / 2)
    game.screen.blit(rotated_image, new_pos)

    pygame.display.flip()