import math
import numpy as np

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

def calculate_bird_position(slingshot, bird, game):
    # If the bird is in the slingshot, limit it to only moving in the circle
    if bird.in_slingshot:
        stretch = calculate_distance(slingshot.pos, bird.body.position)
        if calculate_distance(slingshot.pos, bird.body.position) > slingshot.max_stretch:
            theta = calculate_angle(slingshot.pos, bird.body.position)
            bird.body.position = [slingshot.max_stretch * math.cos(theta) + slingshot.pos[0], 
                    slingshot.max_stretch * math.sin(theta) + slingshot.pos[1]]
            stretch = slingshot.max_stretch
        return stretch

def check_target_collision(game, bird, space):
    if game.level_list[game.level].name == "target":
        target_pos = game.level_list[game.level].target_pos
        if (bird.body.position[1] > target_pos[1] + 70 and bird.body.position[1] < target_pos[1] + 300 and 
            bird.body.position[0] > target_pos[0] + 150 and bird.body.position[0] < target_pos[0] + 200):
            bird.body.velocity = (0, 0)
            space.gravity = (0, 0)

def begin(arbiter, space, data):
    # Check if the collision is between the bird and a block
    if arbiter.shapes[0].id == "bird" and arbiter.shapes[1].id == "block":
        bird_shape = arbiter.shapes[0]
        block_shape = arbiter.shapes[1]
        total_velocity = math.sqrt(bird_shape.body.velocity[0] ** 2 + bird_shape.body.velocity[1] ** 2)
        # May need to fine tune this / 3 number
        if total_velocity / 3 > arbiter.shapes[1].body.mass:
            space.remove(block_shape.body, block_shape)
    elif arbiter.shapes[0].id == "block" and arbiter.shapes[1].id == "block":
        total_impulse = math.sqrt(arbiter.total_impulse[0] ** 2 + arbiter.total_impulse[1] ** 2)
        if abs(total_impulse) > 2000:
            block_shape = arbiter.shapes[0]
            block_shape2 = arbiter.shapes[1]
            space.remove(block_shape.body, block_shape)
            space.remove(block_shape2.body, block_shape2)
    elif arbiter.shapes[1].id == "block" and arbiter.shapes[0].id == "ground":
        # May require fine tuning, however, I think this is a good enough algorithm
        total_velocity = math.sqrt(arbiter.shapes[1].body.velocity[0] ** 2 + arbiter.shapes[1].body.velocity[1] ** 2)
        if (abs(arbiter.shapes[1].body.angular_velocity) * total_velocity > 500
            or arbiter.shapes[1].body.angular_velocity > 2 or total_velocity > 400
            ):
            block_shape = arbiter.shapes[1]
            space.remove(block_shape.body, block_shape)
    return True 