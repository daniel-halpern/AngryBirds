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

# Calculates bird position *in slingshot*
def calculate_bird_position(slingshot, bird, game):
    # If the bird is in the slingshot, limit it to only moving in the circle
    if bird.in_slingshot:
        stretch = calculate_distance(slingshot.pos, bird.pos)
        if calculate_distance(slingshot.pos, bird.pos) > slingshot.max_stretch:
            theta = calculate_angle(slingshot.pos, bird.pos)
            bird.pos = [slingshot.max_stretch * math.cos(theta) + slingshot.pos[0], 
                    slingshot.max_stretch * math.sin(theta) + slingshot.pos[1]]
            stretch = slingshot.max_stretch
        return stretch
    # If the bird is not in the slingshot, calculate position using velocity and dt
    else:
        bird.pos = [bird.pos[0] + (bird.velocity[0] * game.dt) / game.pixels_per_meter, 
                    bird.pos[1] - (bird.velocity[1] * game.dt) / game.pixels_per_meter,]
        if game.level_list[game.level].name == "target":
            target_pos = game.level_list[game.level].target_pos
        # If the bird hits the floor, bounce. May want to move to check_collisions()
        if bird.pos[1] + bird.size > game.floor:
            bird.pos[1] = game.floor - bird.size
            bird.velocity[1] = -bird.velocity[1] * game.energy_lost_multiplier
            bird.velocity[0] = bird.velocity[0] * game.energy_lost_multiplier
        # If the bird hits the target
        elif (game.level_list[game.level].name == "target" and 
              bird.pos[1] > target_pos[1] + 70 and bird.pos[1] < target_pos[1] + 300 and 
              bird.pos[0] > target_pos[0] + 150 and bird.pos[0] < target_pos[0] + 200):
            bird.velocity = [0,0]
            bird.accy = 0

def check_bird_collisions(bird, game):
    blocks = game.level_list[game.level].block_list
    for block in blocks:
        # Calculate the closest point on the block to the bird
        closest_point = None
        closest_distance = None
        # Loops through all the lines in that block
        for i in range(len(block.point_list)):
            p1 = np.array(block.point_list[i])
            p2 = np.array(block.point_list[(i+1) % len(block.point_list)])

            # Calculate the closest point on the edge to the bird
            edge = p2 - p1
            t = max(0, min(1, np.dot(np.array(bird.pos) - p1, edge) / np.dot(edge, edge)))
            closest = p1 + t * edge

            # Check if this point is closer than the previous closest point
            distance = np.linalg.norm(closest - np.array(bird.pos))
            if closest_distance is None or distance < closest_distance:
                closest_point = closest
                closest_distance = distance

            # If the bird is colliding with the block, adjust its position and velocity
            if closest_distance <= bird.size:
                # Calculate the normal of the surface the bird is colliding with
                normal = (np.array(bird.pos) - closest_point)
                normal = normal / np.linalg.norm(normal) if np.linalg.norm(normal) != 0 else normal
                
                # Here to fix the edge case if the bird hits a completely vertical
                # or horizontal line that makes the normal = 0
                velocity = [0,0]
                if normal[0] == 0 and normal[1] == 0:
                    print("Something went terribly wrong...")
                    velocity = [-bird.velocity[0], -bird.velocity[1]]
                elif normal[0] == 0: # Collides with top / bottom
                    velocity = [bird.velocity[0], -bird.velocity[1]]
                elif normal[1] == 0: # Collides with left / right
                    velocity = [-bird.velocity[0], bird.velocity[1]]

                # Move the bird out of the block along the normal
                bird.pos = list(closest_point + normal * (bird.size))
                angle = math.atan2(normal[1], normal[0]) 
                for i in range(10):
                    t = max(0, min(1, np.dot(np.array(bird.pos) - p1, edge) / np.dot(edge, edge)))
                    closest = p1 + t * edge
                    distance = np.linalg.norm(closest - np.array(bird.pos))
                    if distance <= bird.size:
                        bird.pos[0] = bird.pos[0] + .5 * math.cos(angle)
                        bird.pos[1] = bird.pos[1] + .5 * math.sin(angle)
                    else:
                        break

                # Calculate the initial momentum of the bird
                initial_momentum = [bird.velocity[0] * bird.mass,
                                    bird.velocity[1] * bird.mass]
                # Calculates the lever length
                r = calculate_r(p1, p2, closest_point)

                # Reflect the bird's velocity on the normal
                bird.velocity = list(np.array(bird.velocity) - 2 * np.dot(np.array(bird.velocity), normal) * normal) #* game.energy_lost_multiplier
                bird.velocity[0] = -bird.velocity[0] * game.energy_lost_multiplier
                bird.velocity[1] = -bird.velocity[1] * game.energy_lost_multiplier

                # Fixes an edge case
                if velocity != [0,0]:
                    bird.velocity[0] = velocity[0] * game.energy_lost_multiplier
                    bird.velocity[1] = velocity[1] * game.energy_lost_multiplier

                # Finishes calculating angular momentum
                final_bird_momentum = [bird.velocity[0] * bird.mass,
                                       bird.velocity[1] * bird.mass]
                block_momentum = [initial_momentum[0] - final_bird_momentum[0], 
                                  initial_momentum[1] - final_bird_momentum[1]]
                block.velocity = [block_momentum[0] / block.mass, block_momentum[1] / block.mass]
                angle = 90 # Change to actually calculate something
                # Calculate the magnitude of the block's momentum
                block_momentum_magnitude = math.sqrt(block_momentum[0]**2 + block_momentum[1]**2)

                # Calculate the angular momentum
                block.angular_momentum = block.angular_momentum + r * block_momentum_magnitude
                return True

    # No collision detected
    return False

