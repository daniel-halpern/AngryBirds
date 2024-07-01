import pygame
from setup2 import *
from draw2 import *
from events2 import *
from helpers2 import *

def main():
    # Setup the game and the main game loop
    game, space, running, slingshot, bird = initialize_game()
    while running:
        game.dt = game.clock.tick(60)
        event_result = handle_events(game)
        if event_result == False:
            running = False
        elif event_result == 'reset':
            game.level_list = Level(game, "testing"), Level(game, "target"), Level(game, "basketball")
            game, space, slingshot, bird = reset_game(game, space)
            
        elif event_result == 'new bird':
            g
            ame, space, slingshot, bird = reset_game(game, space)

        # Handle mouse presses
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
        
        # Doesn't make much sense physics wise, however, this cancels out the gravitational
        # force ensuring the bird does not move while in the slingshot
        if bird.in_slingshot:
            force = bird.body.mass * space.gravity
            bird.body.apply_force_at_local_point(-force, (0, 0))

        check_target_collision(game, bird, space)

        # Draws everything
        draw(game, space, bird, slingshot)
        space.step(1/60.0)
    pygame.quit() 

main()
