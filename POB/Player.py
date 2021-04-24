class Player(object):
    
    def __init__(self, XPos, YPos, Direction):
        self.X = XPos
        self.Y = YPos
        self.D = Direction

    def position(self):
        return [self.X, self.Y, self.D]
