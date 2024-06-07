from block import *

class Game():
    def __init__(self, game_size, level):
        self.pixels_per_meter = 100
        self.size = game_size
        self.energy_lost_multiplier = .5
        self.dt = 0
        self.block_list = []
        self.level = level
        self.level_list = [Level("start"), Level("basketball")]
        self.level_change_timer = 0
        self.level_change_delay = 500


class Level():
    def __init__(self, name):
        if name == "start":
            self.block_list = [Block([(100,100), (200, 100), (200, 200), (100, 200)], 45, "box", False),
                                Block([(600,600), (600, 600), (700, 200), (700, 200)], 45, "box", False)]
        elif name == "basketball":
            self.block_list = [Block([(100,100), (200, 100), (200, 200), (100, 200)], 45, "box", False),
                                Block([(600,600), (700, 600), (700, 700), (600, 700)], 45, "box", False)]

class Player:
    def __init__():
        return