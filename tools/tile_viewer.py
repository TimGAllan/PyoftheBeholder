"""
Tile Viewer Tool

Interactive pygame-based tool to browse and inspect tile renderings from data/tiles.csv.
Displays tile images along with their metadata values.

Controls:
    A/D             - Previous/Next tile
    Home/End        - Jump to first/last tile
    Page Up/Down    - Jump 10 tiles
    P               - Open tile picker (hierarchical: Environment > Wall > Panel)
    T               - Open sprite selector (change tile's sprite)
    F               - Toggle filter panel
    E               - Enter edit mode
    G               - Open grid settings
    F5              - Reload all data from CSV files
    ESC             - Quit (or exit edit mode)

Tile Picker Controls:
    Up/Down         - Navigate items
    Enter/Right     - Drill down to next level (or select tile at Panel level)
    Left/Backspace  - Go back to previous level
    ESC             - Close picker (or go back at non-root level)

Edit Mode Controls:
    W/S             - Select field (up/down)
    A/D             - Previous/Next tile
    Arrow Keys      - Adjust blit position (Left/Right=X, Up/Down=Y)
    0-9, -          - Type numeric value
    Backspace       - Delete character
    Enter           - Apply value and regenerate tile
    Space           - Toggle Flip (when Flip selected)
    F2              - Save all changes to CSV
    Z               - Undo changes for current tile
    ESC             - Exit edit mode

Grid Settings Mode Controls:
    Arrow Keys      - Navigate panel grid
    Space           - Toggle panel visibility
    A               - Enable all panels
    N               - Disable all panels
    ESC             - Exit grid settings
"""

import pygame as pg
import pandas as pd
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from src.dungeon_tileset import DungeonTileset
from src.utils import sub_image, SCALE_FACTOR


