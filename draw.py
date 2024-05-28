import pygame

def draw(screen, bird, slingshot, game):
    screen.fill("aqua")
    pygame.draw.circle(screen, "blue", slingshot.pos, 50) # The slingshot
    pygame.draw.circle(screen, "red", bird.pos, 25) # The bird
    draw_blocks(screen, game)
    pygame.display.flip()


def draw_blocks(screen, game):
    #for block in game.block_list:
    for block in game.level_list[game.level].block_list:
        if block.type == "box":
            width = block.pos[1][0] - block.pos[0][0]
            height = block.pos[1][1] - block.pos[0][1]
            pygame.draw.rect(screen, "brown", pygame.Rect(block.pos[0][0], block.pos[0][1], width, height))
            #rect_surface = pygame.Surface((width, height))
            #rect_surface.fill((255, 0, 0))  # Fill the Surface with a red color
            #rotated_surface = pygame.transform.rotate(rect_surface, block.angle)
            #new_pos = (block.pos[0][0] - rotated_surface.get_width() // 2, block.pos[0][1] - rotated_surface.get_height() // 2)            
            #screen.blit(rotated_surface, new_pos)

