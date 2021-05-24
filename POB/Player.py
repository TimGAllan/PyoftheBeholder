class Player(object):
    
    def __init__(self, XPos, YPos, Direction):
        self.X = XPos
        self.Y = YPos
        self.D = Direction
        self.position = (XPos, YPos, Direction)

    def move(self,clipping,KeyPress):

        Moves = {
            'w':{'N':[0,-1,'N'],'S':[0,+1,'S'],'E':[+1,0,'E'],'W':[-1,0,'W']},
            's':{'N':[0,+1,'N'],'S':[0,-1,'S'],'E':[-1,0,'E'],'W':[+1,0,'W']},
            'a':{'N':[-1,0,'N'],'S':[+1,0,'S'],'E':[0,-1,'E'],'W':[0,+1,'W']},
            'd':{'N':[+1,0,'N'],'S':[-1,0,'S'],'E':[0,+1,'E'],'W':[0,-1,'W']},
            'q':{'N':[0,0,'W'],'S':[0,0,'E'],'E':[0,0,'N'],'W':[0,0,'S']},
            'e':{'N':[0,0,'E'],'S':[0,0,'W'],'E':[0,0,'S'],'W':[0,0,'N']}
            }

        if clipping[self.Y+Moves[KeyPress][self.D][1]][self.X + Moves[KeyPress][self.D][0]] in [1,3]:
            print("You can't go that way")
        else:
            self.X += Moves[KeyPress][self.D][0]
            self.Y += Moves[KeyPress][self.D][1]
            self.D =  Moves[KeyPress][self.D][2]
            self.position = (self.X, self.Y, self.D)
            print(self.position)