def calculate_r(p1, p2, contact):
    p1 = np.array(p1)
    p2 = np.array(p2)
    center = list((p1 + p2) / 2)
    r = math.sqrt((center[0] - contact[0]) ** 2 + (center[1] - contact[1]) ** 2)
    # If the contact point is above or to the left of the center, r is negative
    return r if contact[0] < center[0] or contact[1] < center[1] else -r

def line_to_rectangle(start, end, width):
    # Calculate the direction of the line
    direction = np.array(end, dtype=float) - np.array(start, dtype=float)
    direction /= np.linalg.norm(direction)

    # Calculate a vector perpendicular to the line
    perpendicular = np.array([-direction[1], direction[0]])

    # Calculate the four corners of the rectangle
    half_width = width / 2
    p1 = start - half_width * perpendicular
    p2 = start + half_width * perpendicular
    p3 = end + half_width * perpendicular
    p4 = end - half_width * perpendicular

    return [tuple(p1), tuple(p2), tuple(p3), tuple(p4)]

def handle_block_movement(game, bird):
    blocks = game.level_list[game.level].block_list
    for block in blocks:
        if block.movable:
            # Add some code here to calculate block horizontal velocity
            block.velocity[1] = block.velocity[1] + block.accy * game.dt
            block.point_list = calculate_block_pos(block, game)
            block.center = block.calculate_block_center()
            angular_velocity = block.angular_momentum / block.rotational_inertia
            block.rotate_points(game.dt*angular_velocity/100)
            block.angle += round(math.degrees(game.dt*angular_velocity/100))
            # Check for collisions between blocks here
            for other_polygon in blocks:
                if block != other_polygon and check_block_collisions(block, other_polygon):
                    handle_block_collision(block, other_polygon, game, bird)
                    reverse_block_pos(block, other_polygon, game)
            # Check for collision between the block and the floor here
            for point in block.point_list:
                if point[1] > game.floor:
                    handle_floor_collision(block, game, point)
                    break

def handle_floor_collision(block, game, contact):
    pointy = contact[1]
    difference = pointy - game.floor
    new_point_list = []
    furthest_distance = 0
    furthest_point_along_x = contact
    for point in block.point_list:
        new_point_list.append((point[0], point[1] - difference - 1))
        if abs(point[0] - contact[0]) > furthest_distance:
            furthest_point_along_x = point
            furthest_distance = abs(point[0] - contact[0])

    block.point_list = new_point_list
    block.velocity[0] *= game.energy_lost_multiplier
    block.velocity[1] = -block.velocity[1] * game.energy_lost_multiplier

    # Calculate the change in angular momentum
    r = calculate_r(contact, furthest_point_along_x, contact)
    change_in_angular_momentum = r * block.mass * (math.sin(math.radians((block.angle) % 360)) % math.pi)
    print((math.sin(math.radians((90 + block.angle) % 360)) % math.pi), r, change_in_angular_momentum, block.angular_momentum)
    block.angular_momentum = block.angular_momentum + change_in_angular_momentum
    block.collision_count += 1

def handle_block_collision(block1, block2, game, bird):
    initial_momentum = [bird.velocity[0] * bird.mass + block1.velocity[0] * block1.mass,
                        bird.velocity[1] * bird.mass + block1.velocity[1] * block1.mass]
    final_bird_momentum = [bird.velocity[0] * bird.mass,
                        bird.velocity[1] * bird.mass]
    #final_block_momentum = 
    #block1.velocity = [0, 0]
    #block1.accy = 0
    #block2.velocity = [0, 0]
    #block2.accy = 0
    return

def check_block_collisions(block1, block2):
    # Get the axes to test against
    axes = get_axes(block1) + get_axes(block2)
    # Check each axis for overlap
    for axis in axes:
        projection1 = project(block1, axis)
        projection2 = project(block2, axis)
        if not overlap(projection1, projection2):
            # If there's no overlap on this axis, the blocks are not colliding
            return False

    # If we've checked all axes and found overlap on all of them, the blocks are colliding
    return True

def get_axes(block):
    # Returns the normal of each edge of the block
    axes = []
    for i in range(len(block.point_list)):
        point1 = np.array(block.point_list[i])
        point2 = np.array(block.point_list[i - 1])
        edge = point1 - point2
        normal = np.array([-edge[1], edge[0]])
        axes.append(normal / np.linalg.norm(normal))  # Normalize the vector
    return axes

def project(block, axis):
    # Projects the block onto the axis
    dots = [np.dot(point, axis) for point in block.point_list]
    return [min(dots), max(dots)]

def overlap(projection1, projection2):
    # Checks if two projections overlap
    return not (projection1[1] < projection2[0] or projection2[1] < projection1[0])

def calculate_block_pos(block, game):
    new_point_list = []
    for point in block.point_list:
        new_point = [point[0] + (block.velocity[0] * game.dt) / game.pixels_per_meter,
                 point[1] - (block.velocity[1] * game.dt) / game.pixels_per_meter]
        new_point_list.append(new_point)
    return new_point_list

def reverse_block_pos(block, other_polygon, game):
    while check_block_collisions(block, other_polygon):
        new_point_list = []
        for point in block.point_list:
            new_point = [point[0] - (block.velocity[0] * game.dt * .1) / game.pixels_per_meter,
                    point[1] + (block.velocity[1] * game.dt * .1) / game.pixels_per_meter]
            new_point_list.append(new_point)
        block.point_list = new_point_list