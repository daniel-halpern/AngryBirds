import pygame

def draw(screen, bird, slingshot, game):
    screen.fill("aqua")
    pygame.draw.circle(screen, "blue", slingshot.pos, 50) # The slingshot
    pygame.draw.circle(screen, "red", bird.pos, 25) # The bird
    draw_blocks(screen, game)
    pygame.display.flip()

def draw_blocks(screen, game):
    for block in game.level_list[game.level].block_list:
        if block.type == "box":
            pygame.draw.polygon(screen, "brown", block.point_list)
    