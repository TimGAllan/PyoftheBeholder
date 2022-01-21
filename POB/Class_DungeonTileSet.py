import pygame as pg
import pandas as pd
from f_import_image import *

#Import Main Brick image

# DungeonTileset.BG1            = Background Image 1
# DungeonTileset.BG2            = Background Image 1
# DungeonTileset.WallsetImages  = Dataframe containg the Wallset images
# DungeonTileset.WallTiles      = Dataframe containg the WallTiles

class DungeonTileset(object):
    def __init__(self):

        self.BG1 = import_image('Environments','EOB - BRICK - WALLSET - BACKGROUND.png',3)
        self.BG2 = import_image('Environments','EOB - BRICK - WALLSET - BACKGROUND.png',3,1)

        #creates a dataframe from the csv file and loads each of the images into the Dataframe.

        WallsetImages = pd.read_csv('Imagefiles.csv')
        WallsetImages['Image'] = None
        WallsetImages = WallsetImages.set_index(['File'])

        for i in WallsetImages.index:
             WallsetImages.loc[i,['Image']] = import_image('Environments',i,3)

        self.WallsetImages = WallsetImages


        ##Load Dataframe with tile.csv data
        WallTiles = pd.read_csv('tiles.csv')
        WallTiles = WallTiles.set_index(['Environment','Wall','Panel'])
        WallTiles = WallTiles.astype({'Xpos': int, 'Ypos': int, 'Width': int, 'Height': int, 'Flip':bool, 'Blit_Xpos':int, 'Blit_Ypos':int})

        ##Create a new column for the Image
        WallTiles['Image'] = None
        WallTiles['Blit_Pos'] = None

        ##Loop over the dataframe and create an image
        for i in WallTiles.index:
            locsize = ( WallTiles.loc[i,['Xpos']].item()
                       ,WallTiles.loc[i,['Ypos']].item()
                       ,WallTiles.loc[i,['Width']].item()
                       ,WallTiles.loc[i,['Height']].item()
                       )
            flip = WallTiles.loc[i,['Flip']].item()
            WallTiles.loc[i,['Image']] = sub_image(WallsetImages.loc[WallTiles.loc[i,['File']].item(),['Image']].item(),locsize,3,flip)

        self.WallTiles = WallTiles


    def detail(self,x,y):
        return self.WallTiles.loc[x,[y]].item()

    def image(self, environment, wall, panel):
        return self.WallTiles.loc[(environment,wall,panel),['Image']].item()

    def blitPos(self, environment, wall, panel, scalefactor=3):
        blitPos = (self.WallTiles.loc[(environment, wall, panel),['Blit_Xpos']].item()*scalefactor,self.WallTiles.loc[(environment, wall, panel),['Blit_Ypos']].item()*scalefactor) 
        return blitPos