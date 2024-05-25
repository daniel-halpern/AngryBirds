import pygame
from helpers import *

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        return 'reset'

    return True

def handle_mouse_events(bird, slingshot, game):
    mouse_buttons_pressed = pygame.mouse.get_pressed()
    # Calculates where the bird should be drawn
    # In this case, the player is pulling back the slingshot
    if mouse_buttons_pressed[0] and bird.in_slingshot:
        mouse_pos = pygame.mouse.get_pos()
        bird.pos = mouse_pos
        slingshot.stretch = calculate_bird_position(slingshot, bird, game)
    # In this case, the player just let go the slingshot
    elif bird.in_slingshot and abs(slingshot.stretch) > 0:
        bird.in_slingshot = False
        bird.calculate_velocity(slingshot.spring_potential_energy(), 
                            calculate_angle(slingshot.pos, bird.pos))
    # In this case, the bird already has some initial velocity
    elif bird.velocity != [0, 0]: # Bird is launched
        bird.recalculate_velocity(game.dt)
        calculate_bird_position(slingshot, bird, game)