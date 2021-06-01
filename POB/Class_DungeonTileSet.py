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

        ##Loop over the dataframe and create an image
        for i in df.index:
            locsize = (df.loc[i,['Xpos']],df.loc[i,['Ypos']],df.loc[i,['Width']],df.loc[i,['Height']])
            flip = df.loc[i,['Flip']].item()
            df.loc[i,['Image']] = sub_image(self.walls,locsize,3,flip)

        print(df)
