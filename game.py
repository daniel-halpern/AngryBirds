class Game():
    def __init__(self, game_size):
        self.pixels_per_meter = 100
        self.size = game_size
        self.energy_lost_multiplier = .5
        self.dt = 0
        self.block_list = []
    
