import pygame as pg
import sys
import os


class Game(object):
    """
    Main game class handling pygame window, clock, and rendering.

    Attributes:
        player: The player object
        dungeon_view: The dungeon view for rendering
        window: The pygame window surface
        clock: The pygame clock for frame timing
    """

    def __init__(self, player):
        self.player = player
        self.window_size = (960, 600)

    def dungeon_view_init(self, dungeon_view):
        self.dungeon_view = dungeon_view

    def launch(self):
        # Initialize Pygame
        pg.init()
        pg.font.init()

        # Set the Pygame window icon and title
        pg.display.set_icon(pg.image.load('assets/eob_icon.png'))
        pg.display.set_caption('Py of the Beholder')

        self.window = pg.display.set_mode(self.window_size)
        self.clock = pg.time.Clock()

        pg.mouse.set_visible(False)

        scale_factor = 2
        self.cursor_image = pg.image.load("assets/Environments/itemicn.png")

        cursor_size = (
            self.cursor_image.get_width() * scale_factor,
            self.cursor_image.get_height() * scale_factor
        )
        self.cursor_image = pg.transform.scale(self.cursor_image, cursor_size)

        self.cursor_image.set_colorkey((255, 0, 255), pg.RLEACCEL)
        self.cursor_image = self.cursor_image.convert()

    def quit(self):
        pg.quit()
        sys.exit(0)

    def tick(self):
        self.clock.tick(60)

    def redraw_window(self):
        # Render all the wall panels and environment
        for panel in self.dungeon_view.panels:
            tile_value = self.dungeon_view.tiles[panel]

            # Check if this is a door panel (has 'D' in name like CD1, LD2, RD3)
            is_door_panel = len(panel) >= 2 and 'D' in panel and panel != 'BG'

            # For door panels, always render the doorframe (type '2') first
            if is_door_panel and tile_value in '23':
                # Render the doorframe (open door appearance)
                img = self.dungeon_view.dungeon_tileset.image(
                    self.dungeon_view.environment,
                    '2',
                    panel
                )
                if img is not None:
                    self.window.blit(img, self.dungeon_view.panel_positions[panel])

                # If door is closed (type '3'), also render the door sprite on top
                if tile_value == '3':
                    img = self.dungeon_view.dungeon_tileset.image(
                        self.dungeon_view.environment,
                        '3',
                        panel
                    )
                    if img is not None:
                        # Use the blit position offset from CSV for door positioning
                        blit_offset = self.dungeon_view.dungeon_tileset.blit_pos(
                            self.dungeon_view.environment,
                            '3',
                            panel
                        )
                        if blit_offset is not None:
                            self.window.blit(img, blit_offset)

            # Render regular wall panels (skip empty 'X' and clipping values 0,1,4)
            elif tile_value not in 'X014':
                img = self.dungeon_view.dungeon_tileset.image(
                    self.dungeon_view.environment,
                    tile_value,
                    panel
                )
                if img is not None:
                    self.window.blit(img, self.dungeon_view.panel_positions[panel])

            # Render the Adornment
            adornment_name = self.dungeon_view.adornment_panels[panel]
            if adornment_name != 'x':
                img = self.dungeon_view.dungeon_tileset.image(
                    self.dungeon_view.environment,
                    adornment_name,
                    panel
                )
                if img is not None:
                    blit_pos = self.dungeon_view.dungeon_tileset.blit_pos(
                        self.dungeon_view.environment,
                        adornment_name,
                        panel
                    )
                    if blit_pos is not None:
                        self.window.blit(img, blit_pos)

        # Render the UI
        ui = pg.transform.scale(
            pg.image.load(os.path.join('assets', 'UI', self.player.direction + '.png')).convert(),
            self.window_size
        )
        ui.set_colorkey((255, 0, 255), pg.RLEACCEL)
        ui = ui.convert()
        self.window.blit(ui, (0, 0))

        self.window.blit(self.cursor_image, pg.mouse.get_pos(), (0, 0, 22, 32))

        # Display it in pygame
        pg.display.update()
