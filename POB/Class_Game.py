import pygame as pg
import sys
import os
from f_import_image import *

class Game(object):
    
    def __init__(self,player):
        self.player = player
        self.WH = (960,600)

    def dungeonviewInit(self,dungeonview):
        self.dungeonview = dungeonview

    def launch(self):
        ##Initialise Pygame
        pg.init()
        pg.font.init()

        ##The Pygame Window to the POB Icon and Label the Pygame Window "Py of th Beholder
        pg.display.set_icon(pg.image.load('Assets/eob_icon.png'))
        pg.display.set_caption('Py of the Beholder')

        self.window = pg.display.set_mode(self.WH)

        self.clock = pg.time.Clock()

        pg.mouse.set_visible(False)

        scaleFactor = 2
        self.CursorImage = pg.image.load("Assets/items/itemicn.png")

        self.CursorImageWH = (self.CursorImage.get_width()*scaleFactor,self.CursorImage.get_height()*scaleFactor)
        self.CursorImage = pg.transform.scale(self.CursorImage,self.CursorImageWH)
        
        self.CursorImage.set_colorkey((255,0,255), pg.RLEACCEL)
        self.CursorImage = self.CursorImage.convert()


    def quit(self):
        pg.quit()
        sys.exit(0)

    def tick(self):
        self.clock.tick(60)

    def redrawWindow(self):

        ##  Render the background of the view window        
        #self.window.blit(self.dungeonview.bg, (0,0))

        ## Render all the wall panels and environment
        for panel in self.dungeonview.panels:
            # Redender the Wall panel
            if self.dungeonview.tiles[panel] not in 'X01':
                #img = pg.transform.scale(pg.image.load(os.path.join(self.dungeonview.Walls_path, self.dungeonview.tiles[panel], self.dungeonview.panelImageFilenames[panel])), self.dungeonview.panelsWidthHeights[panel])
                #img.set_colorkey((255,0,255), pg.RLEACCEL)
                img = self.dungeonview.dungeonTiletset.image(self.dungeonview.Environment,self.dungeonview.tiles[panel],panel)
                self.window.blit(img, self.dungeonview.panelsPositions[panel])

            # Render the Adornment
            if self.dungeonview.Adornments_panels[panel] != 'x':
                img = pg.transform.scale(pg.image.load(os.path.join(self.dungeonview.Adornments_path, self.dungeonview.Adornments_panels[panel], self.dungeonview.panelImageFilenames[panel])), self.dungeonview.panelsWidthHeights[panel])
                img.set_colorkey((255,0,255), pg.RLEACCEL)
                img = img.convert()
                self.window.blit(img, self.dungeonview.panelsPositions[panel])          

               
        # render the UI
        UI = pg.transform.scale(pg.image.load(os.path.join('Assets', 'UI', self.player.D + '.png')).convert(), self.WH)
        UI.set_colorkey((255,0,255), pg.RLEACCEL)
        UI = UI.convert()
        self.window.blit(UI, (0,0))

        self.window.blit(self.CursorImage, pg.mouse.get_pos(), (0,0,22,32))
    
        # display it in pygame
        pg.display.update()
