# Py of the Beholder

Python remake of the 1991 DOS RPG "Eye of the Beholder" using Pygame. Implements a first-person tile-based dungeon crawler with a panel-based perspective rendering system that replicates the original game's viewport.

## Tech Stack
- Python 3.7+
- Pygame (display, input, surfaces)
- Pandas (CSV data, multi-indexed DataFrames)

## Quick Start
- Run: `python main.py`
- Tools: `python tools/tile_viewer.py`
- Hot-reload: F5 in-game reloads tileset

## Game Controls
- WASD: Move/strafe
- Q/E: Rotate left/right
- SPACE: Interact with switches
- ESC: Quit

## Project Structure
```
src/           # Core modules (game, player, dungeon_view, dungeon_tileset)
levels/        # Level data (wall grids, clipping, switches)
data/          # CSV metadata (tiles, sprites, panels)
assets/        # Sprite sheets and UI images
tools/         # Development utilities (tile_viewer)
```

## Key Files
- `main.py` - Entry point, game loop
- `src/dungeon_view.py` - Panel rendering system (core architecture)
- `src/dungeon_tileset.py` - Tile/sprite loading from CSV
- `data/tiles.csv` - Tile definitions (Environment, Wall, Panel -> Sprite)
- `data/panels.csv` - Panel screen positions and sizes

## Detailed Documentation
@docs/CLAUDE-Architecture.md
@docs/CLAUDE-CodeStyle.md
@docs/CLAUDE-Data.md
@docs/CLAUDE-Tools.md
