import math

class Bird:
    def __init__(self, pos, mass):
        self.pos = pos
        self.inSlingshot = True
        self.velocity = [0, 0]
        self.mass = mass

    # Calculates the velocity of the bird using KE = 1/2 mv^2
    def calculateVelocity(self, energy, theta):
        energyX = -energy * math.cos(theta)
        energyY = energy * math.sin(theta)
        self.velocity[0] = math.sqrt(abs(2 * energyX / self.mass))
        self.velocity[1] = math.sqrt(abs(2 * energyY / self.mass))
        if energyX == 0:
            self.velocity[0] = 0
        else:
            self.velocity[0] = self.velocity[0] * (energyX / abs(energyX))
        if energyY == 0:
            self.velocity[1] = 0
        else:
            self.velocity[1] = self.velocity[1] * (energyY / abs(energyY))