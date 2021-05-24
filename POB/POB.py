##Import Standard Python libraries
import pygame as pg
import os
import sys

##Import POB files
import dungeon      as dg
import DungeonView  as dv
from UIConstants    import *
from Player         import *

##Initialis Pygame
pg.init()
pg.font.init()

##The Pygame Window to the POB Icon and Label the Pygame Window "Py of th Beholder
programIcon = pg.image.load('Assets/eob_icon.png')
pg.display.set_icon(programIcon)
pg.display.set_caption('Py of the Beholder')


WIN = pg.display.set_mode((WIDTH, HEIGHT))


Walls_path = os.path.join('Assets/Environments', dg.environment, 'Walls')
Adornments_path = os.path.join('Assets/Environments', dg.environment, 'Adornments')

dungeonView = dv.DungeonView()
player = Player(7,13,'E')


def clickSwitch():
    global panels
    global playerPosition
    x,y,d = player.position   
    
    if player.position in dg.switches.keys():
        x  = dg.switches[player.position][0][0]
        y  = dg.switches[player.position][0][1]
        if dg.Clipping[x][y] == 3:
            dg.Clipping[x][y] = 2
            dg.Adornments[dg.switches[player.position][1]]='LeverDown'
            
        else:
            dg.Clipping[x][y] = 3
            dg.Adornments[dg.switches[player.position][1]]='LeverUp'
  

def quitGame():
    pg.quit()
    sys.exit(0)

def redrawWindow():

    #Choose background art based on position
    if player.X % 2 == 0 and player.Y % 2 == 0 and player.D in 'NS':
        BG_ART = 'BG1.png'
    elif player.X % 2 == 1 and player.Y % 2 == 0 and player.D in 'NS':
        BG_ART = 'BG2.png'
    elif player.X % 2 == 0 and player.Y % 2 == 1 and player.D in 'NS':
        BG_ART = 'BG2.png'
    elif player.X % 2 == 1 and player.Y % 2 == 1 and player.D in 'NS':
        BG_ART = 'BG1.png'
        
    elif player.X % 2 == 0 and player.Y % 2 == 0 and player.D in 'EW':
        BG_ART = 'BG2.png'
    elif player.X % 2 == 1 and player.Y % 2 == 0 and player.D in 'EW':
        BG_ART = 'BG1.png'
    elif player.X % 2 == 0 and player.Y % 2 == 1 and player.D in 'EW':
        BG_ART = 'BG1.png'
    elif player.X % 2 == 1 and player.Y % 2 == 1 and player.D in 'EW':
        BG_ART = 'BG2.png'

    #  Render the background of the view window        
    BG = pg.transform.scale(pg.image.load(os.path.join('Assets/Environments', dg.environment, BG_ART)), BG_WH)    
    WIN.blit(BG, ORIGIN_POS)
    
    # Render all the wall panels and environment
    for panel in dungeonView.panels:
        # Redender the Wall panel
        img = pg.transform.scale(pg.image.load(os.path.join(Walls_path, dungeonView.tiles[panel], dungeonView.panelImageFilenames[panel])), dungeonView.panelsWidthHeights[panel])
        WIN.blit(img, dungeonView.panelsPositions[panel])

        # Render the Adornment
        img = pg.transform.scale(pg.image.load(os.path.join(Adornments_path, dungeonView.Adornments_panels[panel], dungeonView.panelImageFilenames[panel])), dungeonView.panelsWidthHeights[panel])
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
        dungeonView.updatePanels(player.position,dg.WallsX,dg.WallsY,dg.Adornments,dg.Clipping)
        redrawWindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitGame()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quitGame() 
                
                if pg.key.name(event.key) in 'qweasd':
                    player.move(dg.Clipping,pg.key.name(event.key))
                    
                if event.key == pg.K_SPACE:
                    clickSwitch()

                                     
                    
main()
