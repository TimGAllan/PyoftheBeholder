class Dungeon(object):
    def __init__(self,levels):
        self.levels = levels

class DungeonLevel(object):
    def __init__(self, Environment, WallsX, WallsY, Clipping, Adornments, Switches):
        self.Environment = Environment
        self.WallsX = WallsX
        self.WallsY = WallsY
        self.Clipping = Clipping
        self.Adornments = Adornments
        self.Switches = Switches


