import pygame as pg
import sys
import os

class Game(object):
    
    def __init__(self,player,dungeonview):
        self.player = player
        self.dungeonview = dungeonview
        self.WH = (960,600)

    def launch(self):
        ##Initialise Pygame
        pg.init()
        pg.font.init()

        ##The Pygame Window to the POB Icon and Label the Pygame Window "Py of th Beholder
        pg.display.set_icon(pg.image.load('Assets/eob_icon.png'))
        pg.display.set_caption('Py of the Beholder')

        self.window = pg.display.set_mode(self.WH)

        self.clock = pg.time.Clock()

    def quit(self):
        pg.quit()
        sys.exit(0)

    def tick(self):
        self.clock.tick(60)

    def redrawWindow(self):

        #  Render the background of the view window        
        BG = pg.transform.scale(pg.image.load(os.path.join('Assets/Environments', self.dungeonview.Environment, self.dungeonview.bg)), (528,360))    
        self.window.blit(BG, (0,0))
    
        # Render all the wall panels and environment
        for panel in self.dungeonview.panels:
            # Redender the Wall panel
            img = pg.transform.scale(pg.image.load(os.path.join(self.dungeonview.Walls_path, self.dungeonview.tiles[panel], self.dungeonview.panelImageFilenames[panel])), self.dungeonview.panelsWidthHeights[panel])
            self.window.blit(img, self.dungeonview.panelsPositions[panel])

            # Render the Adornment
            img = pg.transform.scale(pg.image.load(os.path.join(self.dungeonview.Adornments_path, self.dungeonview.Adornments_panels[panel], self.dungeonview.panelImageFilenames[panel])), self.dungeonview.panelsWidthHeights[panel])
            self.window.blit(img, self.dungeonview.panelsPositions[panel])          

        # render the UI
        UI = pg.transform.scale(pg.image.load(os.path.join('Assets', 'UI', self.player.D + '.png')), self.WH)
        self.window.blit(UI, (0,0))
    
        # display it in pygame
        pg.display.update()
