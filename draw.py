import pygame

def draw(screen, bird, slingshot, game):
    screen.fill("aqua")
    pygame.draw.circle(screen, "blue", slingshot.pos, 50) # The slingshot
    pygame.draw.circle(screen, "red", bird.pos, 25) # The bird
    draw_blocks(screen, game)
    pygame.display.flip()


def draw_blocks(screen, game):
    for block in game.block_list:
        if block.type == "box":
            width = block.pos[1][0] - block.pos[0][0]
            height = block.pos[1][1] - block.pos[0][1]
            pygame.draw.rect(screen, "brown", pygame.Rect(block.pos[0][0], block.pos[0][1], width, height))