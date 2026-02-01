"""
Dungeon viewport rendering using a panel-based 3D perspective system.

This module implements the classic first-person dungeon view used in Eye of the Beholder.
The viewport is divided into 33 panels representing walls at different depths and positions.
Each panel maps to a dungeon cell based on the player's position and facing direction.

Panel naming convention:
    - Position prefix: L(eft), C(enter), R(ight), F(ar-left), K(far-right)
    - Type: F(ront wall), P(erpendicular wall), D(oor)
    - Depth suffix: 1-4 (1=closest, 4=furthest)
    - Special: BG (background)

Examples:
    - LP1: Left Perpendicular wall at depth 1 (closest)
    - CF2: Center Front wall at depth 2
    - RD3: Right Door at depth 3

Coordinate system for panel offsets:
    - Origin is player position (x, y)
    - Positive X is East, Negative X is West
    - Positive Y is South, Negative Y is North
    - Offsets are direction-dependent to achieve correct perspective
"""
import os
import pandas as pd
from .dungeon_tileset import DungeonTileset
from .utils import SCALE_FACTOR


# Wall type constants
class WallType:
    """Constants for wall types in the dungeon grid."""
    NONE = 'X'          # No wall (empty space)
    NO_ADORNMENT = 'x'  # No adornment marker


# Directions where perpendicular walls use WallsX grid
HORIZONTAL_FACING = ('E', 'W')


