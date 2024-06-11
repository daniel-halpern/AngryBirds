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
        self.level_list = [Level("target"), Level("basketball")]
        self.level_change_timer = 0
        self.level_change_delay = 500


class Level():
    def __init__(self, name):
        self.name = name
        if name == "target":
            self.block_list = []
            self.target_pos = (0,0)
        elif name == "basketball":
            self.block_list = [
                # Backboard
                Block([(1000, 200), (1000, 635), (1025, 635), (1025, 200)], 0, "box", False),
                # Hoop
                Block([(870, 300), (870, 400), (880, 400), (880, 300)], 160, "box", False),
                Block([(985, 300), (985, 400), (975, 400), (975, 300)], 20, "box", False)
    ]
class Player:
    def __init__():
        return