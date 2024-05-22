class Slingshot:
    def __init__(self, pos):
        self.pos = pos
        self.maxStretch = 50
        self.springConstant = 10
        self.stretch = 0

    def springPotentialEnergy(self):
        return .5 * self.springConstant * (self.stretch ** 2) # PEs = 1/2kx^2