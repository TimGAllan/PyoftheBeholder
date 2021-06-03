import pygame as pg
import pandas as pd
from f_import_image import *

#Import Main Brick image

class DungeonTileset(object):
    def __init__(self):

        self.BG1 = import_image('Environments','EOB - BRICK - WALLSET - BACKGROUND.png',3)
        self.BG2 = import_image('Environments','EOB - BRICK - WALLSET - BACKGROUND.png',3,1)
        self.walls = import_image('Environments','EOB - BRICK - WALLSET - WALLS.png',3)

        ##Load Dataframe with tile.csv data
        df = pd.read_csv('tiles.csv')
        df = df.set_index(['Environment','Wall','Panel'])
        df = df.astype({'Xpos': int, 'Ypos': int, 'Width': int, 'Height': int, 'Flip':bool, 'Blit_Xpos':int, 'Blit_Ypos':int})

        ##Create a new column for the Image
        df['Image'] = None
        df['Blit_Pos'] = None

        ##Loop over the dataframe and create an image
        for i in df.index:
            locsize = (df.loc[i,['Xpos']].item(),df.loc[i,['Ypos']].item(),df.loc[i,['Width']].item(),df.loc[i,['Height']].item())
            #blitPos = (df.loc[i,['Blit_Xpos']].item(),df.loc[i,['Blit_Ypos']].item())
            flip = df.loc[i,['Flip']].item()
            df.loc[i,['Image']] = sub_image(self.walls,locsize,3,flip)

        self.df = df

    def image(self, environment, wall, panel):
        return self.df.loc[(environment,wall,panel),['Image']].item()

    def blitPos(self, environment, wall, panel, scalefactor=3):
        blitPos = (self.df.loc[(environment, wall, panel),['Blit_Xpos']].item()*scalefactor,self.df.loc[(environment, wall, panel),['Blit_Ypos']].item()*scalefactor) 
        return blitPos