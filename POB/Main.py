##Import Standard Python libraries
import pygame as pg
import os
import sys

##Import POB files
from Dungeon            import *
from Class_DungeonView  import *
from Class_Player       import *
from UIConstants        import *


##Initialis Pygame
pg.init()
pg.font.init()

##The Pygame Window to the POB Icon and Label the Pygame Window "Py of th Beholder
programIcon = pg.image.load('Assets/eob_icon.png')
pg.display.set_icon(programIcon)
pg.display.set_caption('Py of the Beholder')


WIN = pg.display.set_mode((960, 600))

dungeonView = DungeonView(Dungeon.levels[0].Environment)
player = Player(7,13,'E')

def quitGame():
    pg.quit()
    sys.exit(0)

def redrawWindow():

    #  Render the background of the view window        
    BG = pg.transform.scale(pg.image.load(os.path.join('Assets/Environments', dungeonView.Environment, dungeonView.bg)), BG_WH)    
    WIN.blit(BG, ORIGIN_POS)
    
    # Render all the wall panels and environment
    for panel in dungeonView.panels:
        # Redender the Wall panel
        img = pg.transform.scale(pg.image.load(os.path.join(dungeonView.Walls_path, dungeonView.tiles[panel], dungeonView.panelImageFilenames[panel])), dungeonView.panelsWidthHeights[panel])
        WIN.blit(img, dungeonView.panelsPositions[panel])

        # Render the Adornment
        img = pg.transform.scale(pg.image.load(os.path.join(dungeonView.Adornments_path, dungeonView.Adornments_panels[panel], dungeonView.panelImageFilenames[panel])), dungeonView.panelsWidthHeights[panel])
        WIN.blit(img, dungeonView.panelsPositions[panel])          

    # render the UI
    UI = pg.transform.scale(pg.image.load(os.path.join('Assets', 'UI', player.D + '.png')), (WIDTH, HEIGHT))
    WIN.blit(UI, ORIGIN_POS)
    
    # display it in pygame
    pg.display.update()

def main():
    
    clock = pg.time.Clock()
    
    while True:
        clock.tick(FPS)
        dungeonView.updatePanels(player.position,Dungeon.levels[0].WallsX,Dungeon.levels[0].WallsY,Dungeon.levels[0].Adornments,Dungeon.levels[0].Clipping)
        redrawWindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitGame()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quitGame() 
                
                if pg.key.name(event.key) in 'qweasd':
                    player.move(Dungeon.levels[0].Clipping,pg.key.name(event.key))
                    
                if event.key == pg.K_SPACE:
                    player.clickSwitch(Dungeon.levels[0].Switches, Dungeon.levels[0].Adornments, Dungeon.levels[0].Clipping)

                                     
                    
main()
