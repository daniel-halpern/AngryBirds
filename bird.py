import math
import time

class Bird:
    def __init__(self, pos, mass):
        self.pos = pos
        self.inSlingshot = True
        self.velocity = [0, 0]
        self.mass = mass
        self.Fnetx = 0
        self.Fnety = 0
        self.accx = 0
        self.accy = -20000
        self.airTime = 0
        self.startTime = 0

    def calculateVelocity(self, energy, theta):
        velocity = math.sqrt(2 * energy)
        self.airTime = time.time() - self.startTime
        self.velocity[0] = -velocity * math.cos(theta)
        self.velocity[1] = velocity * math.sin(theta)
    
    def recalculateVelocity(self):
        self.velocity[0] = self.velocity[0] + self.accx * self.airTime
        self.velocity[1] = self.velocity[1] + self.accy * self.airTime
