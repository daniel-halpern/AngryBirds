from helpers import *

class Block: 
    def __init__(self, point_list, angle, mass, type, movable):
        self.point_list = point_list
        self.angle = angle
        self.type = type
        self.movable = movable
        self.angular_momentum = 0
        self.angular_acceleration = 0
        self.velocity = [0, 0]
        self.accy = -.1
        self.mass = mass
        # Make an actual way of calculating it
        r = 100
        self.rotational_inertia = .5 * mass * r 
        self.center = self.calculate_block_center()
        self.collision_count = 0

        # Rotate points
        self.point_list = self.rotate_points(self.angle)

    def rotate_points(self, angle, center_point=None):
        if center_point is None:
            center_point = self.center

        angle_rad = math.radians(angle)
        rotated_points = []
        for point in self.point_list:
            # Translate point back to origin
            point = (point[0] - center_point[0], point[1] - center_point[1])

            # Rotate point
            x_new = point[0] * math.cos(angle_rad) - point[1] * math.sin(angle_rad)
            y_new = point[0] * math.sin(angle_rad) + point[1] * math.cos(angle_rad)

            # Translate point back
            point = (x_new + center_point[0], y_new + center_point[1])
            rotated_points.append(point)

        self.point_list = rotated_points
        return rotated_points
    
    def calculate_block_center(self):
        # Calculate center of points
        x_coords = [p[0] for p in self.point_list]
        y_coords = [p[1] for p in self.point_list]
        center = (sum(x_coords) / len(self.point_list), sum(y_coords) / len(self.point_list))
        return center
