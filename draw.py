import pygame
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import math

def draw(game, space, bird, slingshot):
    # Draw the background
    #bg_image = pygame.image.load('assets/angryBirdsBackground.jpg')
    bg_image = pygame.image.load('assets/BackgroundTest.png')
    bg_image = pygame.transform.scale(bg_image, [game.size[0] * 3, game.size[1]])
    game.screen.blit(bg_image, (game.screen_pos, 0))

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

    # If the level is "target", draw the target
    if game.level_list[game.level].name == "target":
        target_image = pygame.image.load('assets/target.png')
        game.screen.blit(target_image, game.level_list[game.level].target_pos)

    # Draw the bird
    pos = pymunk.pygame_util.to_pygame(bird.body.position, game.screen)
    angle_degrees = math.degrees(bird.body.angle)
    rotated_image = pygame.transform.rotate(bird.image, -angle_degrees)  # Pygame rotates counterclockwise, pymunk uses clockwise rotation
    new_pos = (pos[0] - rotated_image.get_width() / 2 - 3, pos[1] - rotated_image.get_height() / 2 - 3)
    game.screen.blit(rotated_image, new_pos)

    # Draw the pig
    for pig in game.pig_list:
        if pig.shape in space.shapes:
            if pig.killed == False:
                pos = pymunk.pygame_util.to_pygame(pig.body.position, game.screen)
                angle_degrees = math.degrees(pig.body.angle)
                rotated_image = pygame.transform.rotate(pig.image, -angle_degrees)  # Pygame rotates counterclockwise, pymunk uses clockwise rotation
                new_pos = (pos[0] - rotated_image.get_width() / 2 - 3, pos[1] - rotated_image.get_height() / 2 - 3)
                game.screen.blit(rotated_image, new_pos)
        else:
            pig.killed = True

    draw_blocks(game, space)

    pygame.display.flip()

def draw_blocks(game, space):
    for block in game.level_list[game.level].block_list:
        if block.shape in space.shapes:
            pos = pymunk.pygame_util.to_pygame(block.shape.body.position, game.screen)
            angle_degrees = math.degrees(block.shape.body.angle)
            # Just practice using a match-case statement
            match block.material_type: 
                case "ice":
                    color = (173, 216, 230)  # Light blue
                case "stone":
                    color = (128, 128, 128)  # Gray
                case "wood":
                    color = (139, 69, 19)  # Brown
                case _:
                    color = (255, 255, 255)  # Default to white if material is unknown

            width, height = block.size[0], block.size[1]
            
            # Create a surface to draw the rotated block
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(surface, color, surface.get_rect())
            rotated_surface = pygame.transform.rotate(surface, -angle_degrees)
            
            # Calculate the new position after rotation
            new_pos = (pos[0] - rotated_surface.get_width() / 2, pos[1] - rotated_surface.get_height() / 2)
            game.screen.blit(rotated_surface, new_pos)
            
            # Quick debug view
            #draw_options = pymunk.pygame_util.DrawOptions(game.screen)
            #space.debug_draw(draw_options)
        else:
            block.removed = True