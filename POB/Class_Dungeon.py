class Dungeon(object):
    def __init__(self,levels,entryPos):
        self.levels = levels    #The levels of the dungeons in a list
        self.entryPos = entryPos #Dungeon Entry postion: (levelm XPos, Ypos, Direction)

class DungeonLevel(object):
    def __init__(self, environment, wallsX, wallsY, clipping, adornments, switches):
        self.environment = environment
        self.wallsX = wallsX
        self.wallsY = wallsY
        self.clipping = clipping
        self.adornments = adornments
        self.switches = switches


