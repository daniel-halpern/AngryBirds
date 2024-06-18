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

def check_collisions(bird, game):
    polygons = game.level_list[game.level].block_list
    for polygon in polygons:
        # Calculate the closest point on the polygon to the bird
        closest_point = None
        closest_distance = None
        # Loops through all the lines in that polygon
        for i in range(len(polygon.point_list)):
            p1 = np.array(polygon.point_list[i])
            p2 = np.array(polygon.point_list[(i+1) % len(polygon.point_list)])

            # Calculate the closest point on the edge to the bird
            edge = p2 - p1
            t = max(0, min(1, np.dot(np.array(bird.pos) - p1, edge) / np.dot(edge, edge)))
            closest = p1 + t * edge

            # Check if this point is closer than the previous closest point
            distance = np.linalg.norm(closest - np.array(bird.pos))
            if closest_distance is None or distance < closest_distance:
                closest_point = closest
                closest_distance = distance

            # If the bird is colliding with the polygon, adjust its position and velocity
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

                # Move the bird out of the polygon along the normal
                bird.pos = list(closest_point + normal * (bird.size))

                # Calculate the initial momentum of the bird
                initial_momentum = [bird.velocity[0] * bird.mass,
                                    bird.velocity[1] * bird.mass]
                # Calculates the lever length
                r = calculate_r(p1, p2, closest_point)

                # Reflect the bird's velocity on the normal
                bird.velocity = list(np.array(bird.velocity) - 2 * np.dot(np.array(bird.velocity), normal) * normal * game.energy_lost_multiplier)
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
                angle = 90 # Change to actually calculate something
                #polygon.angular_momentum = [r * block_momentum[0] * math.sin(angle),
                #                            r * block_momentum[1] * math.sin(angle)]
                # Calculate the magnitude of the block's momentum
                block_momentum_magnitude = math.sqrt(block_momentum[0]**2 + block_momentum[1]**2)

                # Calculate the angular momentum
                polygon.angular_momentum = r * block_momentum_magnitude
                print(initial_momentum, final_bird_momentum, block_momentum, polygon.angular_momentum)
                return True

    # No collision detected
    return False

def calculate_r(p1, p2, contact):
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

def calculate_block_rotations(game):
    polygons = game.level_list[game.level].block_list
    for polygon in polygons:
        if polygon.movable:
            angular_velocity = polygon.angular_momentum / polygon.rotational_inertia
            polygon.rotate_points(game.dt*angular_velocity/100)