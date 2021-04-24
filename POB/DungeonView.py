class DungeonViewPanel():

    def __init__(self, XPos, YPos, Width, Height, tile, Image):
        self.XPos = XPos
        self.YPos = YPos
        self.Width = Width
        self.Height = Height
        self.tile = tile
        self.image = Image


class DungeonView(object):
    # This class stores all the 

    # Right Panel 1
    LP1 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RP1 = DungeonViewPanel(0,0,100,100,"x","RP1.png")

    LW1 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    CW1 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RW1 = DungeonViewPanel(0,0,100,100,"x","RP1.png")

    LP2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RP2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")

    LW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    CW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")

    LLP3 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    LP3 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RP3 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RRP3 = DungeonViewPanel(0,0,100,100,"x","RP1.png")

    LLW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    LW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    CW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RRW2 = DungeonViewPanel(0,0,100,100,"x","RP1.png")

    LLP4 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    LP4 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RP4 = DungeonViewPanel(0,0,100,100,"x","RP1.png")
    RRP4 = DungeonViewPanel(0,0,100,100,"x","RP1.png")