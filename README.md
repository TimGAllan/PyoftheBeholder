# Py of the Beholder

A Python remake of the classic 1991 DOS RPG "Eye of the Beholder" by Westwood Studios. This project renders a first-person perspective view of a tile-based dungeon using Pygame, replicating the original game's viewport rendering system.

## Requirements

- Python 3.7+
- pygame
- pandas

Install dependencies:
```bash
pip install pygame pandas
```

## Running the Game

```bash
python main.py
```

### Game Controls

| Key | Action |
|-----|--------|
| W | Move forward |
| S | Move backward |
| A | Strafe left |
| D | Strafe right |
| Q | Rotate left |
| E | Rotate right |
| SPACE | Interact with switches |
| ESC | Quit |

## Project Structure

```
PyoftheBeholder/
├── main.py                    # Entry point, game loop
├── src/                       # Source code
│   ├── game.py               # Pygame window, clock, rendering pipeline
│   ├── player.py             # Position (L,X,Y,D), movement, switch interaction
│   ├── dungeon.py            # Dungeon & DungeonLevel classes
│   ├── dungeon_view.py       # Viewport camera, panel system for 3D perspective
│   ├── dungeon_tileset.py    # Loads sprites from CSV metadata + wallset images
│   ├── cursor.py             # Cursor class
│   └── utils.py              # Image loading utilities (SCALE_FACTOR=3)
├── levels/                    # Level data
│   └── sewer.py              # Level 1 - wall grids, clipping, switches
├── data/                      # Game data files (CSV)
│   ├── tiles.csv             # Tile definitions (Environment, Wall, Panel -> Sprite)
│   ├── sprites.csv           # Sprite source coordinates in wallset images
│   ├── panels.csv            # Panel screen positions and dimensions
│   ├── imagefiles.csv        # Wallset image file list
│   └── walls.csv             # Wall type definitions
├── assets/                    # Game assets
│   ├── Environments/         # Wallset sprite sheets + adornments
│   ├── UI/                   # Compass overlays (N.png, S.png, E.png, W.png)
│   └── items/                # Item sprites
└── tools/                     # Development tools
    ├── tile_viewer.py        # Interactive tile viewer/editor
    └── sprite_viewer.py      # Sprite sheet browser
```

## Data Files

### tiles.csv
Maps tile combinations to sprites. Each row defines a tile:
- `Environment` - The tileset/theme (e.g., "Sewer")
- `Wall` - Wall variant (e.g., "A", "B", "BG1")
- `Panel` - Screen panel position (e.g., "LP1", "CF2")
- `SpriteName` - Reference to sprite in sprites.csv
- `Flip` - Whether to horizontally flip the sprite
- `Blit_Xpos_Offset`, `Blit_Ypos_Offset` - Per-tile position adjustments

### sprites.csv
Defines sprite source coordinates within wallset images:
- `SpriteName` - Unique sprite identifier
- `File` - Source image file
- `Xpos`, `Ypos` - Top-left corner in source image
- `Width`, `Height` - Sprite dimensions

### panels.csv
Defines screen panel positions and sizes:
- `Panel` - Panel code (e.g., "LP1", "CF2", "RD3")
- `Blit_Xpos`, `Blit_Ypos` - Base screen position
- `Width`, `Height` - Panel dimensions

## Tools

### Sprite Viewer (`tools/sprite_viewer.py`)

Browse sprites within wallset images from `data/sprites.csv`.

```bash
python tools/sprite_viewer.py
```

1. Select an image file from the list
2. Browse sprites with A/D keys
3. Red rectangle shows sprite bounds in the image
4. Use +/- to zoom, arrow keys to pan

| Key | Action |
|-----|--------|
| A/D | Previous/Next sprite |
| +/- | Zoom in/out |
| Arrow Keys | Pan image |
| R | Reset zoom/pan |
| B | Back to file selection |

---

### Tile Viewer (`tools/tile_viewer.py`)

Interactive tool to browse and inspect tile renderings from `data/tiles.csv`.

```bash
python tools/tile_viewer.py
```

#### Main Controls

| Key | Action |
|-----|--------|
| A/D | Previous/Next tile |
| Home/End | Jump to first/last tile |
| Page Up/Down | Jump 10 tiles |
| P | Open tile picker (hierarchical browser) |
| T | Open sprite selector (change tile's sprite) |
| F | Cycle environment filter |
| R | Reset filter |
| E | Enter edit mode |
| G | Open grid settings (toggle panel visibility) |
| F5 | Reload all data from CSV files |
| ESC | Quit |

#### Tile Picker (P)

Hierarchical browser to navigate tiles:
1. **Environment** - Select tileset/theme
2. **Wall** - Select wall variant
3. **Panel** - Select screen panel

| Key | Action |
|-----|--------|
| Up/Down | Navigate items |
| Enter/Right | Drill down to next level |
| Left/Backspace | Go back to previous level |
| ESC | Close picker |

#### Edit Mode (E)

Modify tile properties and save changes:

| Key | Action |
|-----|--------|
| W/S | Select field (up/down) |
| A/D | Previous/Next tile |
| Arrow Keys | Adjust blit position offsets |
| 0-9, - | Type numeric value |
| Enter | Apply typed value |
| Space | Toggle Flip |
| F2 | Save all changes to CSV |
| Z | Undo changes for current tile |
| ESC | Exit edit mode |

#### Grid Settings (G)

Toggle visibility of panel guide boxes in the viewport.

## Architecture

### Viewport Panel System

The 3D perspective is achieved through a panel system. Each panel represents a specific screen position at a specific depth:

- **Position codes**: L/C/R (left/center/right), F/P/D (front/perpendicular/door), 1-4 (depth)
- **Examples**: LP1 (left perpendicular depth 1), CF2 (center front depth 2), RD3 (right door depth 3)

### Wall Grids

`wallsX` and `wallsY` are 2D arrays defining walls on X-axis and Y-axis edges:
- `X` = no wall
- `A`, `B`, etc. = wall variants for visual variety

### Clipping Grid

Defines walkable areas and special tiles:
- 0 = walkable
- 1 = blocked
- 2 = door (open)
- 3 = door (closed)
- 4 = special

### Scale Factor

The game renders at 3x scale (SCALE_FACTOR=3). Original coordinates in CSV files are at 1x scale and multiplied at runtime.

## License

This is a fan remake for educational purposes. Eye of the Beholder is a trademark of Westwood Studios/Electronic Arts.
