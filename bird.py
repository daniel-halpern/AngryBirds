import math

class Bird:
    def __init__(self, pos, mass):
        self.pos = pos
        self.inSlingshot = True
        self.velocity = [0, 0]
        self.mass = mass

    def calculateVelocity(self, energy, theta):
        velocity = math.sqrt(2 * energy)
        self.velocity[0] = -velocity * math.cos(theta)
        self.velocity[1] = velocity * math.sin(theta)