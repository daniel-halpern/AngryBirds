class Block: 
    def __init__(self, pos, type, movable):
        self.pos = pos # Position of center of mass
        self.type = type
        self.movable = movable
        self.width = pos[1][0] - pos[0][0]
        self.height = pos[1][1] - pos[0][1]