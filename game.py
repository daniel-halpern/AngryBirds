from block import *

class Game():
    def __init__(self, game_size):
        self.pixels_per_meter = 100
        self.size = game_size
        self.energy_lost_multiplier = .5
        self.dt = 0
        self.block_list = []
        self.block_list2 = []
        self.level = 1
        self.level_list = [Level("start"), Level("basketball")]


class Level():
    def __init__(self, name):
        if name == "start":
            self.block_list = [Block([(500,500), (700,700)], 0, "box", False), 
                       Block([(0,500), (50,700)], 0, "box", False), 
                       Block([(100,100), (200, 200)], 0, "box", False)]
            self.block_list2 = [Block2([(100,100), (200, 100), (200, 200), (100, 200)], 45, "box", False),
                                Block2([(600,600), (600, 600), (700, 200), (700, 200)], 45, "box", False)]
        elif name == "basketball":
            self.block_list = [Block([(1000, 400), (1025, 500)], 0, "box", False),
                               Block([(1125, 200), (1150, 500)], 0, "box", False)]
            self.block_list2 = [Block2([(100,100), (200, 100), (200, 200), (100, 200)], 45, "box", False),
                                Block2([(600,600), (700, 600), (700, 700), (600, 700)], 45, "box", False)]
