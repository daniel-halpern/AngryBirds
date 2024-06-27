import pymunk

class Block:
    def __init__(self, position, size, mass, material_type, movable=True):
        self.position = position
        self.size = size
        self.mass = mass
        self.material_type = material_type
        self.movable = movable
        self.moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        if not self.movable:
            self.body_type = pymunk.Body.STATIC
        self.body.position = self.position
        self.set_material_properties(self.shape)

    def set_material_properties(self, shape):
        if self.material_type == 'wood':
            shape.friction = 0.6
            shape.elasticity = 0.2
        elif self.material_type == 'stone':
            shape.friction = 0.9
            shape.elasticity = 0.1
        elif self.material_type == 'ice':
            shape.friction = 0.1
            shape.elasticity = 0.5
        # Add more materials as needed

