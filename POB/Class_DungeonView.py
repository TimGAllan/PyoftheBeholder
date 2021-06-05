import os
import pygame as pg
from Class_DungeonTileSet import *

class DungeonView(object):
    def __init__(self,Environment):
        self.Environment = Environment
        self.dungeonTiletset = DungeonTileset()
        self.Walls_path = os.path.join('Assets/Environments', self.Environment, 'Walls')
        self.Adornments_path = os.path.join('Assets/Environments', self.Environment, 'Adornments')

        self.panels =    ['BG','FP4','KP4','LP4','RP4','FF3','LF3','CF3','RF3','KF3','CD3','LD3','RD3','FP3','LP3','RP3','KP3','LF2','CF2','RF2','CD2','LD2','RD2','LP2','RP2','LF1','CF1','RF1','CD1','LD1','RD1','LP1','RP1']
        self.tiles={
            'BG':'BG1','FP4':'x','KP4':'x','LP4':'x','RP4':'x','FF3':'x','LF3':'x','CF3':'x','RF3':'x','KF3':'x','CD3':'x','LD3':'x','RD3':'x','FP3':'x','LP3':'x','RP3':'x','KP3':'x',
            'LF2':'x','CF2':'x','RF2':'x','CD2':'x','LD2':'x','RD2':'x','LP2':'x','RP2':'x','LF1':'x','CF1':'x','RF1':'x','CD1':'x','LD1':'x','RD1':'x','LP1':'x','RP1':'x'}
        self.Adornments_panels={
            'BG':'x','FP4':'x','KP4':'x','LP4':'x','RP4':'x','FF3':'x','LF3':'x','CF3':'x','RF3':'x','KF3':'x','CD3':'x','LD3':'x','RD3':'x','FP3':'x','LP3':'x','RP3':'x','KP3':'x',
            'LF2':'x','CF2':'x','RF2':'x','CD2':'x','LD2':'x','RD2':'x','LP2':'x','RP2':'x','LF1':'x','CF1':'x','RF1':'x','CD1':'x','LD1':'x','RD1':'x','LP1':'x','RP1':'x'}
        self.panelImageFilenames={
            'FP4':'FP4.png','KP4':'KP4.png','LP4':'LP4.png','RP4':'RP4.png','FF3': 'F3.png','LF3': 'F3.png','CF3': 'F3.png','RF3': 'F3.png','KF3': 'F3.png','CD3': 'D3.png','LD3':'LD3.png',
            'RD3':'RD3.png','FP3':'FP3.png','LP3':'LP3.png','RP3':'RP3.png','KP3':'KP3.png','LF2': 'F2.png','CF2': 'F2.png','RF2': 'F2.png','CD2': 'D2.png','LD2':'LD2.png','RD2':'RD2.png',
            'LP2':'LP2.png','RP2':'RP2.png','LF1': 'F1.png','CF1': 'F1.png','RF1': 'F1.png','CD1': 'D1.png','LD1':'LD1.png','RD1':'RD1.png','LP1':'LP1.png','RP1':'RP1.png'}
        self.panelsWidthHeights={
            'BG':(528,360),'FP4':( 72,120),'KP4':( 72,120),'LP4':( 16,120),'RP4':( 16,120),'FF3':(144,120),'LF3':(144,120),'CF3':(144,120),'RF3':(144,120),'KF3':(144,120),'CD3':(144,120),'LD3':(144,120),
            'RD3':(144,120),'FP3':( 48,144),'LP3':( 48,192),'RP3':( 48,192),'KP3':( 48,144),'LF2':(240,192),'CF2':(240,192),'RF2':(240,192),'CD2':(240,192),'LD2':(240,192),'RD2':(240,192),
            'LP2':( 72,288),'RP2':( 72,288),'LF1':(384,288),'CF1':(384,288),'RF1':(384,288),'CD1':(384,288),'LD1':(384,288),'RD1':(384,288),'LP1':( 72,360),'RP1':( 72,360)}
        self.panelsPositions={
            'BG':(0,0),'FP4':( 48, 72),'KP4':(408, 72),'LP4':(192, 72),'RP4':(320, 72),'FF3':(-96, 72),'LF3':( 48, 72),'CF3':(192, 72),'RF3':(336, 72),'KF3':(480, 72),'CD3':(192, 72),'LD3':( 48, 72),'RD3':(336, 72),
            'FP3':(  0, 72),'LP3':(144, 48),'RP3':(336, 48),'KP3':(480, 72),'LF2':(-96, 48),'CF2':(144, 48),'RF2':(384, 48),'CD2':(144, 48),'LD2':(-96, 48),'RD2':(384, 48),'LP2':( 72, 24),'RP2':(384, 24),
            'LF1':(-312,24),'CF1':( 72, 24),'RF1':(456, 24),'CD1':( 72, 24),'LD1':(-312,24),'RD1':(456, 24),'LP1':(  0,  0),'RP1':(456,  0),}
        
        self.panelsOffsets={
            'FP4':{'E':(3,-1),'W':(-3,2),'N':(-1,-3),'S':(2,3)},
            'KP4':{'E':(3,2),'W':(-3,-1),'N':(2,-3),'S':(-1,3)},
            'LP4':{'E':(3,0),'W':(-3,1),'N':(0,-3),'S':(1,3)},
            'RP4':{'E':(3,1),'W':(-3,0),'N':(1,-3),'S':(0,3)},
            'FF3':{'E':(3,-2),'W':(-2,2),'N':(-2,-2),'S':(2,3)},
            'LF3':{'E':(3,-1),'W':(-2,1),'N':(-1,-2),'S':(1,3)},
            'CF3':{'E':(3,0),'W':(-2,0),'N':(0,-2),'S':(0,3)},
            'RF3':{'E':(3,1),'W':(-2,-1),'N':(1,-2),'S':(-1,3)},
            'KF3':{'E':(3,2),'W':(-2,-2),'N':(2,-2),'S':(-2,3)},
            'CD3':{'E':(3,0),'W':(-3,0),'N':(0,-3),'S':(0,3)},
            'LD3':{'E':(3,-1),'W':(-3,1),'N':(-1,-3),'S':(1,3)},
            'RD3':{'E':(3,1),'W':(-3,-1),'N':(1,-3),'S':(-1,3)},
            'FP3':{'E':(2,-1),'W':(-2,2),'N':(-1,-2),'S':(2,2)},
            'LP3':{'E':(2,0),'W':(-2,1),'N':(0,-2),'S':(1,2)},
            'RP3':{'E':(2,1),'W':(-2,0),'N':(1,-2),'S':(0,2)},
            'KP3':{'E':(2,2),'W':(-2,-1),'N':(2,-2),'S':(-1,2)},
            'LF2':{'E':(2,-1),'W':(-1,1),'N':(-1,-1),'S':(1,2)},
            'CF2':{'E':(2,0),'W':(-1,0),'N':(0,-1),'S':(0,2)},
            'RF2':{'E':(2,1),'W':(-1,-1),'N':(1,-1),'S':(-1,2)},
            'CD2':{'E':(2,0),'W':(-2,0),'N':(0,-2),'S':(0,2)},
            'LD2':{'E':(2,-1),'W':(-2,1),'N':(-1,-2),'S':(1,2)},
            'RD2':{'E':(2,1),'W':(-2,-1),'N':(1,-2),'S':(-1,2)},
            'LP2':{'E':(1,0),'W':(-1,1),'N':(0,-1),'S':(1,1)},
            'RP2':{'E':(1,1),'W':(-1,0),'N':(1,-1),'S':(0,1)},
            'LF1':{'E':(1,-1),'W':(0,1),'N':(-1,0),'S':(1,1)},
            'CF1':{'E':(1,0),'W':(0,0),'N':(0,0),'S':(0,1)},
            'RF1':{'E':(1,1),'W':(0,-1),'N':(1,0),'S':(-1,1)},
            'CD1':{'E':(1,0),'W':(-1,0),'N':(0,-1),'S':(0,1)},
            'LD1':{'E':(1,-1),'W':(-1,1),'N':(-1,-1),'S':(1,1)},
            'RD1':{'E':(1,1),'W':(-1,-1),'N':(1,-1),'S':(-1,1)},
            'LP1':{'E':(0,0),'W':(0,1),'N':(0,0),'S':(1,0)},
            'RP1':{'E':(0,1),'W':(0,0),'N':(1,0),'S':(0,0)}
              }


    def updatePanels(self,playerPosition,WallsX,WallsY,Adornments,Clipping):
        x,y,d = playerPosition

        #Swap the the Background Image
        if self.tiles['BG'] == 'BG1':
            self.tiles['BG'] = 'BG2'
        else:
            self.tiles['BG'] = 'BG1'

        #if x % 2 == 0 and y % 2 == 0 and d in 'NS':
        #    self.bg = self.dungeonTiletset.BG1
        #elif x % 2 == 1 and y % 2 == 0 and d in 'NS':
        #    self.bg = self.dungeonTiletset.BG2
        #elif x % 2 == 0 and y % 2 == 1 and d in 'NS':
        #    self.bg = self.dungeonTiletset.BG2
        #elif x % 2 == 1 and y % 2 == 1 and d in 'NS':
        #    self.bg = self.dungeonTiletset.BG1
        
        #elif x % 2 == 0 and y % 2 == 0 and d in 'EW':
        #    self.bg = self.dungeonTiletset.BG2
        #elif x % 2 == 1 and y % 2 == 0 and d in 'EW':
        #    self.bg = self.dungeonTiletset.BG1
        #elif x % 2 == 0 and y % 2 == 1 and d in 'EW':
        #    self.bg = self.dungeonTiletset.BG1
        #elif x % 2 == 1 and y % 2 == 1 and d in 'EW':
        #    self.bg = self.dungeonTiletset.BG2
    
        if d in 'EW':
            a,b = 'P','F'
        else:
            a,b = 'F','P'
    
        # assign WallX panels
        for panel in filter(lambda x:x[1]==a, self.panels):
            self.tiles[panel]=WallsX[y+self.panelsOffsets[panel][d][1]][x+self.panelsOffsets[panel][d][0]]
        
            Adornment_Key = ('x',x+self.panelsOffsets[panel][d][0],y+self.panelsOffsets[panel][d][1])
            if Adornment_Key in Adornments.keys():
                self.Adornments_panels[panel] = Adornments[Adornment_Key]
            else:
                self.Adornments_panels[panel] = 'x'

        # assign WallY Panels
        for panel in filter(lambda x:x[1]==b, self.panels):
            self.tiles[panel]=WallsY[y+self.panelsOffsets[panel][d][1]][x+self.panelsOffsets[panel][d][0]]
        
            Adornment_Key = ('y',x+self.panelsOffsets[panel][d][0],y+self.panelsOffsets[panel][d][1])
            if Adornment_Key in Adornments.keys():
                self.Adornments_panels[panel] = Adornments[Adornment_Key]
            else:
                self.Adornments_panels[panel] = 'x'

        # Assign the door panels        
        for panel in filter(lambda x:x[1]=='D', self.panels):
            self.tiles[panel]=str(Clipping[y+self.panelsOffsets[panel][d][1]][x+self.panelsOffsets[panel][d][0]])
