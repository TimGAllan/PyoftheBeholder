import pygame as pg
import pandas as pd
from f_import_image import *

#Import Main Brick image

class DungeonTileset(object):
    def __init__(self):

        self.BG1 = import_image('Environments','EOB - BRICK - WALLSET - BACKGROUND.png',3)
        self.BG2 = import_image('Environments','EOB - BRICK - WALLSET - BACKGROUND.png',3,1)

        #creates a dataframe from the csv file and loads each of the images into the Dataframe.

        ImagesDF = pd.read_csv('Imagefiles.csv')
        ImagesDF['Image'] = None
        ImagesDF = ImagesDF.set_index(['File'])

        for i in ImagesDF.index:
             ImagesDF.loc[i,['Image']] = import_image('Environments',i,3)

        self.imagesDF = ImagesDF


        ##Load Dataframe with tile.csv data
        df = pd.read_csv('tiles.csv')
        df = df.set_index(['Environment','Wall','Panel'])
        df = df.astype({'Xpos': int, 'Ypos': int, 'Width': int, 'Height': int, 'Flip':bool, 'Blit_Xpos':int, 'Blit_Ypos':int})

        ##Create a new column for the Image
        df['Image'] = None
        df['Blit_Pos'] = None

        self.df = df

        ##Loop over the dataframe and create an image
        for i in df.index:
            locsize = (self.detail(i,'Xpos'),self.detail(i,'Ypos'),self.detail(i,'Width'),self.detail(i,'Height'))
            flip = self.detail(i,'Flip')
            print(self.detail(i,'File'))
            print(self.imagesDF)
            df.loc[i,['Image']] = sub_image(self.imagesDF.loc[self.detail(i,'File'),'Image'],locsize,3,flip)

    def detail(self,x,y):
        return self.df.loc[x,[y]].item()

    def image(self, environment, wall, panel):
        return self.df.loc[(environment,wall,panel),['Image']].item()

    def blitPos(self, environment, wall, panel, scalefactor=3):
        blitPos = (self.df.loc[(environment, wall, panel),['Blit_Xpos']].item()*scalefactor,self.df.loc[(environment, wall, panel),['Blit_Ypos']].item()*scalefactor) 
        return blitPos