class Block: 
    def __init__(self, pos, angle, type, movable):
        self.pos = pos # Position of center of mass
        self.angle = 0
        self.type = type
        self.movable = movable
        self.width = pos[1][0] - pos[0][0]
        self.height = pos[1][1] - pos[0][1]