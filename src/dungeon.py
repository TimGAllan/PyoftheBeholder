class Dungeon(object):
    def __init__(self, levels, entry_pos):
        self.levels = levels        # The levels of the dungeon in a list
        self.entry_pos = entry_pos  # Dungeon entry position: (level, x, y, direction)


class DungeonLevel(object):
    def __init__(self, environment, walls_x, walls_y, clipping, adornments, switches):
        self.environment = environment
        self.walls_x = walls_x
        self.walls_y = walls_y
        self.clipping = clipping
        self.adornments = adornments
        self.switches = switches
