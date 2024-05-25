class Slingshot:
    def __init__(self, pos):
        self.pos = pos
        self.max_stretch = 50
        self.spring_constant = 10
        self.stretch = 0

    def spring_potential_energy(self):
        return .5 * self.spring_constant * (self.stretch ** 2) # PEs = 1/2kx^2