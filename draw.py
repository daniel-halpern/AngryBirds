import pygame

def draw(screen, bird, slingshot, game):
    # Draw the background
    #screen.fill("aqua")
    bg_image = pygame.image.load('assets/angryBirdsBackground.jpg')
    bg_image = pygame.transform.scale(bg_image, game.size)
    screen.blit(bg_image, (0,0))

    # Draw the slingshot bands
    if bird.in_slingshot:
        band1_pos = (slingshot.pos[0] - 15, slingshot.pos[1] - 15)
        band2_pos = (slingshot.pos[0] + 25, slingshot.pos[1] - 10)
        pygame.draw.line(screen, "brown4", band1_pos, bird.pos, width = 20)
        pygame.draw.line(screen, "brown4", band2_pos, bird.pos, width = 20)

    # Draw the slingshot
    #pygame.draw.circle(screen, "blue", slingshot.pos, 50) # The slingshot
    slingshot_image = pygame.image.load('assets/Slingshot_Classic.png')
    newPos = (slingshot.pos[0] - 25, slingshot.pos[1] - 50)
    screen.blit(slingshot_image, newPos) 

    draw_blocks(screen, game)
    # If the level is "start", draw the target
    if game.level == 0:
        target_pos = (1000, 275)
        target_image = pygame.image.load('assets/target.png')
        screen.blit(target_image, target_pos)
        
    # Draw the bird
    bird_image = pygame.image.load('assets/Red.png')
    bird_size = (50, 50)  # Replace with the desired size
    bird_image = pygame.transform.scale(bird_image, bird_size)
    bird_image_pos = (bird.pos[0] - bird_image.get_width() // 2, bird.pos[1] - bird_image.get_height() // 2)
    screen.blit(bird_image, bird_image_pos)
    #pygame.draw.circle(screen, "red", bird.pos, 25)

    pygame.display.flip()

def draw_blocks(screen, game):
    for block in game.level_list[game.level].block_list:
        if block.type == "box":
            pygame.draw.polygon(screen, "brown", block.point_list)
