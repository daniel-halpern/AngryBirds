import pygame
from helpers import *

def handle_keyboard_events(game):
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        return 'reset'
    if keys[pygame.K_LEFT] and current_time - game.level_change_timer > game.level_change_delay:
        game.level = (game.level -1) % len(game.level_list)
        game.level_change_timer = current_time
        return 'reset'
    if keys[pygame.K_RIGHT] and current_time - game.level_change_timer > game.level_change_delay:
        game.level = (game.level + 1) % len(game.level_list)
        game.level_change_timer = current_time
        return 'reset'
    if keys[pygame.K_e]:
        return 'new bird'
    if keys[pygame.K_f]:
        return 'scroll'
    if keys[pygame.K_t]:
        return 'set bird launch'
    return True

def handle_mouse_events(game, bird, slingshot):
    mouse_buttons_pressed = pygame.mouse.get_pressed()
    # If the player is pulling back the slingshot
    if mouse_buttons_pressed[0] and bird.in_slingshot:
        mouse_pos = pygame.mouse.get_pos()
        bird.body.position = mouse_pos
        slingshot.stretch = calculate_bird_position(slingshot, bird, game)
    elif bird.in_slingshot and abs(slingshot.stretch) > 0:
        bird.in_slingshot = False
        bird.calculate_velocity(slingshot.spring_potential_energy(), 
                                calculate_angle(slingshot.pos, bird.body.position))