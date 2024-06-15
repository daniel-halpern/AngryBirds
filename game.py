from block import *

class Game():
    def __init__(self, game_size, level):
        self.pixels_per_meter = 100
        self.size = game_size
        self.floor = 625
        self.energy_lost_multiplier = .5
        self.dt = 0
        self.block_list = []
        self.level = level
        self.level_list = [Level("testing"), Level("target"), Level("basketball")]
        self.level_change_timer = 0
        self.level_change_delay = 500


class Level():
    def __init__(self, name):
        self.name = name
        if name == "target":
            self.block_list = []
            self.target_pos = (1000, 275)

        elif name == "basketball":
            self.hoop_pos = (1000, 200)
            xpos = self.hoop_pos[0]
            ypos = self.hoop_pos[1]
            self.block_list = [
                # Backboard
                Block([self.hoop_pos, (xpos, ypos + 435), (xpos + 25, ypos + 435),
                    (xpos + 25, ypos)], 0, "box", False),
                # Hoop
                Block([(xpos - 130, ypos + 100), (xpos - 130, ypos + 200), 
                       (xpos - 120, ypos + 200), (xpos - 120, ypos + 100)], 160, "box", False),
                Block([(xpos - 15, ypos + 100), (xpos - 15, ypos + 200), 
                       (xpos - 25, ypos + 200), (xpos - 25, ypos + 100)], 20, "box", False)
             ]
        elif name == "testing":
            line1 = line_to_rectangle((100,100), (200, 200), 15)
            self.block_list = [
                Block([(500, 500), (600, 600), (600, 700)], 20, "box", False),
                Block(line1, 0, "box", False)

            ]
            
class Slingshot:
    def __init__(self, pos):
        self.pos = pos
        self.max_stretch = 50
        self.spring_constant = 12
        self.stretch = 0

    def spring_potential_energy(self):
        return .5 * self.spring_constant * (self.stretch ** 2) # PEs = 1/2kx^2

class Player:
    def __init__():
        return