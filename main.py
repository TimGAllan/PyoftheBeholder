"""
Py of the Beholder - Main Entry Point
A Python remake of Eye of the Beholder (1991) using Pygame.

Controls:
    WASD - Move/Strafe
    Q/E  - Rotate left/right
    SPACE - Interact with switches
    F5   - Hot-reload tileset (after sprite_viewer changes)
    ESC  - Quit
"""
import pygame as pg
import importlib

from src.player import Player
from src.game import Game
import src.dungeon_tileset
import src.dungeon_view
from src.dungeon_view import DungeonView
from levels.sewer import dungeon


def main():
    # Initialize player and game
    player = Player(dungeon)
    game = Game(player)
    game.launch()

    # Initialize dungeon view
    dungeon_view = DungeonView(dungeon.levels[0].environment)
    game.dungeon_view_init(dungeon_view)

    # Initial panel update
    dungeon_view.update_panels(
        player.level_pos,
        dungeon.levels[0].walls_x,
        dungeon.levels[0].walls_y,
        dungeon.levels[0].adornments,
        dungeon.levels[0].clipping
    )

    # Main game loop
    while True:
        game.tick()
        game.redraw_window()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game.quit()

                if pg.key.name(event.key) in 'qweasd':
                    moved = player.move(dungeon.levels[0].clipping, pg.key.name(event.key))
                    if moved:
                        dungeon_view.update_panels(
                            player.level_pos,
                            dungeon.levels[0].walls_x,
                            dungeon.levels[0].walls_y,
                            dungeon.levels[0].adornments,
                            dungeon.levels[0].clipping
                        )
                        print(f"FPS: {int(game.clock.get_fps())}")

                if event.key == pg.K_SPACE:
                    player.click_switch(
                        dungeon.levels[0].switches,
                        dungeon.levels[0].adornments,
                        dungeon.levels[0].clipping
                    )
                    # Refresh view to show lever state change (no background swap)
                    dungeon_view.update_panels(
                        player.level_pos,
                        dungeon.levels[0].walls_x,
                        dungeon.levels[0].walls_y,
                        dungeon.levels[0].adornments,
                        dungeon.levels[0].clipping,
                        swap_background=False
                    )

                if event.key == pg.K_F5:
                    # Hot-reload tileset and view after sprite_viewer changes
                    print("Reloading tileset and view...")
                    importlib.reload(src.dungeon_tileset)
                    importlib.reload(src.dungeon_view)
                    dungeon_view = src.dungeon_view.DungeonView(dungeon.levels[0].environment)
                    game.dungeon_view_init(dungeon_view)
                    dungeon_view.update_panels(
                        player.level_pos,
                        dungeon.levels[0].walls_x,
                        dungeon.levels[0].walls_y,
                        dungeon.levels[0].adornments,
                        dungeon.levels[0].clipping
                    )
                    print("Reload complete!")


if __name__ == '__main__':
    main()
