import math

# Simple distance calculation function
def calculate_distance(pos1, pos2):
    deltaX = pos1[0] - pos2[0]
    deltaY = pos1[1] - pos2[1]
    return math.sqrt(deltaX ** 2 + deltaY ** 2)

# Calculates the angle of pos2 around pos1 in radians
def calculate_angle(pos1, pos2):
    deltaX = pos2[0] - pos1[0]
    deltaY = pos2[1] - pos1[1]
    return math.atan2(deltaY, deltaX)

# Calculates bird position *in slingshot*
def calculate_bird_position(slingshot, bird, game):
    if bird.in_slingshot:
        stretch = calculate_distance(slingshot.pos, bird.pos)
        if calculate_distance(slingshot.pos, bird.pos) > slingshot.max_stretch:
            theta = calculate_angle(slingshot.pos, bird.pos)
            bird.pos = [slingshot.max_stretch * math.cos(theta) + slingshot.pos[0], 
                    slingshot.max_stretch * math.sin(theta) + slingshot.pos[1]]
            stretch = slingshot.max_stretch
        return stretch
    else:
        bird.pos = [bird.pos[0] + (bird.velocity[0] * game.dt) / game.pixels_per_meter, 
                    bird.pos[1] - (bird.velocity[1] * game.dt) / game.pixels_per_meter,]
        # If the bird hits the floor, bounce
        if bird.pos[1] + bird.size > game.size[1]:
            bird.pos[1] = game.size[1] - bird.size
            bird.velocity[1] = -bird.velocity[1] * game.energy_lost_multiplier
            bird.velocity[0] = bird.velocity[0] * game.energy_lost_multiplier

def check_collisions(bird, game):
    for block in game.block_list:
        if block.type == "box":
            birdx, birdy = bird.pos[0], bird.pos[1]
            blockx1, blocky1 = block.pos[0][0], block.pos[0][1]
            blockx2, blocky2 = block.pos[1][0], block.pos[1][1]
            if birdx + bird.size >= blockx1 and birdx - bird.size <= blockx2:
                if birdy + bird.size >= blocky1 and birdy - bird.size <= blocky2:
                    closest_x = max(blockx1, min(birdx, blockx1 + block.width))
                    closest_y = max(blocky1, min(birdy, blocky1 + block.height))
                    dist_from_closest_x = abs(birdx - closest_x)
                    dist_from_closest_y = abs(birdy - closest_y)
                    if dist_from_closest_x >= dist_from_closest_y:
                        if bird.velocity[0] > 0:
                            bird.pos[0] = closest_x - bird.size
                        else: 
                            bird.pos[0] = closest_x + bird.size
                        bird.velocity = [-bird.velocity[0] * game.energy_lost_multiplier, bird.velocity[1]]
                    else:
                        if bird.velocity[1] > 0:
                            bird.pos[1] = closest_y + bird.size
                        else: 
                            bird.pos[1] = closest_y - bird.size
                        bird.velocity = [bird.velocity[0], -bird.velocity[1] * game.energy_lost_multiplier]
                        print(closest_x, closest_y)
                        return True
    return False