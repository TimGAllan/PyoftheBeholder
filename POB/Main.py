##Import POB files
from Dungeon            import *
from Class_DungeonView  import *
from Class_Player       import *
from Class_Game         import *


#player = Player(7,13,'E')
player = Player(dungeon)

game = Game(player)
game.launch()


dungeonView = DungeonView(dungeon.levels[0].environment)
game.dungeonviewInit(dungeonView)

def main():

    dungeonView.updatePanels(player.levelPos,dungeon.levels[0].wallsX,dungeon.levels[0].wallsY,dungeon.levels[0].adornments,dungeon.levels[0].clipping)

    while True:
        game.tick()
        #dungeonView.updatePanels(player.levelPos,dungeon.levels[0].wallsX,dungeon.levels[0].wallsY,dungeon.levels[0].adornments,dungeon.levels[0].clipping)
        game.redrawWindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game.quit() 
                
                if pg.key.name(event.key) in 'qweasd':
                    player.move(dungeon.levels[0].clipping,pg.key.name(event.key))
                    dungeonView.updatePanels(player.levelPos,dungeon.levels[0].wallsX,dungeon.levels[0].wallsY,dungeon.levels[0].adornments,dungeon.levels[0].clipping)
                    print(str(int(game.clock.get_fps())))
                    
                if event.key == pg.K_SPACE:
                    player.clickSwitch(dungeon.levels[0].switches, dungeon.levels[0].adornments, dungeon.levels[0].clipping)

                                     
                    
main()
