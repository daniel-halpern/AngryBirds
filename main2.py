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
            game, space, slingshot, bird = reset_game(game)
            game.level_list = Level(game, "testing"), Level(game, "target"), Level(game, "basketball")
        elif event_result == 'new bird':
            game, space, slingshot, bird = reset_game(game)

        # Handle mouse presses
        mouse_buttons_pressed = pygame.mouse.get_pressed()
        # If the player is pulling back the slingshot
        if mouse_buttons_pressed[0] and bird.in_slingshot:
            mouse_pos = pygame.mouse.get_pos()
            bird.body.position = mouse_pos
            slingshot.stretch = calculate_bird_position2(slingshot, bird, game)
        elif bird.in_slingshot and abs(slingshot.stretch) > 0:
            space.gravity = (0.0, 900.0)
            bird.in_slingshot = False
            bird.calculate_velocity(slingshot.spring_potential_energy(), 
                                    calculate_angle(slingshot.pos, bird.body.position))

        # Draws everything
        draw(game, space, bird, slingshot)
        space.step(1/60.0)
    pygame.quit() 

main()
