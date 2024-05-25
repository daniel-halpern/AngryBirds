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
        if bird.pos[1] > game.size[1]:
            bird.pos[1] = game.size[1]
            bird.velocity[1] = -bird.velocity[1] * game.energy_lost_multiplier
            bird.velocity[0] = bird.velocity[0] * game.energy_lost_multiplier

def check_collisions(bird, game):
    for block in game.block_list:
        if block.type == "line":
            if bird.pos[0] >= block.pos[0][0] and bird.pos[0] <= block.pos[1][0]:
                if bird.pos[1] >= block.pos[0][1] - bird.size and bird.pos[1] <= block.pos[0][1]:
                    return True
        elif block.type == "box":
            width = block.pos[1][0] - block.pos[0][0]
            height = block.pos[1][1] - block.pos[0][1]
            if bird.pos[0] >= block.pos[0][0] and bird.pos[0] <= block.pos[0][0] + width:
                if bird.pos[1] >= block.pos[1][0] - bird.size and bird.pos[1] <= block.pos[1][0] + height:
                    return True
    return False