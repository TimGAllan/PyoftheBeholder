"""
Sprite Viewer Tool

Interactive pygame-based tool to browse sprites within wallset images.
Select an image file, then browse through all sprites defined in that image.

Controls:
    File Selection:
        Up/Down         - Navigate file list
        Enter           - Select file and view sprites
        ESC             - Quit

    Sprite Browsing:
        Up/Down         - Previous/Next sprite
        Home/End        - Jump to first/last sprite
        Page Up/Down    - Jump 10 sprites
        +/- or Scroll   - Zoom in/out
        Click+Drag      - Pan the sprite sheet
        P               - Enter pan mode (arrows to pan, ESC to exit)
        R               - Reset zoom and pan
        S               - Toggle show all sprites (cyan rectangles)
        B               - Back to file selection
        Enter           - Enter edit mode
        N               - Create new sprite (select area on image)
        Delete          - Delete current sprite (with confirmation)
        ESC             - Quit

    Delete Confirmation:
        Y               - Confirm deletion
        N/ESC           - Cancel deletion

    Create Mode (N):
        Click+Drag      - Select area for new sprite
        ESC             - Cancel create mode
        (Releasing mouse creates sprite with auto-generated name)

    Edit Mode:
        Up/Down         - Navigate fields (Name, Position, Size)
        Enter           - Edit selected field
        F2              - Save changes
        ESC             - Exit edit mode (or cancel field edit)

    Editing Name:
        Type            - Enter text
        Backspace       - Delete character
        Enter           - Confirm name
        ESC             - Cancel edit

    Editing Position/Size:
        Left/Right      - Adjust X / Width
        Up/Down         - Adjust Y / Height
        Enter           - Confirm
        ESC             - Cancel edit
"""

import pygame as pg
import pandas as pd
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from src.utils import SCALE_FACTOR


