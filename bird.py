import math

class Bird:
    def __init__(self, pos, mass):
        self.pos = pos
        self.in_slingshot = True
        self.size = 25
        self.velocity = [0, 0]
        self.mass = mass
        self.Fnetx = 0
        self.Fnety = 0
        self.accx = 0
        self.accy = -.2

    def calculate_velocity(self, energy, theta):
        velocity = math.sqrt(2 * energy)
        self.velocity[0] = -velocity * math.cos(theta)
        self.velocity[1] = velocity * math.sin(theta)
    
    def recalculate_velocity(self, dt):
        self.velocity[0] = self.velocity[0] + self.accx * dt
        self.velocity[1] = self.velocity[1] + self.accy * dt