class TileViewer:
    """Interactive tile viewer for browsing and inspecting tiles from tiles.csv."""

    # Colors
    BG_COLOR = (40, 40, 50)
    PANEL_COLOR = (50, 50, 60)
    BORDER_COLOR = (80, 80, 100)
    TEXT_COLOR = (220, 220, 220)
    LABEL_COLOR = (150, 150, 170)
    HIGHLIGHT_COLOR = (100, 150, 200)
    HELP_COLOR = (120, 120, 140)
    EDIT_HIGHLIGHT_COLOR = (80, 100, 140)
    EDIT_CURSOR_COLOR = (200, 200, 100)
    MODIFIED_COLOR = (200, 150, 100)
    GRID_COLOR = (70, 90, 110)
    GRID_LABEL_COLOR = (100, 120, 140)
    CHECKBOX_CHECKED_COLOR = (100, 180, 100)
    CHECKBOX_UNCHECKED_COLOR = (80, 80, 90)

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1050, 500))
        pg.display.set_caption("Tile Viewer")
        self.font = pg.font.SysFont("Consolas", 16)
        self.font_small = pg.font.SysFont("Consolas", 14)
        self.font_large = pg.font.SysFont("Consolas", 20)
        self.clock = pg.time.Clock()

        # Load tileset
        print("Loading tileset...")
        self.tileset = DungeonTileset()
        self.tiles = list(self.tileset.wall_tiles.index)
        self.current_index = 0
        self.filter_active = False
        self.filter_environment = None
        self.filter_wall = None
        self.filtered_tiles = self.tiles.copy()

        # Get unique values for filtering
        self.environments = sorted(set(idx[0] for idx in self.tiles))
        self.walls = sorted(set(idx[1] for idx in self.tiles))

        # Edit mode state
        self.edit_mode = False
        self.selected_field_index = 0
        self.editable_fields = ['Xpos', 'Ypos', 'Width', 'Height', 'Blit_Xpos_Offset', 'Blit_Ypos_Offset', 'Flip']
        self.edit_buffer = ""
        self.edit_overrides = {}  # {(env, wall, panel): {field: value, 'Image': surface}}
        self.unsaved_changes = False

        # Load panel positions and sizes from CSV
        panels_df = pd.read_csv('data/panels.csv')
        panels_df = panels_df.set_index('Panel')

        self.panel_positions = {
            panel: (int(row['Blit_Xpos']) * SCALE_FACTOR, int(row['Blit_Ypos']) * SCALE_FACTOR)
            for panel, row in panels_df.iterrows()
        }

        self.panel_sizes = {
            panel: (int(row['Width']) * SCALE_FACTOR, int(row['Height']) * SCALE_FACTOR)
            for panel, row in panels_df.iterrows()
        }

        # All available panels for grid settings (organized by type)
        self.all_panels = [
            # Perpendicular panels (row 0-2)
            'LP1', 'LP2', 'LP3', 'LP4', 'RP1', 'RP2', 'RP3', 'RP4',
            'FP3', 'FP4', 'KP3', 'KP4',
            # Front panels (row 3-6)
            'CF1', 'CF2', 'CF3', 'LF1', 'LF2', 'LF3',
            'RF1', 'RF2', 'RF3', 'FF3', 'KF3',
            # Door panels (row 7-9)
            'CD1', 'CD2', 'CD3', 'LD1', 'LD2', 'LD3',
            'RD1', 'RD2', 'RD3'
        ]

        # Panel visibility settings (which grid boxes to display)
        self.panel_visibility = {panel: False for panel in self.all_panels}
        # Initialize default visible panels
        for p in ['LP1', 'LP2', 'LP3', 'LP4', 'RP1', 'RP2', 'RP3', 'RP4', 'CF1', 'CF2', 'CF3']:
            self.panel_visibility[p] = True

        # Grid settings mode state
        self.grid_settings_mode = False
        self.grid_settings_cursor = 0

        # Tile picker mode state (hierarchical: Environment -> Wall -> Panel)
        self.tile_picker_mode = False
        self.picker_level = 0  # 0=Environment, 1=Wall, 2=Panel
        self.picker_cursor = 0
        self.picker_scroll_offset = 0
        self.picker_visible_rows = 12
        self.picker_selected_env = None
        self.picker_selected_wall = None

        # Sprite selector mode state (for changing a tile's sprite)
        self.sprite_selector_mode = False
        self.selector_cursor = 0
        self.selector_scroll_offset = 0
        self.selector_visible_rows = 12
        # Get list of unique sprite names from sprites.csv (with None option at top)
        self.sprite_names = ['(None)'] + list(self.tileset.wall_tiles['SpriteName'].unique())

        print(f"Loaded {len(self.tiles)} tiles")

    def run(self):
        """Main loop."""
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if self.sprite_selector_mode:
                        self.handle_sprite_selector_key(event.key)
                    elif self.tile_picker_mode:
                        self.handle_tile_picker_key(event.key)
                    elif self.grid_settings_mode:
                        self.handle_grid_settings_key(event.key)
                    elif self.edit_mode:
                        running = self.handle_edit_key(event.key, event.unicode)
                    else:
                        running = self.handle_key(event.key)

            self.draw()
            pg.display.flip()
            self.clock.tick(30)

        pg.quit()

    def handle_key(self, key):
        """Handle keyboard input. Returns False to quit."""
        if key == pg.K_ESCAPE:
            return False
        elif key == pg.K_a:
            self.current_index = max(0, self.current_index - 1)
        elif key == pg.K_d:
            self.current_index = min(len(self.filtered_tiles) - 1, self.current_index + 1)
        elif key == pg.K_HOME:
            self.current_index = 0
        elif key == pg.K_END:
            self.current_index = len(self.filtered_tiles) - 1
        elif key == pg.K_PAGEUP:
            self.current_index = max(0, self.current_index - 10)
        elif key == pg.K_PAGEDOWN:
            self.current_index = min(len(self.filtered_tiles) - 1, self.current_index + 10)
        elif key == pg.K_f:
            self.cycle_filter()
        elif key == pg.K_r:
            self.reset_filter()
        elif key == pg.K_e:
            self.enter_edit_mode()
        elif key == pg.K_g:
            self.grid_settings_mode = True
        elif key == pg.K_p:
            self.open_tile_picker()
        elif key == pg.K_t:
            self.open_sprite_selector()
        elif key == pg.K_F5:
            self.reload()
        return True

    def cycle_filter(self):
        """Cycle through filter options."""
        if self.filter_environment is None:
            # Start filtering by first environment
            self.filter_environment = self.environments[0]
        else:
            # Cycle to next environment
            idx = self.environments.index(self.filter_environment)
            if idx < len(self.environments) - 1:
                self.filter_environment = self.environments[idx + 1]
            else:
                self.filter_environment = None

        self.apply_filter()

    def reset_filter(self):
        """Reset all filters."""
        self.filter_environment = None
        self.filter_wall = None
        self.apply_filter()

    def apply_filter(self):
        """Apply current filter settings."""
        self.filtered_tiles = [
            idx for idx in self.tiles
            if (self.filter_environment is None or idx[0] == self.filter_environment)
            and (self.filter_wall is None or idx[1] == self.filter_wall)
        ]
        self.current_index = min(self.current_index, len(self.filtered_tiles) - 1)
        self.current_index = max(0, self.current_index)

    def reload(self):
        """Reload all data from CSV files and refresh the display."""
        print("Reloading data from CSV files...")

        # Store current position info to restore after reload
        current_idx = None
        if self.filtered_tiles:
            current_idx = self.filtered_tiles[self.current_index]

        # Clear any unsaved changes
        self.edit_overrides = {}
        self.unsaved_changes = False

        # Reload tileset (this reloads tiles.csv, sprites.csv, and regenerates images)
        self.tileset = DungeonTileset()
        self.tiles = list(self.tileset.wall_tiles.index)

        # Update unique values for filtering
        self.environments = sorted(set(idx[0] for idx in self.tiles))
        self.walls = sorted(set(idx[1] for idx in self.tiles))

        # Reload panel positions and sizes from CSV
        panels_df = pd.read_csv('data/panels.csv')
        panels_df = panels_df.set_index('Panel')

        self.panel_positions = {
            panel: (int(row['Blit_Xpos']) * SCALE_FACTOR, int(row['Blit_Ypos']) * SCALE_FACTOR)
            for panel, row in panels_df.iterrows()
        }

        self.panel_sizes = {
            panel: (int(row['Width']) * SCALE_FACTOR, int(row['Height']) * SCALE_FACTOR)
            for panel, row in panels_df.iterrows()
        }

        # Update sprite names list for sprite selector
        self.sprite_names = ['(None)'] + list(self.tileset.wall_tiles['SpriteName'].unique())

        # Re-apply filter
        self.apply_filter()

        # Try to restore position
        if current_idx and current_idx in self.filtered_tiles:
            self.current_index = self.filtered_tiles.index(current_idx)
        else:
            self.current_index = min(self.current_index, len(self.filtered_tiles) - 1)
            self.current_index = max(0, self.current_index)

        print(f"Reloaded {len(self.tiles)} tiles")

    def enter_edit_mode(self):
        """Enter edit mode for the current sprite."""
        if not self.filtered_tiles:
            return
        self.edit_mode = True
        self.selected_field_index = 0
        self.edit_buffer = ""

    def exit_edit_mode(self):
        """Exit edit mode."""
        self.edit_mode = False
        self.edit_buffer = ""

    def handle_edit_key(self, key, unicode):
        """Handle keyboard input in edit mode. Returns False to quit."""
        if key == pg.K_ESCAPE:
            self.exit_edit_mode()
            return True
        elif key == pg.K_w:
            self.selected_field_index = (self.selected_field_index - 1) % len(self.editable_fields)
            self.edit_buffer = ""
        elif key == pg.K_s:
            self.selected_field_index = (self.selected_field_index + 1) % len(self.editable_fields)
            self.edit_buffer = ""
        elif key == pg.K_a:
            self.current_index = max(0, self.current_index - 1)
            self.edit_buffer = ""
        elif key == pg.K_d:
            self.current_index = min(len(self.filtered_tiles) - 1, self.current_index + 1)
            self.edit_buffer = ""
        elif key == pg.K_LEFT:
            self.adjust_blit_pos('Blit_Xpos_Offset', -1)
        elif key == pg.K_RIGHT:
            self.adjust_blit_pos('Blit_Xpos_Offset', 1)
        elif key == pg.K_UP:
            self.adjust_blit_pos('Blit_Ypos_Offset', -1)
        elif key == pg.K_DOWN:
            self.adjust_blit_pos('Blit_Ypos_Offset', 1)
        elif key == pg.K_SPACE:
            # Toggle Flip field
            field = self.editable_fields[self.selected_field_index]
            if field == 'Flip':
                self.toggle_flip()
        elif key == pg.K_RETURN:
            self.apply_edit()
        elif key == pg.K_BACKSPACE:
            self.edit_buffer = self.edit_buffer[:-1]
        elif key == pg.K_F2:
            self.save_to_csv()
        elif key == pg.K_z:
            self.undo_current_sprite()
        elif unicode and (unicode.isdigit() or unicode == '-'):
            # Only allow digits and minus sign for numeric input
            field = self.editable_fields[self.selected_field_index]
            if field != 'Flip':
                self.edit_buffer += unicode
        return True

    def handle_grid_settings_key(self, key):
        """Handle keyboard input in grid settings mode."""
        # Grid layout: 4 items per row
        items_per_row = 4
        total_panels = len(self.all_panels)

        if key == pg.K_ESCAPE:
            self.grid_settings_mode = False
        elif key == pg.K_UP:
            self.grid_settings_cursor = max(0, self.grid_settings_cursor - items_per_row)
        elif key == pg.K_DOWN:
            self.grid_settings_cursor = min(total_panels - 1, self.grid_settings_cursor + items_per_row)
        elif key == pg.K_LEFT:
            self.grid_settings_cursor = max(0, self.grid_settings_cursor - 1)
        elif key == pg.K_RIGHT:
            self.grid_settings_cursor = min(total_panels - 1, self.grid_settings_cursor + 1)
        elif key == pg.K_SPACE:
            # Toggle current panel visibility
            panel = self.all_panels[self.grid_settings_cursor]
            self.panel_visibility[panel] = not self.panel_visibility[panel]
        elif key == pg.K_a:
            # Enable all panels
            for panel in self.all_panels:
                self.panel_visibility[panel] = True
        elif key == pg.K_n:
            # Disable all panels
            for panel in self.all_panels:
                self.panel_visibility[panel] = False

    def open_tile_picker(self):
        """Open the hierarchical tile picker."""
        self.tile_picker_mode = True
        self.picker_level = 0
        self.picker_cursor = 0
        self.picker_scroll_offset = 0
        self.picker_selected_env = None
        self.picker_selected_wall = None

        # Try to pre-select based on current tile
        if self.filtered_tiles:
            current_idx = self.filtered_tiles[self.current_index]
            env, wall, panel = current_idx
            # Pre-select current environment
            if env in self.environments:
                self.picker_cursor = self.environments.index(env)
                self._adjust_picker_scroll()

    def get_picker_items(self):
        """Get the list of items for the current picker level."""
        if self.picker_level == 0:
            # Environment level
            return self.environments
        elif self.picker_level == 1:
            # Wall level - get walls for selected environment
            walls = sorted(set(
                idx[1] for idx in self.tiles
                if idx[0] == self.picker_selected_env
            ))
            return walls
        else:
            # Panel level - get panels for selected environment and wall
            panels = sorted(set(
                idx[2] for idx in self.tiles
                if idx[0] == self.picker_selected_env and idx[1] == self.picker_selected_wall
            ))
            return panels

    def handle_tile_picker_key(self, key):
        """Handle keyboard input in tile picker mode."""
        items = self.get_picker_items()
        total_items = len(items)

        if key == pg.K_ESCAPE:
            # Go back a level or close picker
            if self.picker_level == 0:
                self.tile_picker_mode = False
            else:
                self.picker_level -= 1
                self.picker_cursor = 0
                self.picker_scroll_offset = 0
                # Try to restore cursor position
                if self.picker_level == 0 and self.picker_selected_env in self.environments:
                    self.picker_cursor = self.environments.index(self.picker_selected_env)
                elif self.picker_level == 1:
                    walls = self.get_picker_items()
                    if self.picker_selected_wall in walls:
                        self.picker_cursor = walls.index(self.picker_selected_wall)
                self._adjust_picker_scroll()

        elif key == pg.K_BACKSPACE:
            # Go back a level (same as ESC but doesn't close at level 0)
            if self.picker_level > 0:
                self.picker_level -= 1
                self.picker_cursor = 0
                self.picker_scroll_offset = 0
                if self.picker_level == 0 and self.picker_selected_env in self.environments:
                    self.picker_cursor = self.environments.index(self.picker_selected_env)
                elif self.picker_level == 1:
                    walls = self.get_picker_items()
                    if self.picker_selected_wall in walls:
                        self.picker_cursor = walls.index(self.picker_selected_wall)
                self._adjust_picker_scroll()

        elif key in (pg.K_UP, pg.K_w):
            self.picker_cursor = max(0, self.picker_cursor - 1)
            self._adjust_picker_scroll()

        elif key in (pg.K_DOWN, pg.K_s):
            self.picker_cursor = min(total_items - 1, self.picker_cursor + 1)
            self._adjust_picker_scroll()

        elif key == pg.K_PAGEUP:
            self.picker_cursor = max(0, self.picker_cursor - self.picker_visible_rows)
            self._adjust_picker_scroll()

        elif key == pg.K_PAGEDOWN:
            self.picker_cursor = min(total_items - 1, self.picker_cursor + self.picker_visible_rows)
            self._adjust_picker_scroll()

        elif key == pg.K_HOME:
            self.picker_cursor = 0
            self._adjust_picker_scroll()

        elif key == pg.K_END:
            self.picker_cursor = total_items - 1
            self._adjust_picker_scroll()

        elif key in (pg.K_RETURN, pg.K_SPACE, pg.K_RIGHT):
            # Select current item and drill down or select tile
            if self.picker_level == 0:
                # Selected environment, go to wall level
                self.picker_selected_env = items[self.picker_cursor]
                self.picker_level = 1
                self.picker_cursor = 0
                self.picker_scroll_offset = 0
            elif self.picker_level == 1:
                # Selected wall, go to panel level
                self.picker_selected_wall = items[self.picker_cursor]
                self.picker_level = 2
                self.picker_cursor = 0
                self.picker_scroll_offset = 0
            else:
                # Selected panel, select the tile and close
                selected_panel = items[self.picker_cursor]
                selected_idx = (self.picker_selected_env, self.picker_selected_wall, selected_panel)

                # Find this tile in the full list
                if selected_idx in self.tiles:
                    tile_index = self.tiles.index(selected_idx)
                    # Update filtered list if needed
                    if selected_idx in self.filtered_tiles:
                        self.current_index = self.filtered_tiles.index(selected_idx)
                    else:
                        # Reset filter to show selected tile
                        self.filter_environment = None
                        self.filter_wall = None
                        self.filtered_tiles = self.tiles.copy()
                        self.current_index = tile_index
                    self.tile_picker_mode = False

        elif key == pg.K_LEFT:
            # Go back a level
            if self.picker_level > 0:
                self.picker_level -= 1
                self.picker_cursor = 0
                self.picker_scroll_offset = 0
                if self.picker_level == 0 and self.picker_selected_env in self.environments:
                    self.picker_cursor = self.environments.index(self.picker_selected_env)
                elif self.picker_level == 1:
                    walls = self.get_picker_items()
                    if self.picker_selected_wall in walls:
                        self.picker_cursor = walls.index(self.picker_selected_wall)
                self._adjust_picker_scroll()

    def _adjust_picker_scroll(self):
        """Adjust scroll offset to keep cursor visible."""
        if self.picker_cursor < self.picker_scroll_offset:
            self.picker_scroll_offset = self.picker_cursor
        elif self.picker_cursor >= self.picker_scroll_offset + self.picker_visible_rows:
            self.picker_scroll_offset = self.picker_cursor - self.picker_visible_rows + 1

    def open_sprite_selector(self):
        """Open sprite selector for current tile."""
        if not self.filtered_tiles:
            return
        self.sprite_selector_mode = True
        # Position cursor at current sprite
        data = self.get_current_sprite_data()
        if data:
            current_sprite = data['SpriteName']
            if current_sprite == '' or current_sprite is None:
                self.selector_cursor = 0  # Position at "(None)"
            elif current_sprite in self.sprite_names:
                self.selector_cursor = self.sprite_names.index(current_sprite)
            else:
                self.selector_cursor = 0
        else:
            self.selector_cursor = 0
        self.selector_scroll_offset = max(0, self.selector_cursor - self.selector_visible_rows // 2)

    def handle_sprite_selector_key(self, key):
        """Handle keyboard input in sprite selector mode."""
        total_sprites = len(self.sprite_names)

        if key == pg.K_ESCAPE:
            self.sprite_selector_mode = False
        elif key in (pg.K_UP, pg.K_w):
            self.selector_cursor = max(0, self.selector_cursor - 1)
            self._adjust_selector_scroll()
        elif key in (pg.K_DOWN, pg.K_s):
            self.selector_cursor = min(total_sprites - 1, self.selector_cursor + 1)
            self._adjust_selector_scroll()
        elif key == pg.K_PAGEUP:
            self.selector_cursor = max(0, self.selector_cursor - self.selector_visible_rows)
            self._adjust_selector_scroll()
        elif key == pg.K_PAGEDOWN:
            self.selector_cursor = min(total_sprites - 1, self.selector_cursor + self.selector_visible_rows)
            self._adjust_selector_scroll()
        elif key == pg.K_HOME:
            self.selector_cursor = 0
            self._adjust_selector_scroll()
        elif key == pg.K_END:
            self.selector_cursor = total_sprites - 1
            self._adjust_selector_scroll()
        elif key in (pg.K_RETURN, pg.K_SPACE):
            # Apply selected sprite to current tile
            self.apply_sprite_selection()
            self.sprite_selector_mode = False

    def _adjust_selector_scroll(self):
        """Adjust scroll offset to keep cursor visible in sprite selector."""
        if self.selector_cursor < self.selector_scroll_offset:
            self.selector_scroll_offset = self.selector_cursor
        elif self.selector_cursor >= self.selector_scroll_offset + self.selector_visible_rows:
            self.selector_scroll_offset = self.selector_cursor - self.selector_visible_rows + 1

    def apply_sprite_selection(self):
        """Apply the selected sprite to the current tile."""
        if not self.filtered_tiles:
            return

        selected_sprite_name = self.sprite_names[self.selector_cursor]
        idx = self.filtered_tiles[self.current_index]

        # Update overrides with new sprite data
        if idx not in self.edit_overrides:
            self.edit_overrides[idx] = {}

        # Handle "(None)" selection - no sprite
        if selected_sprite_name == '(None)':
            self.edit_overrides[idx]['SpriteName'] = ''
            self.edit_overrides[idx]['Image'] = None
            self.unsaved_changes = True
            return

        # Get sprite data from sprites DataFrame
        import pandas as pd
        sprites_df = pd.read_csv('data/sprites.csv').set_index('SpriteName')
        sprite_row = sprites_df.loc[selected_sprite_name]

        self.edit_overrides[idx]['SpriteName'] = selected_sprite_name
        self.edit_overrides[idx]['Xpos'] = int(sprite_row['Xpos'])
        self.edit_overrides[idx]['Ypos'] = int(sprite_row['Ypos'])
        self.edit_overrides[idx]['Width'] = int(sprite_row['Width'])
        self.edit_overrides[idx]['Height'] = int(sprite_row['Height'])
        self.edit_overrides[idx]['File'] = sprite_row['File']

        self.unsaved_changes = True
        self.regenerate_sprite()

    def get_effective_value(self, field):
        """Get the effective value for a field (override or original)."""
        if not self.filtered_tiles:
            return None
        idx = self.filtered_tiles[self.current_index]
        overrides = self.edit_overrides.get(idx, {})
        if field in overrides:
            return overrides[field]
        row = self.tileset.wall_tiles.loc[idx]
        return row[field]

    def is_field_modified(self, field):
        """Check if a field has been modified from its original value."""
        if not self.filtered_tiles:
            return False
        idx = self.filtered_tiles[self.current_index]
        overrides = self.edit_overrides.get(idx, {})
        return field in overrides

    def toggle_flip(self):
        """Toggle the Flip value for the current sprite."""
        if not self.filtered_tiles:
            return
        idx = self.filtered_tiles[self.current_index]
        current_flip = self.get_effective_value('Flip')
        self.set_override('Flip', not current_flip)
        self.regenerate_sprite()

    def adjust_blit_pos(self, field, delta):
        """Adjust Blit_Xpos_Offset or Blit_Ypos_Offset by delta."""
        if not self.filtered_tiles:
            return
        current_value = self.get_effective_value(field)
        self.set_override(field, current_value + delta)

    def set_override(self, field, value):
        """Set an override value for the current sprite."""
        if not self.filtered_tiles:
            return
        idx = self.filtered_tiles[self.current_index]
        if idx not in self.edit_overrides:
            self.edit_overrides[idx] = {}
        self.edit_overrides[idx][field] = value
        self.unsaved_changes = True

    def apply_edit(self):
        """Apply the current edit buffer to the selected field."""
        if not self.edit_buffer:
            return
        field = self.editable_fields[self.selected_field_index]
        if field == 'Flip':
            return  # Flip is toggled with space, not typed

        try:
            value = int(self.edit_buffer)
            self.set_override(field, value)
            self.regenerate_sprite()
            self.edit_buffer = ""
        except ValueError:
            # Invalid input, clear buffer
            self.edit_buffer = ""

    def regenerate_sprite(self):
        """Regenerate the sprite image with current override values."""
        if not self.filtered_tiles:
            return
        idx = self.filtered_tiles[self.current_index]
        row = self.tileset.wall_tiles.loc[idx]
        overrides = self.edit_overrides.get(idx, {})

        # Get values (override or original)
        xpos = overrides.get('Xpos', row['Xpos'])
        ypos = overrides.get('Ypos', row['Ypos'])
        width = overrides.get('Width', row['Width'])
        height = overrides.get('Height', row['Height'])
        flip = overrides.get('Flip', row['Flip'])

        # Validate dimensions
        if width <= 0 or height <= 0:
            return

        # Get source sprite sheet (use override if available)
        file = overrides.get('File', row['File'])
        source_image = self.tileset.wallset_images.loc[file, 'Image']

        # Extract new sprite using sub_image
        try:
            new_sprite = sub_image(source_image, (xpos, ypos, width, height), 3, flip)
            overrides['Image'] = new_sprite
            self.edit_overrides[idx] = overrides
        except Exception:
            # If extraction fails, don't update the image
            pass

    def undo_current_sprite(self):
        """Undo all changes for the current sprite."""
        if not self.filtered_tiles:
            return
        idx = self.filtered_tiles[self.current_index]
        if idx in self.edit_overrides:
            del self.edit_overrides[idx]
            # Check if there are still unsaved changes
            self.unsaved_changes = bool(self.edit_overrides)

    def save_to_csv(self):
        """Save all modifications to the CSV files."""
        if not self.edit_overrides:
            return

        import pandas as pd

        # Load current CSV files
        sprites_df = pd.read_csv('data/sprites.csv')
        sprites_df = sprites_df.set_index('SpriteName')

        panels_df = pd.read_csv('data/panels.csv')
        panels_df = panels_df.set_index('Panel')

        tiles_df = pd.read_csv('data/tiles.csv')

        # Track what we've modified
        modified_sprites = set()
        modified_panels = set()

        # Apply overrides
        for idx, overrides in self.edit_overrides.items():
            env, wall, panel = idx
            row = self.tileset.wall_tiles.loc[idx]
            sprite_name = row['SpriteName']

            # Update sprite source coordinates
            for field in ['Xpos', 'Ypos', 'Width', 'Height']:
                if field in overrides:
                    sprites_df.loc[sprite_name, field] = overrides[field]
                    modified_sprites.add(sprite_name)

            # Update tile blit position offsets in tiles.csv
            for field in ['Blit_Xpos_Offset', 'Blit_Ypos_Offset']:
                if field in overrides:
                    mask = (tiles_df['Environment'] == env) & \
                           (tiles_df['Wall'] == wall) & \
                           (tiles_df['Panel'] == panel)
                    tiles_df.loc[mask, field] = overrides[field]

            # Update flip in tiles.csv
            if 'Flip' in overrides:
                mask = (tiles_df['Environment'] == env) & \
                       (tiles_df['Wall'] == wall) & \
                       (tiles_df['Panel'] == panel)
                tiles_df.loc[mask, 'Flip'] = overrides['Flip']

            # Update SpriteName in tiles.csv
            if 'SpriteName' in overrides:
                mask = (tiles_df['Environment'] == env) & \
                       (tiles_df['Wall'] == wall) & \
                       (tiles_df['Panel'] == panel)
                tiles_df.loc[mask, 'SpriteName'] = overrides['SpriteName']

        # Save back to CSV
        sprites_df.reset_index().to_csv('data/sprites.csv', index=False)
        panels_df.reset_index().to_csv('data/panels.csv', index=False)
        tiles_df.to_csv('data/tiles.csv', index=False)

        # Update the tileset's dataframes to reflect saved changes
        for idx, overrides in self.edit_overrides.items():
            for field in ['Xpos', 'Ypos', 'Width', 'Height', 'Blit_Xpos_Offset', 'Blit_Ypos_Offset', 'Flip', 'SpriteName', 'File']:
                if field in overrides:
                    self.tileset.wall_tiles.loc[idx, field] = overrides[field]
            # Keep the regenerated image
            if 'Image' in overrides:
                self.tileset.wall_tiles.loc[idx, 'Image'] = overrides['Image']

        # Clear overrides and mark as saved
        self.edit_overrides = {}
        self.unsaved_changes = False

        print(f"Saved changes: {len(modified_sprites)} sprites, {len(modified_panels)} panels")

    def get_current_sprite_data(self):
        """Get all data for the current sprite, with overrides applied."""
        if not self.filtered_tiles:
            return None

        idx = self.filtered_tiles[self.current_index]
        row = self.tileset.wall_tiles.loc[idx]
        overrides = self.edit_overrides.get(idx, {})

        return {
            'Environment': idx[0],
            'Wall': idx[1],
            'Panel': idx[2],
            'SpriteName': overrides.get('SpriteName', row['SpriteName']),
            'File': overrides.get('File', row['File']),
            'Xpos': overrides.get('Xpos', row['Xpos']),
            'Ypos': overrides.get('Ypos', row['Ypos']),
            'Width': overrides.get('Width', row['Width']),
            'Height': overrides.get('Height', row['Height']),
            'Flip': overrides.get('Flip', row['Flip']),
            'Blit_Xpos': row['Blit_Xpos'],
            'Blit_Ypos': row['Blit_Ypos'],
            'Blit_Xpos_Offset': overrides.get('Blit_Xpos_Offset', row['Blit_Xpos_Offset']),
            'Blit_Ypos_Offset': overrides.get('Blit_Ypos_Offset', row['Blit_Ypos_Offset']),
            'Image': overrides.get('Image', row['Image'])
        }

    def draw(self):
        """Draw the viewer interface."""
        self.screen.fill(self.BG_COLOR)

        # Draw title bar
        self.draw_title_bar()

        # Draw viewport panel (left side) with panel grid
        self.draw_viewport_panel()

        # Draw metadata panel (right side)
        self.draw_metadata_panel()

        # Draw help bar (bottom)
        self.draw_help_bar()

        # Draw overlay modes
        if self.grid_settings_mode:
            self.draw_grid_settings_panel()
        elif self.tile_picker_mode:
            self.draw_tile_picker()
        elif self.sprite_selector_mode:
            self.draw_sprite_selector()

    def draw_title_bar(self):
        """Draw the title bar with sprite count."""
        title_rect = pg.Rect(10, 10, 1030, 35)
        pg.draw.rect(self.screen, self.PANEL_COLOR, title_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, title_rect, 1)

        # Title text
        filter_text = ""
        if self.filter_environment:
            filter_text = f" [Filter: {self.filter_environment}]"

        edit_text = ""
        if self.edit_mode:
            edit_text = " [EDIT MODE]"
            if self.unsaved_changes:
                edit_text = " [EDIT MODE*]"

        title = f"Tile Viewer - {self.current_index + 1}/{len(self.filtered_tiles)} tiles{filter_text}{edit_text}"
        title_color = self.MODIFIED_COLOR if self.edit_mode else self.TEXT_COLOR
        title_surf = self.font_large.render(title, True, title_color)
        self.screen.blit(title_surf, (20, 17))

    def draw_viewport_panel(self):
        """Draw the dungeon viewport with panel grid and sprite."""
        # Viewport area: 528x360 + padding
        viewport_x = 10
        viewport_y = 55
        viewport_w = 528
        viewport_h = 360

        # Draw background panel
        panel_rect = pg.Rect(viewport_x, viewport_y, viewport_w + 20, viewport_h + 20)
        pg.draw.rect(self.screen, self.PANEL_COLOR, panel_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, panel_rect, 1)

        # Viewport origin (top-left of the 528x360 area)
        vx = viewport_x + 10
        vy = viewport_y + 10

        # Draw checkerboard background for viewport
        self.draw_checkerboard(vx, vy, viewport_w, viewport_h)

        # Draw panel grid boxes
        self.draw_panel_grid(vx, vy)

        # Render current sprite at blit position
        data = self.get_current_sprite_data()
        if data:
            # Only render image if one exists
            if data['Image']:
                blit_x = vx + (data['Blit_Xpos'] + data['Blit_Xpos_Offset']) * SCALE_FACTOR
                blit_y = vy + (data['Blit_Ypos'] + data['Blit_Ypos_Offset']) * SCALE_FACTOR
                self.screen.blit(data['Image'], (blit_x, blit_y))

            # Highlight current panel (even if no sprite)
            panel = data['Panel']
            if panel in self.panel_positions:
                pos = self.panel_positions[panel]
                size = self.panel_sizes.get(panel, (50, 50))
                # Only highlight if panel is visible (not off-screen)
                if pos[0] >= 0 and pos[1] >= 0:
                    highlight_rect = pg.Rect(vx + pos[0], vy + pos[1], size[0], size[1])
                    pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, highlight_rect, 2)

                    # Draw center gridlines (red crosshairs across entire viewport)
                    center_x = vx + pos[0] + size[0] // 2
                    center_y = vy + pos[1] + size[1] // 2
                    # Vertical line (full viewport height)
                    pg.draw.line(self.screen, (255, 0, 0),
                                 (center_x, vy), (center_x, vy + viewport_h), 1)
                    # Horizontal line (full viewport width)
                    pg.draw.line(self.screen, (255, 0, 0),
                                 (vx, center_y), (vx + viewport_w, center_y), 1)

    def draw_panel_grid(self, vx, vy):
        """Draw grid boxes for each panel position."""
        for panel in self.all_panels:
            # Check if panel is visible
            if not self.panel_visibility.get(panel, False):
                continue

            pos = self.panel_positions.get(panel)
            size = self.panel_sizes.get(panel)
            if not pos or not size:
                continue

            # Skip panels with negative positions (off-screen)
            if pos[0] < 0 or pos[1] < 0:
                continue

            # Draw panel box
            rect = pg.Rect(vx + pos[0], vy + pos[1], size[0], size[1])
            pg.draw.rect(self.screen, self.GRID_COLOR, rect, 1)

            # Draw panel label (small font)
            label = self.font_small.render(panel, True, self.GRID_LABEL_COLOR)
            self.screen.blit(label, (rect.x + 2, rect.y + 2))

    def draw_checkerboard(self, x, y, width, height, tile_size=8):
        """Draw a checkerboard pattern for transparency visualization."""
        colors = [(60, 60, 70), (70, 70, 80)]
        for row in range(0, height, tile_size):
            for col in range(0, width, tile_size):
                color = colors[(row // tile_size + col // tile_size) % 2]
                rect = pg.Rect(x + col, y + row,
                              min(tile_size, width - col),
                              min(tile_size, height - row))
                pg.draw.rect(self.screen, color, rect)

    def draw_grid_settings_panel(self):
        """Draw the grid settings overlay panel."""
        # Semi-transparent overlay
        overlay = pg.Surface((1050, 500), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Main panel
        panel_w, panel_h = 500, 430
        panel_x = (1050 - panel_w) // 2
        panel_y = (500 - panel_h) // 2
        panel_rect = pg.Rect(panel_x, panel_y, panel_w, panel_h)
        pg.draw.rect(self.screen, self.PANEL_COLOR, panel_rect)
        pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, panel_rect, 2)

        # Title
        title = self.font_large.render("Grid Panel Settings", True, self.TEXT_COLOR)
        self.screen.blit(title, (panel_x + 20, panel_y + 15))

        # Separator line
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, panel_y + 45), (panel_x + panel_w - 10, panel_y + 45))

        # Panel groups with labels
        groups = [
            ("Perpendicular Panels:", ['LP1', 'LP2', 'LP3', 'LP4', 'RP1', 'RP2', 'RP3', 'RP4', 'FP3', 'FP4', 'KP3', 'KP4']),
            ("Front Panels:", ['CF1', 'CF2', 'CF3', 'LF1', 'LF2', 'LF3', 'RF1', 'RF2', 'RF3', 'FF3', 'KF3']),
            ("Door Panels:", ['CD1', 'CD2', 'CD3', 'LD1', 'LD2', 'LD3', 'RD1', 'RD2', 'RD3']),
        ]

        y = panel_y + 60
        items_per_row = 4
        item_width = 110
        checkbox_size = 14

        for group_label, panels in groups:
            # Group label
            label_surf = self.font.render(group_label, True, self.LABEL_COLOR)
            self.screen.blit(label_surf, (panel_x + 20, y))
            y += 25

            # Draw panels in rows of 4
            for i, panel in enumerate(panels):
                row = i // items_per_row
                col = i % items_per_row
                x = panel_x + 30 + col * item_width
                item_y = y + row * 24

                # Get cursor index for this panel
                panel_index = self.all_panels.index(panel)
                is_selected = (panel_index == self.grid_settings_cursor)
                is_checked = self.panel_visibility.get(panel, False)

                # Selection indicator
                if is_selected:
                    indicator = self.font.render(">", True, self.EDIT_CURSOR_COLOR)
                    self.screen.blit(indicator, (x - 15, item_y))

                # Checkbox
                checkbox_rect = pg.Rect(x, item_y + 2, checkbox_size, checkbox_size)
                if is_checked:
                    pg.draw.rect(self.screen, self.CHECKBOX_CHECKED_COLOR, checkbox_rect)
                    # Draw checkmark
                    pg.draw.line(self.screen, self.TEXT_COLOR,
                                 (x + 3, item_y + 9), (x + 6, item_y + 12), 2)
                    pg.draw.line(self.screen, self.TEXT_COLOR,
                                 (x + 6, item_y + 12), (x + 11, item_y + 5), 2)
                else:
                    pg.draw.rect(self.screen, self.CHECKBOX_UNCHECKED_COLOR, checkbox_rect)
                pg.draw.rect(self.screen, self.BORDER_COLOR, checkbox_rect, 1)

                # Panel name
                text_color = self.TEXT_COLOR if is_checked else self.HELP_COLOR
                if is_selected:
                    text_color = self.EDIT_CURSOR_COLOR
                panel_text = self.font.render(panel, True, text_color)
                self.screen.blit(panel_text, (x + checkbox_size + 5, item_y))

            # Move y past this group's rows
            rows_in_group = (len(panels) + items_per_row - 1) // items_per_row
            y += rows_in_group * 24 + 15

        # Help text at bottom
        help_y = panel_y + panel_h - 50
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, help_y - 10), (panel_x + panel_w - 10, help_y - 10))
        help_text = "[Arrows] Navigate  [Space] Toggle  [A] All  [N] None  [ESC] Done"
        help_surf = self.font_small.render(help_text, True, self.HELP_COLOR)
        self.screen.blit(help_surf, (panel_x + (panel_w - help_surf.get_width()) // 2, help_y))

    def draw_tile_picker(self):
        """Draw the hierarchical tile picker overlay panel."""
        # Semi-transparent overlay
        overlay = pg.Surface((1050, 500), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Main panel
        panel_w, panel_h = 500, 450
        panel_x = (1050 - panel_w) // 2
        panel_y = (500 - panel_h) // 2
        panel_rect = pg.Rect(panel_x, panel_y, panel_w, panel_h)
        pg.draw.rect(self.screen, self.PANEL_COLOR, panel_rect)
        pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, panel_rect, 2)

        # Title based on level
        level_titles = ["Select Environment", "Select Wall", "Select Panel"]
        title = self.font_large.render(level_titles[self.picker_level], True, self.TEXT_COLOR)
        self.screen.blit(title, (panel_x + 20, panel_y + 15))

        # Breadcrumb showing current path
        breadcrumb_y = panel_y + 45
        breadcrumb_parts = []
        if self.picker_selected_env:
            breadcrumb_parts.append(self.picker_selected_env)
        if self.picker_selected_wall:
            breadcrumb_parts.append(self.picker_selected_wall)

        if breadcrumb_parts:
            breadcrumb_text = " > ".join(breadcrumb_parts)
            breadcrumb_surf = self.font.render(breadcrumb_text, True, self.HIGHLIGHT_COLOR)
            self.screen.blit(breadcrumb_surf, (panel_x + 20, breadcrumb_y))

        # Separator line
        sep_y = panel_y + 70
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, sep_y), (panel_x + panel_w - 10, sep_y))

        # Get items for current level
        items = self.get_picker_items()
        total_items = len(items)

        # Draw item list
        list_y = sep_y + 15
        row_height = 28
        thumb_size = 24

        for i in range(self.picker_visible_rows):
            item_idx = self.picker_scroll_offset + i
            if item_idx >= total_items:
                break

            item = items[item_idx]
            row_y = list_y + i * row_height
            is_selected = (item_idx == self.picker_cursor)

            # Selection highlight
            if is_selected:
                highlight_rect = pg.Rect(panel_x + 15, row_y - 2, panel_w - 30, row_height)
                pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

            # Draw item based on level
            if self.picker_level == 2:
                # Panel level - show thumbnail and sprite info
                tile_idx = (self.picker_selected_env, self.picker_selected_wall, item)
                if tile_idx in self.tileset.wall_tiles.index:
                    row = self.tileset.wall_tiles.loc[tile_idx]
                    image = row['Image']
                    sprite_name = row['SpriteName']

                    # Draw thumbnail
                    thumb_x = panel_x + 25
                    if image:
                        img_w, img_h = image.get_width(), image.get_height()
                        scale = min(thumb_size / img_w, thumb_size / img_h, 1.0)
                        new_w = max(1, int(img_w * scale))
                        new_h = max(1, int(img_h * scale))
                        thumb = pg.transform.scale(image, (new_w, new_h))
                        thumb_draw_y = row_y + (row_height - new_h) // 2 - 2
                        self.screen.blit(thumb, (thumb_x, thumb_draw_y))

                    # Draw panel name and sprite
                    text_color = self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR
                    panel_surf = self.font.render(str(item), True, text_color)
                    self.screen.blit(panel_surf, (panel_x + 60, row_y))

                    sprite_text = str(sprite_name)[:35] if sprite_name else "(None)"
                    sprite_surf = self.font_small.render(sprite_text, True, self.LABEL_COLOR)
                    self.screen.blit(sprite_surf, (panel_x + 120, row_y + 2))
            else:
                # Environment or Wall level - show name and count
                text_color = self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR

                # Count items at next level
                if self.picker_level == 0:
                    count = len(set(idx[1] for idx in self.tiles if idx[0] == item))
                    count_label = f"({count} walls)"
                else:
                    count = len(set(idx[2] for idx in self.tiles
                                   if idx[0] == self.picker_selected_env and idx[1] == item))
                    count_label = f"({count} panels)"

                # Draw arrow indicator for drill-down
                arrow_surf = self.font.render(">", True, text_color)
                self.screen.blit(arrow_surf, (panel_x + 25, row_y))

                item_surf = self.font.render(str(item), True, text_color)
                self.screen.blit(item_surf, (panel_x + 50, row_y))

                count_surf = self.font_small.render(count_label, True, self.LABEL_COLOR)
                self.screen.blit(count_surf, (panel_x + 200, row_y + 2))

        # Scrollbar
        scrollbar_x = panel_x + panel_w - 20
        scrollbar_y = list_y
        scrollbar_h = self.picker_visible_rows * row_height
        pg.draw.rect(self.screen, self.BORDER_COLOR, (scrollbar_x, scrollbar_y, 8, scrollbar_h), 1)

        # Scrollbar thumb
        if total_items > self.picker_visible_rows:
            thumb_h = max(20, scrollbar_h * self.picker_visible_rows // total_items)
            thumb_y = scrollbar_y + (scrollbar_h - thumb_h) * self.picker_scroll_offset // (total_items - self.picker_visible_rows)
            pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, (scrollbar_x + 1, thumb_y, 6, thumb_h))

        # Help text at bottom
        help_y = panel_y + panel_h - 30
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, help_y - 10), (panel_x + panel_w - 10, help_y - 10))

        if self.picker_level == 2:
            help_text = "[Up/Down] Navigate  [Enter] Select  [Left/Backspace] Back  [ESC] Close"
        else:
            help_text = "[Up/Down] Navigate  [Enter/Right] Drill Down  [Left/Backspace] Back  [ESC] Close"
        help_surf = self.font_small.render(help_text, True, self.HELP_COLOR)
        self.screen.blit(help_surf, (panel_x + (panel_w - help_surf.get_width()) // 2, help_y))

    def draw_sprite_selector(self):
        """Draw the sprite selector overlay for changing a tile's sprite."""
        import pandas as pd

        # Semi-transparent overlay
        overlay = pg.Surface((1050, 500), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Main panel
        panel_w, panel_h = 700, 450
        panel_x = (1050 - panel_w) // 2
        panel_y = (500 - panel_h) // 2
        panel_rect = pg.Rect(panel_x, panel_y, panel_w, panel_h)
        pg.draw.rect(self.screen, self.PANEL_COLOR, panel_rect)
        pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, panel_rect, 2)

        # Title
        data = self.get_current_sprite_data()
        current_sprite = data['SpriteName'] if data else "None"
        title = self.font_large.render(f"Select Sprite for Tile", True, self.TEXT_COLOR)
        self.screen.blit(title, (panel_x + 20, panel_y + 15))

        # Show current tile info
        if data:
            info_text = f"Current: {data['Environment']}/{data['Wall']}/{data['Panel']}"
            info_surf = self.font_small.render(info_text, True, self.LABEL_COLOR)
            self.screen.blit(info_surf, (panel_x + 300, panel_y + 20))

        # Separator line
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, panel_y + 45), (panel_x + panel_w - 10, panel_y + 45))

        # Column headers
        header_y = panel_y + 55
        col_thumb = panel_x + 20
        col_sprite = panel_x + 80
        col_file = panel_x + 350
        col_size = panel_x + 550

        headers = [
            (col_thumb, "Thumb"),
            (col_sprite, "SpriteName"),
            (col_file, "File"),
            (col_size, "Size"),
        ]
        for col_x, header in headers:
            header_surf = self.font_small.render(header, True, self.LABEL_COLOR)
            self.screen.blit(header_surf, (col_x, header_y))

        # Separator line under headers
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, header_y + 20), (panel_x + panel_w - 10, header_y + 20))

        # Load sprites data for display
        sprites_df = pd.read_csv('data/sprites.csv').set_index('SpriteName')

        # Draw sprite list
        list_y = header_y + 28
        row_height = 28
        thumb_size = 24

        for i in range(self.selector_visible_rows):
            sprite_idx = self.selector_scroll_offset + i
            if sprite_idx >= len(self.sprite_names):
                break

            sprite_name = self.sprite_names[sprite_idx]
            row_y = list_y + i * row_height
            is_selected = (sprite_idx == self.selector_cursor)
            is_current = (sprite_name == current_sprite) or (sprite_name == '(None)' and current_sprite == '')

            # Selection highlight
            if is_selected:
                highlight_rect = pg.Rect(panel_x + 15, row_y - 2, panel_w - 30, row_height)
                pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

            # Draw text columns
            if is_current:
                text_color = self.CHECKBOX_CHECKED_COLOR
            elif is_selected:
                text_color = self.EDIT_CURSOR_COLOR
            else:
                text_color = self.TEXT_COLOR

            # Handle "(None)" option specially
            if sprite_name == '(None)':
                sprite_surf = self.font_small.render("(None) - No sprite", True, text_color)
                self.screen.blit(sprite_surf, (col_sprite, row_y))
                # Mark current sprite
                if is_current:
                    marker = self.font_small.render("*", True, self.CHECKBOX_CHECKED_COLOR)
                    self.screen.blit(marker, (col_thumb - 10, row_y))
                continue

            # Get sprite info
            sprite_row = sprites_df.loc[sprite_name]
            file_name = sprite_row['File']
            width = int(sprite_row['Width'])
            height = int(sprite_row['Height'])

            # Draw thumbnail - find a tile that uses this sprite to get the image
            matching_tiles = self.tileset.wall_tiles[self.tileset.wall_tiles['SpriteName'] == sprite_name]
            if len(matching_tiles) > 0:
                image = matching_tiles.iloc[0]['Image']
                if image:
                    img_w, img_h = image.get_width(), image.get_height()
                    scale = min(thumb_size / img_w, thumb_size / img_h, 1.0)
                    new_w = max(1, int(img_w * scale))
                    new_h = max(1, int(img_h * scale))
                    thumb = pg.transform.scale(image, (new_w, new_h))
                    thumb_x = col_thumb + (thumb_size - new_w) // 2
                    thumb_y = row_y + (row_height - new_h) // 2 - 2
                    self.screen.blit(thumb, (thumb_x, thumb_y))

            # Truncate long names
            display_name = sprite_name[:35] + "..." if len(sprite_name) > 35 else sprite_name
            display_file = file_name[:25] + "..." if len(file_name) > 25 else file_name

            sprite_surf = self.font_small.render(display_name, True, text_color)
            file_surf = self.font_small.render(display_file, True, text_color)
            size_surf = self.font_small.render(f"{width}x{height}", True, text_color)

            self.screen.blit(sprite_surf, (col_sprite, row_y))
            self.screen.blit(file_surf, (col_file, row_y))
            self.screen.blit(size_surf, (col_size, row_y))

            # Mark current sprite
            if is_current:
                marker = self.font_small.render("*", True, self.CHECKBOX_CHECKED_COLOR)
                self.screen.blit(marker, (col_thumb - 10, row_y))

        # Scrollbar
        scrollbar_x = panel_x + panel_w - 20
        scrollbar_y = list_y
        scrollbar_h = self.selector_visible_rows * row_height
        pg.draw.rect(self.screen, self.BORDER_COLOR, (scrollbar_x, scrollbar_y, 8, scrollbar_h), 1)

        # Scrollbar thumb
        if len(self.sprite_names) > self.selector_visible_rows:
            thumb_h = max(20, scrollbar_h * self.selector_visible_rows // len(self.sprite_names))
            thumb_y = scrollbar_y + (scrollbar_h - thumb_h) * self.selector_scroll_offset // (len(self.sprite_names) - self.selector_visible_rows)
            pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, (scrollbar_x + 1, thumb_y, 6, thumb_h))

        # Help text at bottom
        help_y = panel_y + panel_h - 30
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_x + 10, help_y - 10), (panel_x + panel_w - 10, help_y - 10))
        help_text = "[W/S/Arrows] Navigate  [PgUp/Dn] Page  [Enter/Space] Apply  [ESC] Cancel"
        help_surf = self.font_small.render(help_text, True, self.HELP_COLOR)
        self.screen.blit(help_surf, (panel_x + (panel_w - help_surf.get_width()) // 2, help_y))

    def draw_metadata_panel(self):
        """Draw the metadata display panel."""
        panel_rect = pg.Rect(558, 55, 480, 380)
        pg.draw.rect(self.screen, self.PANEL_COLOR, panel_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, panel_rect, 1)

        data = self.get_current_sprite_data()
        if not data:
            return

        if self.edit_mode:
            self.draw_edit_mode_metadata(panel_rect, data)
        else:
            self.draw_normal_metadata(panel_rect, data)

    def draw_normal_metadata(self, panel_rect, data):
        """Draw metadata in normal (non-edit) mode."""
        # Metadata fields to display
        # Handle empty/None sprite
        sprite_name = data['SpriteName'] if data['SpriteName'] else "(None)"
        file_name = data['File'] if data['File'] and str(data['File']) != 'nan' else "-"

        fields = [
            ("Environment", data['Environment']),
            ("Wall", data['Wall']),
            ("Panel", data['Panel']),
            ("", ""),  # Spacer
            ("SpriteName", sprite_name),
            ("File", file_name),
        ]

        # Only show sprite details if there's a sprite assigned
        if data['SpriteName'] and data['Image']:
            total_blit_x = data['Blit_Xpos'] + data['Blit_Xpos_Offset']
            total_blit_y = data['Blit_Ypos'] + data['Blit_Ypos_Offset']
            fields.extend([
                ("", ""),  # Spacer
                ("Source Position", f"({data['Xpos']}, {data['Ypos']})"),
                ("Source Size", f"{data['Width']} x {data['Height']}"),
                ("Flip", str(data['Flip'])),
                ("", ""),  # Spacer
                ("Panel Blit Pos", f"({data['Blit_Xpos']}, {data['Blit_Ypos']})"),
                ("Blit Offset", f"({data['Blit_Xpos_Offset']}, {data['Blit_Ypos_Offset']})"),
                ("Total Blit Pos", f"({total_blit_x}, {total_blit_y})"),
                ("Scaled Blit Pos", f"({total_blit_x * SCALE_FACTOR}, {total_blit_y * SCALE_FACTOR})"),
            ])

        if data['Image']:
            fields.append(("", ""))  # Spacer
            fields.append(("Actual Size", f"{data['Image'].get_width()} x {data['Image'].get_height()}"))

        y = panel_rect.y + 15
        for label, value in fields:
            if label == "" and value == "":
                y += 10  # Spacer
                continue

            # Draw label
            label_surf = self.font.render(f"{label}:", True, self.LABEL_COLOR)
            self.screen.blit(label_surf, (panel_rect.x + 15, y))

            # Draw value (may need to truncate long strings)
            value_str = str(value)
            if len(value_str) > 45:
                value_str = value_str[:42] + "..."
            value_surf = self.font.render(value_str, True, self.TEXT_COLOR)
            self.screen.blit(value_surf, (panel_rect.x + 150, y))

            y += 25

    def draw_edit_mode_metadata(self, panel_rect, data):
        """Draw metadata panel in edit mode with editable fields."""
        y = panel_rect.y + 15

        # Non-editable header fields
        header_fields = [
            ("Environment", data['Environment']),
            ("Wall", data['Wall']),
            ("Panel", data['Panel']),
        ]

        for label, value in header_fields:
            label_surf = self.font.render(f"{label}:", True, self.LABEL_COLOR)
            self.screen.blit(label_surf, (panel_rect.x + 15, y))
            value_surf = self.font.render(str(value), True, self.TEXT_COLOR)
            self.screen.blit(value_surf, (panel_rect.x + 150, y))
            y += 25

        y += 10  # Spacer

        # Editable fields
        for i, field in enumerate(self.editable_fields):
            is_selected = (i == self.selected_field_index)
            is_modified = self.is_field_modified(field)

            # Draw selection highlight
            if is_selected:
                highlight_rect = pg.Rect(panel_rect.x + 10, y - 2, panel_rect.width - 20, 22)
                pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

            # Draw selection indicator
            indicator = ">" if is_selected else " "
            indicator_surf = self.font.render(indicator, True, self.EDIT_CURSOR_COLOR)
            self.screen.blit(indicator_surf, (panel_rect.x + 15, y))

            # Draw label with modified indicator
            label_text = f"{field}:" + ("*" if is_modified else "")
            label_color = self.MODIFIED_COLOR if is_modified else self.LABEL_COLOR
            label_surf = self.font.render(label_text, True, label_color)
            self.screen.blit(label_surf, (panel_rect.x + 30, y))

            # Draw value or edit buffer
            if is_selected and self.edit_buffer:
                # Show edit buffer with cursor
                value_str = self.edit_buffer + "_"
                value_color = self.EDIT_CURSOR_COLOR
            else:
                value_str = str(data[field])
                value_color = self.MODIFIED_COLOR if is_modified else self.TEXT_COLOR

            value_surf = self.font.render(value_str, True, value_color)
            self.screen.blit(value_surf, (panel_rect.x + 150, y))

            y += 25

        y += 10  # Spacer

        # Display additional info
        if data['Image']:
            label_surf = self.font.render("Actual Size:", True, self.LABEL_COLOR)
            self.screen.blit(label_surf, (panel_rect.x + 15, y))
            value_surf = self.font.render(
                f"{data['Image'].get_width()} x {data['Image'].get_height()}",
                True, self.TEXT_COLOR
            )
            self.screen.blit(value_surf, (panel_rect.x + 150, y))
            y += 25

        # Show edit instructions
        y += 15
        instructions = [
            "Type value + Enter to apply",
            "Space to toggle Flip",
            "S to save, Z to undo",
        ]
        for line in instructions:
            help_surf = self.font_small.render(line, True, self.HELP_COLOR)
            self.screen.blit(help_surf, (panel_rect.x + 15, y))
            y += 20

    def draw_help_bar(self):
        """Draw the help bar at the bottom."""
        help_rect = pg.Rect(10, 445, 1030, 45)
        pg.draw.rect(self.screen, self.PANEL_COLOR, help_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, help_rect, 1)

        if self.grid_settings_mode:
            help_text = "[Arrows] Navigate  [Space] Toggle  [A] All  [N] None  [ESC] Done"
        elif self.edit_mode:
            help_text = "[W/S] Field  [A/D] Tile  [Arrows] Blit Pos  [0-9] Value  [Enter] Apply  [Space] Flip  [F2] Save  [Z] Undo  [ESC] Exit"
        else:
            help_text = "[A/D] Prev/Next  [P] Picker  [T] Sprite  [E] Edit  [G] Grid  [F] Filter  [F5] Reload  [ESC] Quit"

        help_surf = self.font_small.render(help_text, True, self.HELP_COLOR)
        self.screen.blit(help_surf, (help_rect.centerx - help_surf.get_width() // 2, help_rect.y + 15))


if __name__ == "__main__":
    viewer = TileViewer()
    viewer.run()