class SpriteViewer:
    """Interactive sprite viewer for browsing sprites within wallset images."""

    # Colors
    BG_COLOR = (40, 40, 50)
    PANEL_COLOR = (50, 50, 60)
    BORDER_COLOR = (80, 80, 100)
    TEXT_COLOR = (220, 220, 220)
    LABEL_COLOR = (150, 150, 170)
    HIGHLIGHT_COLOR = (100, 150, 200)
    HELP_COLOR = (120, 120, 140)
    SPRITE_RECT_COLOR = (255, 0, 0)  # Red for sprite bounds
    EDIT_HIGHLIGHT_COLOR = (80, 100, 140)
    EDIT_CURSOR_COLOR = (200, 200, 100)
    MODIFIED_COLOR = (255, 180, 100)  # Orange for modified values
    EDIT_ACTIVE_COLOR = (100, 180, 100)  # Green for active field

    # Edit mode field names
    EDIT_FIELDS = ['Name', 'Position', 'Size']

    def __init__(self):
        pg.init()
        self.window_width = 1600
        self.window_height = 850
        self.screen = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        pg.display.set_caption("Sprite Viewer")
        self.font = pg.font.SysFont("Consolas", 16)
        self.font_small = pg.font.SysFont("Consolas", 14)
        self.font_large = pg.font.SysFont("Consolas", 20)
        self.clock = pg.time.Clock()

        # Load data
        print("Loading data...")
        self.image_files = pd.read_csv('data/imageFiles.csv')
        self.sprites_df = pd.read_csv('data/sprites.csv')

        # State
        self.mode = 'file_select'  # 'file_select' or 'sprite_browse'
        self.file_cursor = 0
        self.file_scroll_offset = 0

        # Sprite browsing state
        self.current_file = None
        self.current_image = None
        self.filtered_sprites = []
        self.sprite_index = 0

        # Zoom and pan
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.pan_mode = False  # True when arrow keys pan instead of navigate
        self.dragging = False  # True when mouse is dragging to pan
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_start_pan_x = 0
        self.drag_start_pan_y = 0

        # Edit mode state
        self.edit_mode = False
        self.edit_field_index = 0  # 0=Name, 1=Position, 2=Size
        self.editing_field = False  # True when actively editing a field value
        self.edit_text = ""  # For text input (name editing)
        self.edit_cursor_pos = 0  # Cursor position in text
        self.pending_edits = {}  # {sprite_index: {'SpriteName': ..., 'Xpos': ..., etc}}
        self.edit_original_value = None  # Store original value for cancel

        # Delete confirmation state
        self.delete_confirm_pending = False

        # Create sprite mode state
        self.create_mode = False
        self.selection_active = False
        self.selection_start = None  # (x, y) in image coordinates
        self.selection_end = None  # (x, y) in image coordinates

        # Show all sprites toggle
        self.show_all_sprites = False

        # Load tiles.csv for name updates
        self.tiles_df = pd.read_csv('data/tiles.csv')

        print(f"Loaded {len(self.image_files)} image files, {len(self.sprites_df)} sprites")

    def run(self):
        """Main loop."""
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.VIDEORESIZE:
                    self.window_width = event.w
                    self.window_height = event.h
                    self.screen = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_mouse_down(event.pos)
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.create_mode and self.selection_active:
                            self.complete_sprite_selection()
                        self.dragging = False
                        self.selection_active = False
                elif event.type == pg.MOUSEMOTION:
                    if self.dragging or (self.create_mode and self.selection_active):
                        self.handle_mouse_drag(event.pos)
                elif event.type == pg.MOUSEWHEEL:
                    self.handle_mouse_wheel(event.y, pg.mouse.get_pos())
                elif event.type == pg.KEYDOWN:
                    if self.mode == 'file_select':
                        running = self.handle_file_select_key(event.key)
                    elif self.create_mode:
                        running = self.handle_create_mode_key(event.key)
                    elif self.editing_field:
                        running = self.handle_field_edit_key(event.key, event.unicode)
                    elif self.edit_mode:
                        running = self.handle_edit_mode_key(event.key)
                    elif self.pan_mode:
                        running = self.handle_pan_mode_key(event.key)
                    else:
                        running = self.handle_sprite_browse_key(event.key)

            self.draw()
            pg.display.flip()
            self.clock.tick(30)

        pg.quit()

    def handle_file_select_key(self, key):
        """Handle keyboard input in file selection mode."""
        total_files = len(self.image_files)
        visible_rows = max(1, (self.window_height - 170) // 30)

        if key == pg.K_ESCAPE:
            return False
        elif key in (pg.K_UP, pg.K_w):
            self.file_cursor = max(0, self.file_cursor - 1)
            self._adjust_file_scroll()
        elif key in (pg.K_DOWN, pg.K_s):
            self.file_cursor = min(total_files - 1, self.file_cursor + 1)
            self._adjust_file_scroll()
        elif key == pg.K_PAGEUP:
            self.file_cursor = max(0, self.file_cursor - visible_rows)
            self._adjust_file_scroll()
        elif key == pg.K_PAGEDOWN:
            self.file_cursor = min(total_files - 1, self.file_cursor + visible_rows)
            self._adjust_file_scroll()
        elif key == pg.K_HOME:
            self.file_cursor = 0
            self._adjust_file_scroll()
        elif key == pg.K_END:
            self.file_cursor = total_files - 1
            self._adjust_file_scroll()
        elif key in (pg.K_RETURN, pg.K_SPACE):
            self.select_file()

        return True

    def _adjust_file_scroll(self):
        """Adjust scroll offset to keep cursor visible."""
        visible_rows = max(1, (self.window_height - 170) // 30)  # Dynamic row count
        if self.file_cursor < self.file_scroll_offset:
            self.file_scroll_offset = self.file_cursor
        elif self.file_cursor >= self.file_scroll_offset + visible_rows:
            self.file_scroll_offset = self.file_cursor - visible_rows + 1

    def select_file(self):
        """Select the current file and load its image and sprites."""
        if len(self.image_files) == 0:
            return

        self.current_file = self.image_files.iloc[self.file_cursor]['File']

        # Load the image
        image_path = os.path.join('assets', 'Environments', self.current_file)
        if os.path.exists(image_path):
            self.current_image = pg.image.load(image_path).convert()
            # Don't scale - show at original size for precise sprite viewing
        else:
            print(f"Image not found: {image_path}")
            return

        # Filter sprites for this file and sort alphabetically
        self.filtered_sprites = self.sprites_df[
            self.sprites_df['File'] == self.current_file
        ].sort_values('SpriteName').reset_index(drop=True)

        self.sprite_index = 0
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.mode = 'sprite_browse'

        print(f"Loaded {self.current_file}: {len(self.filtered_sprites)} sprites")

    def handle_sprite_browse_key(self, key):
        """Handle keyboard input in sprite browsing mode."""
        total_sprites = len(self.filtered_sprites)

        # Handle delete confirmation
        if self.delete_confirm_pending:
            if key == pg.K_y:
                self.delete_current_sprite()
                self.delete_confirm_pending = False
            elif key in (pg.K_n, pg.K_ESCAPE):
                self.delete_confirm_pending = False
                print("Delete cancelled.")
            return True

        if key == pg.K_ESCAPE:
            return False
        elif key == pg.K_DELETE:
            # Initiate delete confirmation
            if len(self.filtered_sprites) > 0:
                self.delete_confirm_pending = True
        elif key == pg.K_n:
            # Enter create sprite mode
            if self.current_image:
                self.create_mode = True
                self.selection_active = False
                self.selection_start = None
                self.selection_end = None
                print("Create mode: Click and drag on the sprite sheet to select an area.")
        elif key == pg.K_s:
            # Toggle show all sprites
            self.show_all_sprites = not self.show_all_sprites
            status = "ON" if self.show_all_sprites else "OFF"
            print(f"Show all sprites: {status}")
        elif key == pg.K_b:
            # Back to file selection
            self.mode = 'file_select'
            self.current_image = None
            self.filtered_sprites = []
        elif key == pg.K_RETURN:
            # Enter edit mode
            if len(self.filtered_sprites) > 0:
                self.edit_mode = True
                self.edit_field_index = 0
        elif key == pg.K_p:
            # Enter pan mode
            self.pan_mode = True
        elif key == pg.K_UP:
            self.sprite_index = max(0, self.sprite_index - 1)
        elif key == pg.K_DOWN:
            self.sprite_index = min(total_sprites - 1, self.sprite_index + 1)
        elif key == pg.K_HOME:
            self.sprite_index = 0
        elif key == pg.K_END:
            self.sprite_index = total_sprites - 1
        elif key == pg.K_PAGEUP:
            self.sprite_index = max(0, self.sprite_index - 10)
        elif key == pg.K_PAGEDOWN:
            self.sprite_index = min(total_sprites - 1, self.sprite_index + 10)
        elif key in (pg.K_PLUS, pg.K_EQUALS, pg.K_KP_PLUS):
            self.zoom = min(8.0, self.zoom * 1.5)
        elif key in (pg.K_MINUS, pg.K_KP_MINUS):
            self.zoom = max(0.25, self.zoom / 1.5)
        elif key == pg.K_r:
            self.zoom = 1.0
            self.pan_x = 0
            self.pan_y = 0

        return True

    def handle_pan_mode_key(self, key):
        """Handle keyboard input in pan mode."""
        if key == pg.K_ESCAPE:
            # Exit pan mode
            self.pan_mode = False
        elif key == pg.K_LEFT:
            self.pan_x += 50
        elif key == pg.K_RIGHT:
            self.pan_x -= 50
        elif key == pg.K_UP:
            self.pan_y += 50
        elif key == pg.K_DOWN:
            self.pan_y -= 50
        elif key == pg.K_r:
            self.zoom = 1.0
            self.pan_x = 0
            self.pan_y = 0
        elif key in (pg.K_PLUS, pg.K_EQUALS, pg.K_KP_PLUS):
            self.zoom = min(8.0, self.zoom * 1.5)
        elif key in (pg.K_MINUS, pg.K_KP_MINUS):
            self.zoom = max(0.25, self.zoom / 1.5)
        elif key == pg.K_p:
            # Toggle pan mode off
            self.pan_mode = False

        return True

    def get_image_panel_rect(self):
        """Calculate the current image panel rectangle."""
        META_PANEL_WIDTH = 570
        LIST_PANEL_WIDTH = 290
        panel_height = self.window_height - 120
        image_panel_width = self.window_width - META_PANEL_WIDTH - LIST_PANEL_WIDTH - 40
        return pg.Rect(10, 60, image_panel_width, panel_height)

    def handle_mouse_down(self, pos):
        """Handle mouse button down - start dragging if in image panel."""
        if self.mode != 'sprite_browse':
            return

        image_panel = self.get_image_panel_rect()
        if image_panel.collidepoint(pos):
            if self.create_mode:
                # Start selection for new sprite
                img_coords = self.screen_to_image_coords(pos)
                if img_coords:
                    self.selection_active = True
                    self.selection_start = img_coords
                    self.selection_end = img_coords
            else:
                self.dragging = True
                self.drag_start_x = pos[0]
                self.drag_start_y = pos[1]
                self.drag_start_pan_x = self.pan_x
                self.drag_start_pan_y = self.pan_y

    def handle_mouse_drag(self, pos):
        """Handle mouse drag - update pan position or selection."""
        if self.create_mode and self.selection_active:
            # Update selection end point
            img_coords = self.screen_to_image_coords(pos)
            if img_coords:
                self.selection_end = img_coords
            return

        if not self.dragging:
            return

        dx = pos[0] - self.drag_start_x
        dy = pos[1] - self.drag_start_y
        self.pan_x = self.drag_start_pan_x + dx
        self.pan_y = self.drag_start_pan_y + dy

    def handle_mouse_wheel(self, direction, pos):
        """Handle mouse wheel - zoom in/out when over image panel."""
        if self.mode != 'sprite_browse':
            return

        image_panel = self.get_image_panel_rect()
        if image_panel.collidepoint(pos):
            if direction > 0:  # Scroll up - zoom in
                self.zoom = min(8.0, self.zoom * 1.25)
            elif direction < 0:  # Scroll down - zoom out
                self.zoom = max(0.25, self.zoom / 1.25)

    def screen_to_image_coords(self, screen_pos):
        """Convert screen coordinates to image coordinates."""
        if not self.current_image:
            return None

        image_panel = self.get_image_panel_rect()
        clip_rect = pg.Rect(image_panel.x + 5, image_panel.y + 5,
                            image_panel.width - 10, image_panel.height - 10)

        # Calculate image position on screen
        img_w = int(self.current_image.get_width() * self.zoom)
        img_h = int(self.current_image.get_height() * self.zoom)
        img_x = clip_rect.x + (clip_rect.width - img_w) // 2 + self.pan_x
        img_y = clip_rect.y + (clip_rect.height - img_h) // 2 + self.pan_y

        # Convert screen position to image position
        rel_x = screen_pos[0] - img_x
        rel_y = screen_pos[1] - img_y

        # Convert to original image coordinates (before zoom)
        img_coord_x = int(rel_x / self.zoom)
        img_coord_y = int(rel_y / self.zoom)

        # Clamp to image bounds
        img_coord_x = max(0, min(img_coord_x, self.current_image.get_width() - 1))
        img_coord_y = max(0, min(img_coord_y, self.current_image.get_height() - 1))

        return (img_coord_x, img_coord_y)

    def image_to_screen_coords(self, img_coords):
        """Convert image coordinates to screen coordinates."""
        if not self.current_image:
            return None

        image_panel = self.get_image_panel_rect()
        clip_rect = pg.Rect(image_panel.x + 5, image_panel.y + 5,
                            image_panel.width - 10, image_panel.height - 10)

        # Calculate image position on screen
        img_w = int(self.current_image.get_width() * self.zoom)
        img_h = int(self.current_image.get_height() * self.zoom)
        img_x = clip_rect.x + (clip_rect.width - img_w) // 2 + self.pan_x
        img_y = clip_rect.y + (clip_rect.height - img_h) // 2 + self.pan_y

        # Convert image position to screen position
        screen_x = img_x + int(img_coords[0] * self.zoom)
        screen_y = img_y + int(img_coords[1] * self.zoom)

        return (screen_x, screen_y)

    def handle_create_mode_key(self, key):
        """Handle keyboard input in create sprite mode."""
        if key == pg.K_ESCAPE:
            # Cancel create mode
            self.create_mode = False
            self.selection_active = False
            self.selection_start = None
            self.selection_end = None
            print("Create mode cancelled.")
        return True

    def complete_sprite_selection(self):
        """Complete the sprite selection and create the new sprite."""
        if not self.selection_start or not self.selection_end:
            return

        # Calculate the rectangle (handle any drag direction)
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end

        xpos = min(x1, x2)
        ypos = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        # Minimum size check
        if width < 1 or height < 1:
            print("Selection too small. Please select a larger area.")
            return

        # Generate placeholder name based on filename and coordinates
        # Remove extension from filename and use as prefix
        file_base = os.path.splitext(self.current_file)[0]
        # Replace hyphens and spaces with underscores for consistency
        file_base = file_base.replace('-', '_').replace(' ', '_')
        sprite_name = f"{file_base}_{xpos}_{ypos}_{width}_{height}"

        # Check if sprite name already exists
        if sprite_name in self.sprites_df['SpriteName'].values:
            print(f"Sprite '{sprite_name}' already exists!")
            return

        # Create new sprite entry
        new_sprite = pd.DataFrame([{
            'SpriteName': sprite_name,
            'File': self.current_file,
            'Xpos': xpos,
            'Ypos': ypos,
            'Width': width,
            'Height': height
        }])

        # Add to dataframe and save
        self.sprites_df = pd.concat([self.sprites_df, new_sprite], ignore_index=True)
        self.sprites_df.to_csv('data/sprites.csv', index=False)

        # Update filtered sprites (sorted alphabetically)
        self.filtered_sprites = self.sprites_df[
            self.sprites_df['File'] == self.current_file
        ].sort_values('SpriteName').reset_index(drop=True)

        # Navigate to the new sprite
        new_index = self.filtered_sprites[
            self.filtered_sprites['SpriteName'] == sprite_name
        ].index
        if len(new_index) > 0:
            self.sprite_index = new_index[0]

        print(f"Created sprite '{sprite_name}' at ({xpos}, {ypos}) size {width}x{height}")

        # Exit create mode
        self.create_mode = False
        self.selection_start = None
        self.selection_end = None

    def handle_edit_mode_key(self, key):
        """Handle keyboard input in edit mode (not actively editing a field)."""
        if key == pg.K_ESCAPE:
            # Exit edit mode
            self.edit_mode = False
            self.edit_field_index = 0
        elif key == pg.K_UP:
            self.edit_field_index = max(0, self.edit_field_index - 1)
        elif key == pg.K_DOWN:
            self.edit_field_index = min(len(self.EDIT_FIELDS) - 1, self.edit_field_index + 1)
        elif key == pg.K_RETURN:
            # Start editing the selected field
            self.start_field_edit()
        elif key == pg.K_F2:
            # Save changes
            self.save_changes()
        elif key == pg.K_a:
            # Previous sprite (keep edit mode)
            if self.sprite_index > 0:
                self.sprite_index -= 1
        elif key == pg.K_d:
            # Next sprite (keep edit mode)
            if self.sprite_index < len(self.filtered_sprites) - 1:
                self.sprite_index += 1

        return True

    def start_field_edit(self):
        """Begin editing the currently selected field."""
        if len(self.filtered_sprites) == 0:
            return

        self.editing_field = True
        sprite = self.get_current_sprite_data()

        if self.edit_field_index == 0:  # Name
            self.edit_text = sprite['SpriteName']
            self.edit_cursor_pos = len(self.edit_text)
            self.edit_original_value = sprite['SpriteName']
        elif self.edit_field_index == 1:  # Position
            self.edit_original_value = (sprite['Xpos'], sprite['Ypos'])
        elif self.edit_field_index == 2:  # Size
            self.edit_original_value = (sprite['Width'], sprite['Height'])

    def handle_field_edit_key(self, key, unicode_char):
        """Handle keyboard input while actively editing a field."""
        if self.edit_field_index == 0:  # Name editing (text input)
            return self.handle_name_edit_key(key, unicode_char)
        else:  # Position or Size editing (arrow keys)
            return self.handle_numeric_edit_key(key)

    def handle_name_edit_key(self, key, unicode_char):
        """Handle text input for name editing."""
        if key == pg.K_ESCAPE:
            # Cancel - restore original value
            self.editing_field = False
            self.edit_text = ""
        elif key == pg.K_RETURN:
            # Confirm the new name
            if self.edit_text.strip():
                self.set_pending_edit('SpriteName', self.edit_text.strip())
            self.editing_field = False
            self.edit_text = ""
        elif key == pg.K_BACKSPACE:
            if self.edit_cursor_pos > 0:
                self.edit_text = self.edit_text[:self.edit_cursor_pos - 1] + self.edit_text[self.edit_cursor_pos:]
                self.edit_cursor_pos -= 1
        elif key == pg.K_DELETE:
            if self.edit_cursor_pos < len(self.edit_text):
                self.edit_text = self.edit_text[:self.edit_cursor_pos] + self.edit_text[self.edit_cursor_pos + 1:]
        elif key == pg.K_LEFT:
            self.edit_cursor_pos = max(0, self.edit_cursor_pos - 1)
        elif key == pg.K_RIGHT:
            self.edit_cursor_pos = min(len(self.edit_text), self.edit_cursor_pos + 1)
        elif key == pg.K_HOME:
            self.edit_cursor_pos = 0
        elif key == pg.K_END:
            self.edit_cursor_pos = len(self.edit_text)
        elif unicode_char and unicode_char.isprintable() and len(unicode_char) == 1:
            # Insert character at cursor position
            self.edit_text = self.edit_text[:self.edit_cursor_pos] + unicode_char + self.edit_text[self.edit_cursor_pos:]
            self.edit_cursor_pos += 1

        return True

    def handle_numeric_edit_key(self, key):
        """Handle arrow key input for position/size editing."""
        if key == pg.K_ESCAPE:
            # Cancel - restore original values
            if self.edit_field_index == 1:  # Position
                x, y = self.edit_original_value
                self.set_pending_edit('Xpos', x)
                self.set_pending_edit('Ypos', y)
            elif self.edit_field_index == 2:  # Size
                w, h = self.edit_original_value
                self.set_pending_edit('Width', w)
                self.set_pending_edit('Height', h)
            self.editing_field = False
        elif key == pg.K_RETURN:
            # Confirm the edit
            self.editing_field = False
        elif key == pg.K_LEFT:
            if self.edit_field_index == 1:  # Position: decrease X
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Xpos', max(0, sprite['Xpos'] - 1))
            elif self.edit_field_index == 2:  # Size: decrease Width
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Width', max(1, sprite['Width'] - 1))
        elif key == pg.K_RIGHT:
            if self.edit_field_index == 1:  # Position: increase X
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Xpos', sprite['Xpos'] + 1)
            elif self.edit_field_index == 2:  # Size: increase Width
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Width', sprite['Width'] + 1)
        elif key == pg.K_UP:
            if self.edit_field_index == 1:  # Position: decrease Y
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Ypos', max(0, sprite['Ypos'] - 1))
            elif self.edit_field_index == 2:  # Size: decrease Height
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Height', max(1, sprite['Height'] - 1))
        elif key == pg.K_DOWN:
            if self.edit_field_index == 1:  # Position: increase Y
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Ypos', sprite['Ypos'] + 1)
            elif self.edit_field_index == 2:  # Size: increase Height
                sprite = self.get_current_sprite_data()
                self.set_pending_edit('Height', sprite['Height'] + 1)

        return True

    def get_current_sprite_data(self):
        """Get current sprite data with any pending edits applied."""
        if len(self.filtered_sprites) == 0:
            return None

        sprite = self.filtered_sprites.iloc[self.sprite_index].copy()

        # Apply pending edits for this sprite
        if self.sprite_index in self.pending_edits:
            for key, value in self.pending_edits[self.sprite_index].items():
                sprite[key] = value

        return sprite

    def set_pending_edit(self, field, value):
        """Set a pending edit for the current sprite."""
        if self.sprite_index not in self.pending_edits:
            self.pending_edits[self.sprite_index] = {}
        self.pending_edits[self.sprite_index][field] = value

    def has_pending_edits(self):
        """Check if there are any pending edits."""
        return len(self.pending_edits) > 0

    def save_changes(self):
        """Save pending edits to CSV files."""
        if not self.has_pending_edits():
            print("No changes to save.")
            return

        # Reload dataframes to ensure fresh data
        sprites_df = pd.read_csv('data/sprites.csv')
        tiles_df = pd.read_csv('data/tiles.csv')

        changes_made = 0

        for sprite_idx, edits in self.pending_edits.items():
            # Get the original sprite name from filtered_sprites
            original_sprite = self.filtered_sprites.iloc[sprite_idx]
            original_name = original_sprite['SpriteName']

            # Find the row in the full sprites_df
            mask = sprites_df['SpriteName'] == original_name

            if not mask.any():
                print(f"Warning: Could not find sprite '{original_name}' in sprites.csv")
                continue

            # Check if name is being changed
            new_name = edits.get('SpriteName', original_name)

            if new_name != original_name:
                # Update name in sprites.csv
                sprites_df.loc[mask, 'SpriteName'] = new_name

                # Update name in tiles.csv
                tiles_mask = tiles_df['SpriteName'] == original_name
                if tiles_mask.any():
                    tiles_df.loc[tiles_mask, 'SpriteName'] = new_name
                    print(f"Updated sprite name in tiles.csv: {original_name} -> {new_name}")

                # Update the filtered_sprites reference
                self.filtered_sprites.at[sprite_idx, 'SpriteName'] = new_name

            # Update position/size in sprites.csv
            for field in ['Xpos', 'Ypos', 'Width', 'Height']:
                if field in edits:
                    sprites_df.loc[mask, field] = edits[field]
                    # Also update filtered_sprites
                    self.filtered_sprites.at[sprite_idx, field] = edits[field]

            changes_made += 1

        # Save the files
        sprites_df.to_csv('data/sprites.csv', index=False)
        tiles_df.to_csv('data/tiles.csv', index=False)

        # Clear pending edits
        self.pending_edits.clear()

        # Reload the dataframes
        self.sprites_df = sprites_df
        self.tiles_df = tiles_df

        print(f"Saved changes to {changes_made} sprite(s).")

    def delete_current_sprite(self):
        """Delete the current sprite from sprites.csv."""
        if len(self.filtered_sprites) == 0:
            print("No sprite to delete.")
            return

        # Get the sprite to delete
        sprite = self.filtered_sprites.iloc[self.sprite_index]
        sprite_name = sprite['SpriteName']

        # Check if sprite is referenced in tiles.csv
        tiles_df = pd.read_csv('data/tiles.csv')
        tiles_using_sprite = tiles_df[tiles_df['SpriteName'] == sprite_name]

        if len(tiles_using_sprite) > 0:
            print(f"WARNING: Sprite '{sprite_name}' is referenced in {len(tiles_using_sprite)} tile(s) in tiles.csv!")
            print("These tiles will have invalid sprite references after deletion:")
            for _, tile in tiles_using_sprite.head(5).iterrows():
                print(f"  - {tile['Environment']}/{tile['dungeon_map_code']}/{tile['Panel']}")
            if len(tiles_using_sprite) > 5:
                print(f"  ... and {len(tiles_using_sprite) - 5} more")

        # Delete from sprites.csv
        sprites_df = pd.read_csv('data/sprites.csv')
        mask = sprites_df['SpriteName'] == sprite_name

        if not mask.any():
            print(f"Error: Could not find sprite '{sprite_name}' in sprites.csv")
            return

        sprites_df = sprites_df[~mask]
        sprites_df.to_csv('data/sprites.csv', index=False)

        # Clear any pending edits for this sprite
        if self.sprite_index in self.pending_edits:
            del self.pending_edits[self.sprite_index]

        # Update pending_edits indices (shift down indices above deleted)
        new_pending_edits = {}
        for idx, edits in self.pending_edits.items():
            if idx > self.sprite_index:
                new_pending_edits[idx - 1] = edits
            else:
                new_pending_edits[idx] = edits
        self.pending_edits = new_pending_edits

        # Reload sprites dataframe
        self.sprites_df = sprites_df

        # Update filtered sprites (sorted alphabetically)
        self.filtered_sprites = self.sprites_df[
            self.sprites_df['File'] == self.current_file
        ].sort_values('SpriteName').reset_index(drop=True)

        # Adjust sprite index if needed
        if len(self.filtered_sprites) == 0:
            self.sprite_index = 0
            print(f"Deleted sprite '{sprite_name}'. No more sprites in this file.")
        else:
            if self.sprite_index >= len(self.filtered_sprites):
                self.sprite_index = len(self.filtered_sprites) - 1
            print(f"Deleted sprite '{sprite_name}'. {len(self.filtered_sprites)} sprites remaining.")

    def draw(self):
        """Draw the viewer interface."""
        self.screen.fill(self.BG_COLOR)

        if self.mode == 'file_select':
            self.draw_file_selection()
        else:
            self.draw_sprite_browser()

        pg.display.flip()

    def draw_file_selection(self):
        """Draw the file selection screen."""
        # Calculate dynamic sizes
        panel_width = self.window_width - 20
        panel_height = self.window_height - 120  # Leave room for title and help bar

        # Title
        title_rect = pg.Rect(10, 10, panel_width, 40)
        pg.draw.rect(self.screen, self.PANEL_COLOR, title_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, title_rect, 1)

        title = self.font_large.render("Select Image File", True, self.TEXT_COLOR)
        self.screen.blit(title, (20, 18))

        # File list panel
        list_rect = pg.Rect(10, 60, panel_width, panel_height)
        pg.draw.rect(self.screen, self.PANEL_COLOR, list_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, list_rect, 1)

        # Column headers
        header_y = 70
        col_file = 30
        col_sprites = 500

        headers = [
            (col_file, "File"),
            (col_sprites, "Sprites"),
        ]
        for col_x, header in headers:
            header_surf = self.font.render(header, True, self.LABEL_COLOR)
            self.screen.blit(header_surf, (col_x, header_y))

        # Separator
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (20, header_y + 25), (self.window_width - 20, header_y + 25))

        # File list
        list_y = header_y + 35
        row_height = 30
        visible_rows = (self.window_height - 170) // row_height  # Dynamic row count

        for i in range(visible_rows):
            file_idx = self.file_scroll_offset + i
            if file_idx >= len(self.image_files):
                break

            row = self.image_files.iloc[file_idx]
            file_name = row['File']
            row_y = list_y + i * row_height
            is_selected = (file_idx == self.file_cursor)

            # Selection highlight
            if is_selected:
                highlight_rect = pg.Rect(20, row_y - 2, self.window_width - 40, row_height)
                pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

            # Count sprites for this file
            sprite_count = len(self.sprites_df[self.sprites_df['File'] == file_name])

            # Draw text
            text_color = self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR
            file_surf = self.font.render(str(file_name), True, text_color)
            count_surf = self.font.render(f"{sprite_count} sprites", True,
                                          self.LABEL_COLOR if not is_selected else text_color)

            self.screen.blit(file_surf, (col_file, row_y))
            self.screen.blit(count_surf, (col_sprites, row_y))

        # Scrollbar
        scrollbar_x = self.window_width - 30
        scrollbar_y = list_y
        visible_rows = (self.window_height - 170) // row_height  # Dynamic row count
        scrollbar_h = visible_rows * row_height
        pg.draw.rect(self.screen, self.BORDER_COLOR, (scrollbar_x, scrollbar_y, 8, scrollbar_h), 1)

        if len(self.image_files) > visible_rows:
            thumb_h = max(20, scrollbar_h * visible_rows // len(self.image_files))
            thumb_y = scrollbar_y + (scrollbar_h - thumb_h) * self.file_scroll_offset // (
                len(self.image_files) - visible_rows)
            pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR, (scrollbar_x + 1, thumb_y, 6, thumb_h))

        # Help bar
        help_y = self.window_height - 50
        help_rect = pg.Rect(10, help_y, self.window_width - 20, 40)
        pg.draw.rect(self.screen, self.PANEL_COLOR, help_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, help_rect, 1)

        help_text = "[Up/Down] Navigate  [Enter] Select  [ESC] Quit"
        help_surf = self.font_small.render(help_text, True, self.HELP_COLOR)
        self.screen.blit(help_surf, (help_rect.centerx - help_surf.get_width() // 2, help_y + 12))

    def draw_sprite_browser(self):
        """Draw the sprite browsing screen."""
        # Fixed panel widths
        META_PANEL_WIDTH = 570
        LIST_PANEL_WIDTH = 290
        PANEL_GAP = 10

        # Calculate dynamic sizes
        panel_height = self.window_height - 120  # Leave room for title and help bar
        image_panel_width = self.window_width - META_PANEL_WIDTH - LIST_PANEL_WIDTH - 40  # 40 for gaps

        # Title bar
        title_rect = pg.Rect(10, 10, self.window_width - 20, 40)
        pg.draw.rect(self.screen, self.PANEL_COLOR, title_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, title_rect, 1)

        sprite_count = len(self.filtered_sprites)
        title = f"Sprite Viewer - {self.current_file} - {self.sprite_index + 1}/{sprite_count} sprites"
        if self.create_mode:
            title += " [CREATE MODE]"
            title_color = (100, 255, 100)  # Green for create mode
        elif self.delete_confirm_pending:
            title += " [CONFIRM DELETE?]"
            title_color = (255, 100, 100)  # Red for delete warning
        elif self.has_pending_edits():
            title += " [UNSAVED]"
            title_color = self.MODIFIED_COLOR
        else:
            title_color = self.TEXT_COLOR
        title_surf = self.font_large.render(title, True, title_color)
        self.screen.blit(title_surf, (20, 18))

        # Zoom indicator and pan mode
        zoom_text = f"Zoom: {self.zoom:.1f}x"
        if self.pan_mode:
            zoom_text += "  [PAN MODE]"
        zoom_color = self.EDIT_ACTIVE_COLOR if self.pan_mode else self.LABEL_COLOR
        zoom_surf = self.font.render(zoom_text, True, zoom_color)
        self.screen.blit(zoom_surf, (self.window_width - 300, 22))

        # Image panel (left side) - grows with window
        image_panel_rect = pg.Rect(10, 60, image_panel_width, panel_height)
        pg.draw.rect(self.screen, self.PANEL_COLOR, image_panel_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, image_panel_rect, 1)

        # Draw the image with zoom and pan
        if self.current_image:
            self.draw_image_with_sprite_rect(image_panel_rect)

        # Metadata panel (middle) - fixed width
        meta_x = 10 + image_panel_width + PANEL_GAP
        meta_panel_rect = pg.Rect(meta_x, 60, META_PANEL_WIDTH, panel_height)
        pg.draw.rect(self.screen, self.PANEL_COLOR, meta_panel_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, meta_panel_rect, 1)

        self.draw_sprite_metadata(meta_panel_rect)

        # Sprite list panel (right side) - fixed width
        list_x = meta_x + META_PANEL_WIDTH + PANEL_GAP
        list_panel_rect = pg.Rect(list_x, 60, LIST_PANEL_WIDTH, panel_height)
        pg.draw.rect(self.screen, self.PANEL_COLOR, list_panel_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, list_panel_rect, 1)

        self.draw_sprite_list(list_panel_rect)

        # Help bar
        help_y = self.window_height - 50
        help_rect = pg.Rect(10, help_y, self.window_width - 20, 40)
        pg.draw.rect(self.screen, self.PANEL_COLOR, help_rect)
        pg.draw.rect(self.screen, self.BORDER_COLOR, help_rect, 1)

        # Context-sensitive help text
        if self.create_mode:
            if self.selection_start and self.selection_end:
                x1, y1 = self.selection_start
                x2, y2 = self.selection_end
                w, h = abs(x2 - x1), abs(y2 - y1)
                help_text = f"Selection: ({min(x1,x2)}, {min(y1,y2)}) {w}x{h}  [Click+Drag] Select area  [ESC] Cancel"
            else:
                help_text = "[Click+Drag] Select sprite area on the image  [ESC] Cancel"
        elif self.delete_confirm_pending:
            if len(self.filtered_sprites) > 0:
                sprite = self.get_current_sprite_data()
                sprite_name = sprite['SpriteName']
            else:
                sprite_name = "?"
            help_text = f"Delete '{sprite_name}'? [Y] Yes  [N/ESC] Cancel"
        elif self.editing_field:
            if self.edit_field_index == 0:  # Name
                help_text = "[Type] Enter text  [Backspace] Delete  [Enter] Confirm  [ESC] Cancel"
            else:  # Position or Size
                help_text = "[Left/Right] Adjust X/Width  [Up/Down] Adjust Y/Height  [Enter] Confirm  [ESC] Cancel"
        elif self.edit_mode:
            help_text = "[Up/Down] Select field  [Enter] Edit field  [A/D] Prev/Next sprite  [F2] Save  [ESC] Exit edit"
        elif self.pan_mode:
            help_text = "[Arrows] Pan  [+/-] Zoom  [R] Reset  [ESC] Exit pan mode"
        else:
            show_status = "ON" if self.show_all_sprites else "OFF"
            help_text = f"[Up/Down] Prev/Next  [Zoom/Pan]  [Enter] Edit  [N] New  [S] Show All ({show_status})  [Del]  [B] Back"

        help_surf = self.font_small.render(help_text, True, self.HELP_COLOR)
        self.screen.blit(help_surf, (help_rect.centerx - help_surf.get_width() // 2, help_y + 12))

    def draw_image_with_sprite_rect(self, panel_rect):
        """Draw the image with the current sprite highlighted."""
        # Create a clipping region
        clip_rect = pg.Rect(panel_rect.x + 5, panel_rect.y + 5,
                            panel_rect.width - 10, panel_rect.height - 10)

        # Calculate scaled image size
        img_w = int(self.current_image.get_width() * self.zoom)
        img_h = int(self.current_image.get_height() * self.zoom)

        # Scale the image
        if self.zoom != 1.0:
            scaled_image = pg.transform.scale(self.current_image, (img_w, img_h))
        else:
            scaled_image = self.current_image

        # Calculate position (centered with pan offset)
        img_x = clip_rect.x + (clip_rect.width - img_w) // 2 + self.pan_x
        img_y = clip_rect.y + (clip_rect.height - img_h) // 2 + self.pan_y

        # Draw checkerboard background
        self.draw_checkerboard(clip_rect.x, clip_rect.y, clip_rect.width, clip_rect.height)

        # Set clipping and draw image
        self.screen.set_clip(clip_rect)
        self.screen.blit(scaled_image, (img_x, img_y))

        # Draw all sprite rectangles in cyan if toggle is on
        if self.show_all_sprites and len(self.filtered_sprites) > 0:
            for idx in range(len(self.filtered_sprites)):
                # Skip the current sprite (it will be drawn in red)
                if idx == self.sprite_index and not self.create_mode:
                    continue
                sprite_row = self.filtered_sprites.iloc[idx]
                # Apply pending edits if any
                s_xpos = sprite_row['Xpos']
                s_ypos = sprite_row['Ypos']
                s_width = sprite_row['Width']
                s_height = sprite_row['Height']
                if idx in self.pending_edits:
                    s_xpos = self.pending_edits[idx].get('Xpos', s_xpos)
                    s_ypos = self.pending_edits[idx].get('Ypos', s_ypos)
                    s_width = self.pending_edits[idx].get('Width', s_width)
                    s_height = self.pending_edits[idx].get('Height', s_height)

                rect_x = img_x + int(s_xpos * self.zoom)
                rect_y = img_y + int(s_ypos * self.zoom)
                rect_w = int(s_width * self.zoom)
                rect_h = int(s_height * self.zoom)

                # Draw cyan rectangle with 3 pixel thickness
                pg.draw.rect(self.screen, (0, 255, 255),
                             (rect_x, rect_y, rect_w, rect_h), 3)

        # Draw current sprite rectangle if we have sprites (and not in create mode)
        if len(self.filtered_sprites) > 0 and not self.create_mode:
            # Use current sprite data with pending edits applied
            sprite = self.get_current_sprite_data()
            rect_x = img_x + int(sprite['Xpos'] * self.zoom)
            rect_y = img_y + int(sprite['Ypos'] * self.zoom)
            rect_w = int(sprite['Width'] * self.zoom)
            rect_h = int(sprite['Height'] * self.zoom)

            # Draw red rectangle with 3 pixel thickness
            pg.draw.rect(self.screen, self.SPRITE_RECT_COLOR,
                         (rect_x, rect_y, rect_w, rect_h), 3)

        # Draw selection rectangle in create mode
        if self.create_mode and self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            sel_x = img_x + int(min(x1, x2) * self.zoom)
            sel_y = img_y + int(min(y1, y2) * self.zoom)
            sel_w = int(abs(x2 - x1) * self.zoom)
            sel_h = int(abs(y2 - y1) * self.zoom)

            # Draw green selection rectangle
            pg.draw.rect(self.screen, (100, 255, 100),
                         (sel_x, sel_y, sel_w, sel_h), 2)
            # Draw corner markers
            marker_size = 6
            for cx, cy in [(sel_x, sel_y), (sel_x + sel_w, sel_y),
                           (sel_x, sel_y + sel_h), (sel_x + sel_w, sel_y + sel_h)]:
                pg.draw.rect(self.screen, (100, 255, 100),
                             (cx - marker_size // 2, cy - marker_size // 2,
                              marker_size, marker_size))

        # Reset clipping
        self.screen.set_clip(None)

        # Draw border around clip area
        pg.draw.rect(self.screen, self.BORDER_COLOR, clip_rect, 1)

    def draw_checkerboard(self, x, y, width, height, tile_size=16):
        """Draw a checkerboard pattern for transparency visualization."""
        colors = [(60, 60, 70), (70, 70, 80)]
        for row in range(0, height, tile_size):
            for col in range(0, width, tile_size):
                color = colors[(row // tile_size + col // tile_size) % 2]
                rect = pg.Rect(x + col, y + row,
                               min(tile_size, width - col),
                               min(tile_size, height - row))
                pg.draw.rect(self.screen, color, rect)

    def draw_sprite_metadata(self, panel_rect):
        """Draw the sprite metadata panel with details and preview."""
        if len(self.filtered_sprites) == 0:
            y = panel_rect.y + 15
            no_sprites = self.font.render("No sprites in this file", True, self.LABEL_COLOR)
            self.screen.blit(no_sprites, (panel_rect.x + 15, y))
            return

        # Get sprite data with pending edits applied
        sprite = self.get_current_sprite_data()

        # === TOP SECTION: Sprite Details ===
        y = panel_rect.y + 10

        # Panel title with edit mode indicator
        title_text = "Sprite Details"
        if self.edit_mode:
            title_text += " [EDIT MODE]"
            if self.has_pending_edits():
                title_text += " *"
        title = self.font.render(title_text, True,
                                 self.EDIT_ACTIVE_COLOR if self.edit_mode else self.TEXT_COLOR)
        self.screen.blit(title, (panel_rect.x + 15, y))
        y += 25

        # Separator
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_rect.x + 10, y), (panel_rect.x + panel_rect.width - 10, y))
        y += 15

        # Check if this sprite has pending edits
        has_edits = self.sprite_index in self.pending_edits

        # Editable fields: Name (0), Position (1), Size (2)
        # Non-editable: File, Area

        # Name field (editable, index 0)
        field_idx = 0
        is_selected = self.edit_mode and self.edit_field_index == field_idx
        is_editing = is_selected and self.editing_field
        is_modified = has_edits and 'SpriteName' in self.pending_edits[self.sprite_index]

        if is_selected:
            highlight_rect = pg.Rect(panel_rect.x + 10, y - 2, panel_rect.width - 20, 22)
            pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

        label_surf = self.font.render("Name:", True, self.LABEL_COLOR)
        self.screen.blit(label_surf, (panel_rect.x + 15, y))

        if is_editing:
            # Draw text input field
            self.draw_text_input(panel_rect.x + 100, y, panel_rect.width - 120)
        else:
            value_str = str(sprite['SpriteName'])
            if len(value_str) > 35:
                value_str = value_str[:32] + "..."
            text_color = self.MODIFIED_COLOR if is_modified else (
                self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR)
            value_surf = self.font.render(value_str, True, text_color)
            self.screen.blit(value_surf, (panel_rect.x + 100, y))
        y += 25

        # File field (not editable)
        label_surf = self.font.render("File:", True, self.LABEL_COLOR)
        self.screen.blit(label_surf, (panel_rect.x + 15, y))
        value_surf = self.font.render(str(sprite['File']), True, self.LABEL_COLOR)
        self.screen.blit(value_surf, (panel_rect.x + 100, y))
        y += 25

        # Position field (editable, index 1)
        field_idx = 1
        is_selected = self.edit_mode and self.edit_field_index == field_idx
        is_editing = is_selected and self.editing_field
        is_modified = has_edits and ('Xpos' in self.pending_edits[self.sprite_index] or
                                      'Ypos' in self.pending_edits[self.sprite_index])

        if is_selected:
            highlight_rect = pg.Rect(panel_rect.x + 10, y - 2, panel_rect.width - 20, 22)
            pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

        label_surf = self.font.render("Position:", True, self.LABEL_COLOR)
        self.screen.blit(label_surf, (panel_rect.x + 15, y))

        value_str = f"({sprite['Xpos']}, {sprite['Ypos']})"
        text_color = self.MODIFIED_COLOR if is_modified else (
            self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR)
        if is_editing:
            text_color = self.EDIT_ACTIVE_COLOR
            value_str += "  [Arrow keys to adjust]"
        value_surf = self.font.render(value_str, True, text_color)
        self.screen.blit(value_surf, (panel_rect.x + 100, y))
        y += 25

        # Size field (editable, index 2)
        field_idx = 2
        is_selected = self.edit_mode and self.edit_field_index == field_idx
        is_editing = is_selected and self.editing_field
        is_modified = has_edits and ('Width' in self.pending_edits[self.sprite_index] or
                                      'Height' in self.pending_edits[self.sprite_index])

        if is_selected:
            highlight_rect = pg.Rect(panel_rect.x + 10, y - 2, panel_rect.width - 20, 22)
            pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

        label_surf = self.font.render("Size:", True, self.LABEL_COLOR)
        self.screen.blit(label_surf, (panel_rect.x + 15, y))

        value_str = f"{sprite['Width']} x {sprite['Height']}"
        text_color = self.MODIFIED_COLOR if is_modified else (
            self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR)
        if is_editing:
            text_color = self.EDIT_ACTIVE_COLOR
            value_str += "  [Arrow keys to adjust]"
        value_surf = self.font.render(value_str, True, text_color)
        self.screen.blit(value_surf, (panel_rect.x + 100, y))
        y += 25

        # Area field (calculated, not editable)
        label_surf = self.font.render("Area:", True, self.LABEL_COLOR)
        self.screen.blit(label_surf, (panel_rect.x + 15, y))
        value_surf = self.font.render(f"{sprite['Width'] * sprite['Height']} px", True, self.LABEL_COLOR)
        self.screen.blit(value_surf, (panel_rect.x + 100, y))
        y += 25

        # === PREVIEW SECTION ===
        y += 10
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_rect.x + 10, y), (panel_rect.x + panel_rect.width - 10, y))
        y += 10

        preview_label = self.font.render("Preview (3x scale):", True, self.LABEL_COLOR)
        self.screen.blit(preview_label, (panel_rect.x + 15, y))
        y += 25

        # Extract and draw the sprite preview at SCALE_FACTOR (3x)
        try:
            sprite_rect = pg.Rect(
                int(sprite['Xpos']),
                int(sprite['Ypos']),
                int(sprite['Width']),
                int(sprite['Height'])
            )
            sprite_surface = self.current_image.subsurface(sprite_rect)

            # Scale preview by SCALE_FACTOR (3x)
            preview_w = int(sprite_surface.get_width() * SCALE_FACTOR)
            preview_h = int(sprite_surface.get_height() * SCALE_FACTOR)
            preview = pg.transform.scale(sprite_surface, (preview_w, preview_h))

            # Calculate preview area (fit within panel)
            max_preview_w = panel_rect.width - 30
            max_preview_h = panel_rect.height - y + panel_rect.y - 20

            # Draw preview background (sized to fit scaled sprite or max area)
            bg_w = min(preview_w + 10, max_preview_w)
            bg_h = min(preview_h + 10, max_preview_h)
            preview_bg = pg.Rect(panel_rect.x + 15, y, bg_w, bg_h)
            self.draw_checkerboard(preview_bg.x, preview_bg.y, preview_bg.width, preview_bg.height, 8)
            pg.draw.rect(self.screen, self.BORDER_COLOR, preview_bg, 1)

            # Clip and draw preview
            self.screen.set_clip(preview_bg)
            preview_x = preview_bg.x + 5
            preview_y = preview_bg.y + 5
            self.screen.blit(preview, (preview_x, preview_y))
            self.screen.set_clip(None)

            # Show scaled dimensions
            dim_y = preview_bg.y + preview_bg.height + 5
            dim_text = f"Scaled: {preview_w}x{preview_h} px"
            dim_surf = self.font_small.render(dim_text, True, self.LABEL_COLOR)
            self.screen.blit(dim_surf, (panel_rect.x + 15, dim_y))

        except Exception as e:
            error_surf = self.font_small.render(f"Error: {e}", True, (255, 100, 100))
            self.screen.blit(error_surf, (panel_rect.x + 15, y))

    def draw_text_input(self, x, y, max_width):
        """Draw a text input field with cursor."""
        # Draw text up to max width
        display_text = self.edit_text

        # Calculate cursor position in pixels
        text_before_cursor = display_text[:self.edit_cursor_pos]
        cursor_x_offset = self.font.size(text_before_cursor)[0]

        # Draw the text
        text_surf = self.font.render(display_text, True, self.EDIT_ACTIVE_COLOR)
        self.screen.blit(text_surf, (x, y))

        # Draw cursor (blinking)
        if pg.time.get_ticks() % 1000 < 500:  # Blink every 500ms
            cursor_x = x + cursor_x_offset
            cursor_height = self.font.get_height()
            pg.draw.line(self.screen, self.TEXT_COLOR,
                         (cursor_x, y), (cursor_x, y + cursor_height), 2)

    def draw_sprite_list(self, panel_rect):
        """Draw the sprite list panel."""
        y = panel_rect.y + 10

        # Panel title
        title = self.font.render("Sprite List", True, self.TEXT_COLOR)
        self.screen.blit(title, (panel_rect.x + 15, y))
        y += 25

        # Separator
        pg.draw.line(self.screen, self.BORDER_COLOR,
                     (panel_rect.x + 10, y), (panel_rect.x + panel_rect.width - 10, y))
        y += 10

        if len(self.filtered_sprites) == 0:
            no_sprites = self.font_small.render("No sprites", True, self.LABEL_COLOR)
            self.screen.blit(no_sprites, (panel_rect.x + 15, y))
            return

        # Calculate how many sprites we can show
        row_height = 20
        available_height = panel_rect.height - (y - panel_rect.y) - 20
        visible_sprites = available_height // row_height

        # Calculate scroll to keep current sprite visible
        start_idx = max(0, self.sprite_index - visible_sprites // 2)
        end_idx = min(len(self.filtered_sprites), start_idx + visible_sprites)
        start_idx = max(0, end_idx - visible_sprites)

        for i in range(start_idx, end_idx):
            sprite_item = self.filtered_sprites.iloc[i]
            is_selected = (i == self.sprite_index)
            has_edits = i in self.pending_edits

            # Selection highlight
            if is_selected:
                highlight_rect = pg.Rect(panel_rect.x + 5, y - 2,
                                         panel_rect.width - 20, row_height)
                pg.draw.rect(self.screen, self.EDIT_HIGHLIGHT_COLOR, highlight_rect)

            # Truncate sprite name - use pending edit name if available
            if has_edits and 'SpriteName' in self.pending_edits[i]:
                name = self.pending_edits[i]['SpriteName']
            else:
                name = sprite_item['SpriteName']
            max_chars = 26
            if len(name) > max_chars:
                name = name[:max_chars - 3] + "..."

            # Add modified indicator
            if has_edits:
                name = "* " + name

            text_color = self.MODIFIED_COLOR if has_edits else (
                self.EDIT_CURSOR_COLOR if is_selected else self.TEXT_COLOR)
            prefix = "> " if is_selected else "  "
            sprite_surf = self.font_small.render(f"{prefix}{name}", True, text_color)
            self.screen.blit(sprite_surf, (panel_rect.x + 10, y))
            y += row_height

        # Scrollbar
        list_start_y = panel_rect.y + 45
        list_height = panel_rect.height - 55
        scrollbar_x = panel_rect.x + panel_rect.width - 15
        pg.draw.rect(self.screen, self.BORDER_COLOR,
                     (scrollbar_x, list_start_y, 8, list_height), 1)

        if len(self.filtered_sprites) > visible_sprites:
            thumb_h = max(20, list_height * visible_sprites // len(self.filtered_sprites))
            thumb_y = list_start_y + (list_height - thumb_h) * start_idx // (
                len(self.filtered_sprites) - visible_sprites)
            pg.draw.rect(self.screen, self.HIGHLIGHT_COLOR,
                         (scrollbar_x + 1, thumb_y, 6, thumb_h))


if __name__ == "__main__":
    viewer = SpriteViewer()
    viewer.run()
