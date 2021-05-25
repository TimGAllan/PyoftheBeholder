##Import Standard Python libraries
import pygame as pg
import os
import sys

##Import POB files
from Dungeon            import *
from Class_DungeonView  import *
from Class_Player       import *
from Class_Game         import *
from UIConstants        import *

dungeonView = DungeonView(Dungeon.levels[0].Environment)
player = Player(7,13,'E')

game = Game(player,dungeonView)
game.Launch()


def main():
    
    while True:
        game.Tick()
        dungeonView.updatePanels(player.position,Dungeon.levels[0].WallsX,Dungeon.levels[0].WallsY,Dungeon.levels[0].Adornments,Dungeon.levels[0].Clipping)
        game.redrawWindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game.quit() 
                
                if pg.key.name(event.key) in 'qweasd':
                    player.move(Dungeon.levels[0].Clipping,pg.key.name(event.key))
                    
                if event.key == pg.K_SPACE:
                    player.clickSwitch(Dungeon.levels[0].Switches, Dungeon.levels[0].Adornments, Dungeon.levels[0].Clipping)

                                     
                    
main()
