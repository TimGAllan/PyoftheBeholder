# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Py of the Beholder (POB) is a Python dungeon crawler game inspired by Eye of the Beholder. It renders a first-person perspective view of a tile-based dungeon using Pygame.

## Running the Game

```bash
cd POB
python Main.py
```

**Controls:** WASD (move/strafe), Q/E (rotate left/right), SPACE (interact with switches), ESC (quit)

**Dependencies:** pygame, pandas (Python 3.7+)

## Architecture

The game uses a component-based architecture centered around viewport rendering:

```
Main.py (entry point, game loop)
    ├── Game          - Pygame window, clock, rendering pipeline
    ├── Player        - Position (L,X,Y,D), movement, switch interaction
    ├── Dungeon       - Container for DungeonLevel objects
    │   └── DungeonLevel - Environment, wall grids, clipping, adornments, switches
    └── DungeonView   - Viewport camera, panel system for 3D perspective
        └── DungeonTileset - Loads sprites from CSV metadata + wallset images
```

### Key Concepts

**Viewport Panel System** (`Class_DungeonView.py`): The 3D perspective is achieved through a panel system. Each panel (e.g., LP1, CF2, RD3) represents a specific screen position at a specific depth. Panels have:
- Position codes: L/C/R (left/center/right), F/P/D (front wall/perpendicular wall/door), 1-4 (depth)
- Offsets per direction (N/S/E/W) to calculate which dungeon cell to render
- Predefined screen positions and dimensions for perspective scaling

**Wall Grids**: `wallsX` and `wallsY` are 2D arrays defining walls on X-axis and Y-axis edges. Values: 'X' (no wall), 'A'/'B' (wall variants for visual variety).

**Clipping Grid**: Defines walkable areas and special tiles:
- 0 = walkable
- 1 = blocked
- 2 = door (open)
- 3 = door (closed)
- 4 = special (unused?)

**Tile Loading** (`Class_DungeonTileSet.py`): Tiles are not individual files. The system:
1. Reads `Imagefiles.csv` to load wallset sprite sheets
2. Reads `Tiles.csv` to get coordinates (Environment, Wall, Panel → x, y, width, height, flip)
3. Extracts sub-images from sprite sheets using pandas DataFrames

### File Relationships

- `Dungeon.py` - Level data (wall grids, clipping, switches) for the "Sewer" environment
- `Tiles.csv` - Sprite coordinates for each (Environment, Wall, Panel) combination
- `Imagefiles.csv` - List of wallset sprite sheet files
- `Assets/Environments/` - Wallset PNGs and adornment sprites
- `Assets/UI/` - Compass/UI overlays (N.png, S.png, E.png, W.png)
