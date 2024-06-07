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
        # If the bird hits the floor, bounce. May want to move to check_collisions()
        if bird.pos[1] + bird.size > game.floor:
            bird.pos[1] = game.floor - bird.size
            bird.velocity[1] = -bird.velocity[1] * game.energy_lost_multiplier
            bird.velocity[0] = bird.velocity[0] * game.energy_lost_multiplier

def check_collisions(bird, game):
    #for block in game.level_list[game.level].block_list2:
    polygons = game.level_list[game.level].block_list
    for polygon in polygons:
        # Calculate the closest point on the polygon to the bird
        closest_point = None
        closest_distance = None
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
                normal = normal / np.linalg.norm(normal)

                # Move the bird out of the polygon along the normal
                bird.pos = list(closest_point + normal * (bird.size))

                # Reflect the bird's velocity on the normal
                bird.velocity = list(np.array(bird.velocity) - 2 * np.dot(np.array(bird.velocity), normal) * normal * game.energy_lost_multiplier)
                bird.velocity[0], bird.velocity[1] = -bird.velocity[0], -bird.velocity[1]
                return True

    # No collision detected
    return False