class DungeonView:
    """
    Manages the first-person viewport rendering using a panel-based system.

    The viewport is divided into 33 panels representing walls at different
    depths and positions. Each panel maps to a dungeon cell based on the
    player's position and facing direction.

    Attributes:
        environment (str): Name of the current environment/tileset (e.g., 'Sewer')
        tiles (dict): Current wall type for each panel
        adornment_panels (dict): Current adornment state for each panel
        dungeon_tileset (DungeonTileset): Tile image manager

    Panel rendering order (back to front):
        BG -> Depth 4 -> Depth 3 -> Depth 2 -> Depth 1
    """


    def __init__(self, environment):
        """
        Initialize the dungeon view for a given environment.

        Args:
            environment (str): Name of the environment tileset to use (e.g., 'Sewer')
        """
        self.environment = environment
        self.dungeon_tileset = DungeonTileset()
        self.adornments_path = os.path.join('assets/Environments', self.environment, 'Adornments')


        # Panel list in render order (back to front)
        self.panels = [
            'BG', 'FP4', 'KP4', 'LP4', 'RP4', 'FF3', 'LF3', 'CF3', 'RF3', 'KF3',
            'CD3', 'LD3', 'RD3', 'FP3', 'LP3', 'RP3', 'KP3', 'LF2', 'CF2', 'RF2',
            'CD2', 'LD2', 'RD2', 'LP2', 'RP2', 'LF1', 'CF1', 'RF1', 'CD1', 'LD1',
            'RD1', 'LP1', 'RP1'
        ]

        # Pre-compute panel groups by type for efficient iteration
        self._panels_by_type = {
            'F': [p for p in self.panels if len(p) > 1 and p[1] == 'F'],
            'P': [p for p in self.panels if len(p) > 1 and p[1] == 'P'],
            'D': [p for p in self.panels if len(p) > 1 and p[1] == 'D'],
        }

        # Initialize panel dictionaries
        self.tiles = self._create_panel_dict(WallType.NO_ADORNMENT)
        self.tiles['BG'] = 'BG1'
        self.adornment_panels = self._create_panel_dict(WallType.NO_ADORNMENT)


        # Panel image filenames for adornment rendering
        self.panel_image_filenames = {
            'FP4': 'FP4.png', 'KP4': 'KP4.png', 'LP4': 'LP4.png', 'RP4': 'RP4.png',
            'FF3': 'F3.png', 'LF3': 'F3.png', 'CF3': 'F3.png', 'RF3': 'F3.png', 'KF3': 'F3.png',
            'CD3': 'D3.png', 'LD3': 'LD3.png', 'RD3': 'RD3.png',
            'FP3': 'FP3.png', 'LP3': 'LP3.png', 'RP3': 'RP3.png', 'KP3': 'KP3.png',
            'LF2': 'F2.png', 'CF2': 'F2.png', 'RF2': 'F2.png',
            'CD2': 'D2.png', 'LD2': 'LD2.png', 'RD2': 'RD2.png',
            'LP2': 'LP2.png', 'RP2': 'RP2.png',
            'LF1': 'F1.png', 'CF1': 'F1.png', 'RF1': 'F1.png',
            'CD1': 'D1.png', 'LD1': 'LD1.png', 'RD1': 'RD1.png',
            'LP1': 'LP1.png', 'RP1': 'RP1.png'
        }

        # Load panel data from CSV
        panels_df = pd.read_csv('data/panels.csv')
        panels_df = panels_df.set_index('Panel')

        # Panel dimensions (width, height) for perspective scaling
        self.panel_sizes = {
            panel: (int(row['Width']) * SCALE_FACTOR, int(row['Height']) * SCALE_FACTOR)
            for panel, row in panels_df.iterrows()
        }

        # Panel screen positions (x, y) for rendering
        self.panel_positions = {
            panel: (int(row['Blit_Xpos']) * SCALE_FACTOR, int(row['Blit_Ypos']) * SCALE_FACTOR)
            for panel, row in panels_df.iterrows()
        }

        # Panel offsets define which dungeon cell to render for each panel.
        # Format: panel_name: {direction: (dx, dy)}
        #
        # The offset is added to the player's (x, y) position to get the
        # dungeon cell coordinates for that panel. Offsets vary by direction
        # to maintain correct perspective as the player rotates.
        self.panel_offsets = {
            'FP4': {'E': (3, -1), 'W': (-3, 2), 'N': (-1, -3), 'S': (2, 3)},
            'KP4': {'E': (3, 2), 'W': (-3, -1), 'N': (2, -3), 'S': (-1, 3)},
            'LP4': {'E': (3, 0), 'W': (-3, 1), 'N': (0, -3), 'S': (1, 3)},
            'RP4': {'E': (3, 1), 'W': (-3, 0), 'N': (1, -3), 'S': (0, 3)},
            'FF3': {'E': (3, -2), 'W': (-2, 2), 'N': (-2, -2), 'S': (2, 3)},
            'LF3': {'E': (3, -1), 'W': (-2, 1), 'N': (-1, -2), 'S': (1, 3)},
            'CF3': {'E': (3, 0), 'W': (-2, 0), 'N': (0, -2), 'S': (0, 3)},
            'RF3': {'E': (3, 1), 'W': (-2, -1), 'N': (1, -2), 'S': (-1, 3)},
            'KF3': {'E': (3, 2), 'W': (-2, -2), 'N': (2, -2), 'S': (-2, 3)},
            'CD3': {'E': (3, 0), 'W': (-3, 0), 'N': (0, -3), 'S': (0, 3)},
            'LD3': {'E': (3, -1), 'W': (-3, 1), 'N': (-1, -3), 'S': (1, 3)},
            'RD3': {'E': (3, 1), 'W': (-3, -1), 'N': (1, -3), 'S': (-1, 3)},
            'FP3': {'E': (2, -1), 'W': (-2, 2), 'N': (-1, -2), 'S': (2, 2)},
            'LP3': {'E': (2, 0), 'W': (-2, 1), 'N': (0, -2), 'S': (1, 2)},
            'RP3': {'E': (2, 1), 'W': (-2, 0), 'N': (1, -2), 'S': (0, 2)},
            'KP3': {'E': (2, 2), 'W': (-2, -1), 'N': (2, -2), 'S': (-1, 2)},
            'LF2': {'E': (2, -1), 'W': (-1, 1), 'N': (-1, -1), 'S': (1, 2)},
            'CF2': {'E': (2, 0), 'W': (-1, 0), 'N': (0, -1), 'S': (0, 2)},
            'RF2': {'E': (2, 1), 'W': (-1, -1), 'N': (1, -1), 'S': (-1, 2)},
            'CD2': {'E': (2, 0), 'W': (-2, 0), 'N': (0, -2), 'S': (0, 2)},
            'LD2': {'E': (2, -1), 'W': (-2, 1), 'N': (-1, -2), 'S': (1, 2)},
            'RD2': {'E': (2, 1), 'W': (-2, -1), 'N': (1, -2), 'S': (-1, 2)},
            'LP2': {'E': (1, 0), 'W': (-1, 1), 'N': (0, -1), 'S': (1, 1)},
            'RP2': {'E': (1, 1), 'W': (-1, 0), 'N': (1, -1), 'S': (0, 1)},
            'LF1': {'E': (1, -1), 'W': (0, 1), 'N': (-1, 0), 'S': (1, 1)},
            'CF1': {'E': (1, 0), 'W': (0, 0), 'N': (0, 0), 'S': (0, 1)},
            'RF1': {'E': (1, 1), 'W': (0, -1), 'N': (1, 0), 'S': (-1, 1)},
            'CD1': {'E': (1, 0), 'W': (-1, 0), 'N': (0, -1), 'S': (0, 1)},
            'LD1': {'E': (1, -1), 'W': (-1, 1), 'N': (-1, -1), 'S': (1, 1)},
            'RD1': {'E': (1, 1), 'W': (-1, -1), 'N': (1, -1), 'S': (-1, 1)},
            'LP1': {'E': (0, 0), 'W': (0, 1), 'N': (0, 0), 'S': (1, 0)},
            'RP1': {'E': (0, 1), 'W': (0, 0), 'N': (1, 0), 'S': (0, 0)}
        }

    def _create_panel_dict(self, default_value):
        """
        Create a dictionary mapping all panels to a default value.

        Args:
            default_value: The value to assign to each panel

        Returns:
            dict: Panel names mapped to the default value
        """
        return {panel: default_value for panel in self.panels}

    def _safe_grid_lookup(self, grid, x, y, default=WallType.NONE):
        """
        Safely lookup a value in a 2D grid with bounds checking.

        Args:
            grid: 2D list to lookup from (indexed as grid[y][x])
            x: X coordinate (column)
            y: Y coordinate (row)
            default: Value to return if coordinates are out of bounds

        Returns:
            The grid value at (x, y) or default if out of bounds
        """
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            return grid[y][x]
        return default

    def _swap_background(self):
        """
        Swap the background between BG1 and BG2.

        Called on each panel update (keypress) to create a subtle
        animation effect (e.g., flickering torchlight).
        """
        self.tiles['BG'] = 'BG2' if self.tiles['BG'] == 'BG1' else 'BG1'

    def _get_panel_coordinate(self, panel, direction, player_x, player_y):
        """
        Calculate the dungeon coordinate for a panel based on player position.

        Args:
            panel: Panel name (e.g., 'LP1', 'CF2')
            direction: Player facing direction ('N', 'S', 'E', 'W')
            player_x: Player X coordinate
            player_y: Player Y coordinate

        Returns:
            tuple: (target_x, target_y) dungeon coordinates for this panel
        """
        offset = self.panel_offsets[panel][direction]
        return (player_x + offset[0], player_y + offset[1])

    def update_panels(self, player_position, walls_x, walls_y, adornments, clipping, swap_background=True):
        """
        Update all panel tile assignments based on player position and dungeon state.

        This method recalculates which wall/door tiles should be displayed in each
        panel of the viewport. It handles:
        - Background animation (optional)
        - Wall panels (perpendicular and front walls)
        - Door panels
        - Adornments on walls

        Args:
            player_position: Tuple of (x, y, direction) for player location
            walls_x: 2D grid of walls on X-axis edges
            walls_y: 2D grid of walls on Y-axis edges
            adornments: Dict mapping (axis, x, y) to adornment names
            clipping: 2D grid of clipping/door values
            swap_background: If True, swap background (for movement). Default True.
        """
        x, y, d = player_position

        # Swap background only when requested (typically on movement, not interactions)
        if swap_background:
            self._swap_background()

        # Determine which panel types use which wall grid based on player direction.
        #
        # The wall grids are constant:
        #   - walls_x contains vertical wall segments (used for 'x' axis adornments)
        #   - walls_y contains horizontal wall segments (used for 'y' axis adornments)
        #
        # What changes based on direction is which PANEL TYPES map to which grid:
        #   - When facing E/W: 'P' panels use walls_x, 'F' panels use walls_y
        #   - When facing N/S: 'F' panels use walls_x, 'P' panels use walls_y
        #
        # This is because:
        #   - Facing East/West: side walls (P) are vertical, front walls (F) are horizontal
        #   - Facing North/South: front walls (F) are vertical, side walls (P) are horizontal

        if d in HORIZONTAL_FACING:
            walls_x_panel_type = 'P'  # P panels use walls_x when facing E/W
            walls_y_panel_type = 'F'  # F panels use walls_y when facing E/W
        else:
            walls_x_panel_type = 'F'  # F panels use walls_x when facing N/S
            walls_y_panel_type = 'P'  # P panels use walls_y when facing N/S

        # Process walls_x panels (vertical walls, 'x' axis adornments)
        for panel in self._panels_by_type[walls_x_panel_type]:
            target_x, target_y = self._get_panel_coordinate(panel, d, x, y)
            self.tiles[panel] = self._safe_grid_lookup(walls_x, target_x, target_y)

            # Check for adornments on this wall
            adornment_key = ('x', target_x, target_y)
            self.adornment_panels[panel] = adornments.get(adornment_key, WallType.NO_ADORNMENT)

        # Process walls_y panels (horizontal walls, 'y' axis adornments)
        for panel in self._panels_by_type[walls_y_panel_type]:
            target_x, target_y = self._get_panel_coordinate(panel, d, x, y)
            self.tiles[panel] = self._safe_grid_lookup(walls_y, target_x, target_y)

            # Check for adornments on this wall
            adornment_key = ('y', target_x, target_y)
            self.adornment_panels[panel] = adornments.get(adornment_key, WallType.NO_ADORNMENT)

        # Process door panels (use clipping grid)
        for panel in self._panels_by_type['D']:
            target_x, target_y = self._get_panel_coordinate(panel, d, x, y)
            clipping_value = self._safe_grid_lookup(clipping, target_x, target_y, default=0)
            self.tiles[panel] = str(clipping_value)
