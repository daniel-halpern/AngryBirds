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
        self.accy = -.2
        self.mass = mass
        # Make an actual way of calculating it
        r = 100
        self.rotational_inertia = .5 * mass * r 

        # Calculate center of points
        #x_coords = [p[0] for p in point_list]
        #y_coords = [p[1] for p in point_list]
        #self.center = (sum(x_coords) / len(point_list), sum(y_coords) / len(point_list))
        self.center = self.calculate_block_center()

        # Rotate points
        self.point_list = self.rotate_points(self.angle)

    def rotate_points(self, angle):
        angle_rad = math.radians(angle)
        rotated_points = []
        for point in self.point_list:
            # Translate point back to origin
            point = (point[0] - self.center[0], point[1] - self.center[1])

            # Rotate point
            x_new = point[0] * math.cos(angle_rad) - point[1] * math.sin(angle_rad)
            y_new = point[0] * math.sin(angle_rad) + point[1] * math.cos(angle_rad)

            # Translate point back
            point = (x_new + self.center[0], y_new + self.center[1])
            rotated_points.append(point)
            self.point_list = rotated_points
        return rotated_points
    
    def calculate_block_center(self):
        # Calculate center of points
        x_coords = [p[0] for p in self.point_list]
        y_coords = [p[1] for p in self.point_list]
        center = (sum(x_coords) / len(self.point_list), sum(y_coords) / len(self.point_list))
        return center
