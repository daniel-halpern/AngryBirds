import pygame

def handle_events(game):
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