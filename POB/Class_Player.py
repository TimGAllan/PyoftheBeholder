class Player(object):
    
    def __init__(self, dungeon):
        self.L = dungeon.entryPos[0]
        self.X = dungeon.entryPos[1]
        self.Y = dungeon.entryPos[2]
        self.D = dungeon.entryPos[3]
        self.dungeonPos = (self.L, self.X, self.Y, self.D)
        self.levelPos = (self.X, self.Y, self.D)

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
            self.dungeonPos = (self.L, self.X, self.Y, self.D)
            self.levelPos = (self.X, self.Y, self.D)
            print(self.dungeonPos)

    def clickSwitch(self, switches, adornments, clipping):
    
        if self.dungeonPos in switches.keys():
            x  = switches[self.dungeonPos][0][0]
            y  = switches[self.dungeonPos][0][1]
            if clipping[x][y] == 3:
                clipping[x][y] = 2
                adornments[switches[self.dungeonPos][1]]='LeverDown'
            
            else:
                clipping[x][y] = 3
                adornments[switches[self.dungeonPos][1]]='LeverUp'
