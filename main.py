import pygame
from setup import *
from draw import *
from events import *
from helpers import *

def main():
    # Setup the game and the main game loop
    pig_list = [Pig((900, 625 - 40)), Pig((1100, 625 - 40)), Pig((1000, 625 - 40 - 200 - 23))]
    game, space, running, slingshot, bird = initialize_game(pig_list)
    while running:
        game.dt = game.clock.tick(60)
        event_result = handle_keyboard_events(game)
        if event_result == False:
            running = False
        elif event_result == 'reset':
            game.level_list = Level(game, "testing"), Level(game, "target"), Level(game, "basketball")
            # May be able to streamline this process and not have to include two pig_lists if
            # I made a way to reset each pig to their original location
            game.pig_list = [Pig((900, 625 - 40)), Pig((1100, 625 - 40)), # Bottom layer
                             Pig((1000, 625 - 40 - 200 - 23))] # Top layer
            game, space, slingshot, bird = reset_game(game, space)
            game.screen_pos = -500
            game.distance_scrolled = 0
            game.score = 0
            
        elif event_result == 'new bird':
            game, space, slingshot, bird = reset_game(game, space)
            undo_scroll(game, slingshot, bird)
            game.distance_scrolled = 0
        elif event_result == 'set bird launch':
            if bird.in_slingshot:
                set_bird_launch(game, bird, slingshot)
                    
        handle_mouse_events(game, bird, slingshot)
        check_target_collision(game, bird, space)
        scroll(game, slingshot, bird)
        draw(game, space, bird, slingshot)

        # Returns the bird to the slingshot if it is coming to a stop
        if check_for_no_movement(game, bird): # Returns true if there is no movement
            undo_scroll(game, slingshot, bird)
            game, space, slingshot, bird = reset_game(game, space)
            game.distance_scrolled = 0
            bird.in_slingshot = True

        # Doesn't make much sense physics wise, however, this cancels out the gravitational
        # force ensuring the bird does not move while in the slingshot
        if bird.in_slingshot:
            force = bird.body.mass * space.gravity
            bird.body.apply_force_at_local_point(-force, (0, 0))

        space.step(1/60.0)
    pygame.quit() 

main()
