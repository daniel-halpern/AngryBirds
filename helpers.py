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

# Checks if the bird is hitting the target
def check_target_collision(game, bird, space):
    if game.level_list[game.level].name == "target":
        target_pos = game.level_list[game.level].target_pos
        if (bird.body.position[1] > target_pos[1] + 70 and bird.body.position[1] < target_pos[1] + 300 and 
            bird.body.position[0] > target_pos[0] + 150 and bird.body.position[0] < target_pos[0] + 200):
            bird.body.velocity = (0, 0)
            space.gravity = (0, 0)

# Deals with the collision destruction
def begin(arbiter, space, data):
    # Check if the collision is between the bird and a block
    if (arbiter.shapes[0].id == "bird" or arbiter.shapes[0].id == "pig") and (arbiter.shapes[1].id == "block" or arbiter.shapes[1].id == "pig"):
        first_shape = arbiter.shapes[0]
        second_shape = arbiter.shapes[1]
        total_velocity = math.sqrt(first_shape.body.velocity[0] ** 2 + second_shape.body.velocity[1] ** 2)
        # May need to fine tune this / 3 number
        if total_velocity / 3 > arbiter.shapes[1].body.mass:
            space.remove(second_shape.body, second_shape)
            if arbiter.shapes[0].id == "pig":
                space.remove(first_shape.body, first_shape)
    elif arbiter.shapes[0].id == "block" and arbiter.shapes[1].id == "block":
        total_impulse = math.sqrt(arbiter.total_impulse[0] ** 2 + arbiter.total_impulse[1] ** 2)
        if abs(total_impulse) > 2000:
            block_shape = arbiter.shapes[0]
            block_shape2 = arbiter.shapes[1]
            space.remove(block_shape.body, block_shape)
            space.remove(block_shape2.body, block_shape2)
    elif arbiter.shapes[0].id == "ground" and arbiter.shapes[1].id == "block":
        # May require fine tuning, however, I think this is a good enough algorithm
        total_velocity = math.sqrt(arbiter.shapes[1].body.velocity[0] ** 2 + arbiter.shapes[1].body.velocity[1] ** 2)
        if (abs(arbiter.shapes[1].body.angular_velocity) * total_velocity > 500
            or arbiter.shapes[1].body.angular_velocity > 2 or total_velocity > 400):
            block_shape = arbiter.shapes[1]
            space.remove(block_shape.body, block_shape)
    elif arbiter.shapes[0].id == "pig" and arbiter.shapes[1].id == "ground":
        # Similar algorithm to the block on ground collision, just different numbers
        total_velocity = math.sqrt(arbiter.shapes[0].body.velocity[0] ** 2 + arbiter.shapes[0].body.velocity[1] ** 2)
        if (abs(arbiter.shapes[0].body.angular_velocity) * total_velocity > 500
            or arbiter.shapes[0].body.angular_velocity > 2 or total_velocity > 400):
            pig_shape = arbiter.shapes[0]
            space.remove(pig_shape.body, pig_shape)
    return True 

def scroll(game, slingshot, bird):
    if bird.body.position[0] > (game.size[0] / 2):
        bird.passed_middle = True
    if bird.passed_middle:
        amount = bird.body.position[0] - (game.size[0] / 2)
        if amount < 0:
            return
        game.distance_scrolled += amount
        for pig in game.level_list[game.level].pig_list:
            pig.body.position = (pig.body.position[0] - amount, pig.body.position[1])
        for block in game.level_list[game.level].block_list:
            block.body.position = (block.body.position[0] - amount, block.body.position[1])
        bird.body.position = (bird.body.position[0] - amount, bird.body.position[1])
        slingshot.pos = (slingshot.pos[0] - amount, slingshot.pos[1])
        game.screen_pos -= amount
        if game.level_list[game.level].name == "target":
            game.level_list[game.level].target_pos = (game.level_list[game.level].target_pos[0] - amount, 
                                                      game.level_list[game.level].target_pos[1])

def undo_scroll(game, slingshot, bird):
    #for pig in game.pig_list:
    for pig in game.level_list[game.level].pig_list:
        pig.body.position = (pig.body.position[0] + game.distance_scrolled, pig.body.position[1])
    for block in game.level_list[game.level].block_list:
        block.body.position = (block.body.position[0] + game.distance_scrolled, block.body.position[1])
    bird.body.position = (bird.body.position[0] + game.distance_scrolled, bird.body.position[1])
    slingshot.pos = (slingshot.pos[0] + game.distance_scrolled, slingshot.pos[1])
    game.screen_pos += game.distance_scrolled
    if game.level_list[game.level].name == "target":
        game.level_list[game.level].target_pos = (game.level_list[game.level].target_pos[0] + game.distance_scrolled, 
                                                  game.level_list[game.level].target_pos[1])


def set_bird_launch(game, bird, slingshot):
    deltax = math.cos(math.radians(bird.pull_back_angle)) * bird.pull_back_distance
    deltay = math.sin(math.radians(bird.pull_back_angle)) * bird.pull_back_distance
    bird.body.position = (slingshot.pos[0] + deltax, slingshot.pos[1] - deltay)
    if True: # May want to make a better way of toggling release
        bird.in_slingshot = False
        energy = .5 * slingshot.spring_constant * (bird.pull_back_distance ** 2)
        velocity = math.sqrt(2 * energy)
        vx = -velocity * math.cos(math.radians(bird.pull_back_angle))
        vy = velocity * math.sin(math.radians(bird.pull_back_angle))
        bird.body.velocity = (vx, vy)

def check_for_no_movement(game, bird):
    if bird.in_slingshot:
        return False
    for block in game.level_list[game.level].block_list:
        if (abs(block.body.velocity[0]) > 1 or abs(block.body.velocity[1]) > 1) and not block.removed:
            return False
    for pig in game.level_list[game.level].pig_list:
        if (abs(pig.body.velocity[0]) > 1 or abs(pig.body.velocity[1]) > 1) and not pig.killed:
            return False
    # Play around with this value. It would be a good idea to raise it during training so it is quicker
    if abs(bird.body.velocity[0]) > 3 or abs(bird.body.velocity[1]) > 3:
        return False
    return True
