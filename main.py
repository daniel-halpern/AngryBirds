import pygame
from setup import *
from bird import *
from game import *
from events import *
from draw import *
import time

def main():
    # Setup the game and the main game loop
    screen, clock, running, slingshot, bird, game = initialize_game()
    while running:
        game.dt = clock.tick(60)

        # Events
        event_result = handle_events(game)
        if event_result == False:
            running = False
        elif event_result == 'reset':
            slingshot, bird = reset_game(game.level)
            game.level_list = Level("testing"), Level("target"), Level("basketball")

        handle_mouse_events(bird, slingshot, game)
        check_collisions(bird, game)
        calculate_block_rotations(game)

        # Draws everything
        draw(screen, bird, slingshot, game)
    pygame.quit() 

main()