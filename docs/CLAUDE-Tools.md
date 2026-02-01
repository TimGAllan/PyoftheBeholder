# Development Tools

## Tile Viewer (`tools/tile_viewer.py`)

Interactive tool to browse, inspect, and edit tile renderings from `data/tiles.csv`.

```bash
python tools/tile_viewer.py
```

### Main Interface

- **Left panel**: Viewport showing tile rendering with panel grid overlay
- **Right panel**: Metadata display (tile info, sprite coordinates, blit positions)
- **Bottom bar**: Context-sensitive help text

### Navigation Controls

| Key | Action |
|-----|--------|
| A/D | Previous/Next tile |
| Home/End | Jump to first/last tile |
| Page Up/Down | Jump 10 tiles |
| P | Open tile picker (hierarchical) |
| T | Open sprite selector |
| F | Cycle environment filter |
| R | Reset filter |
| F5 | Reload all CSV data |
| ESC | Quit |

### Tile Picker (P)

Hierarchical browser with three levels:

1. **Environment** - Select tileset (e.g., "Sewer")
2. **Wall** - Select wall variant (e.g., "A", "B", "BG1")
3. **Panel** - Select screen panel (e.g., "LP1", "CF2")

| Key | Action |
|-----|--------|
| Up/Down | Navigate items |
| Enter/Right | Drill down |
| Left/Backspace | Go back |
| ESC | Close |

### Sprite Selector (T)

Change which sprite a tile uses:
- Lists all sprites from sprites.csv
- Shows thumbnail, filename, dimensions
- "(None)" option to clear sprite assignment

### Edit Mode (E)

Modify tile properties:

| Key | Action |
|-----|--------|
| W/S | Select field |
| A/D | Previous/Next tile |
| Arrow Keys | Adjust blit offsets (X/Y) |
| 0-9, - | Type numeric value |
| Enter | Apply typed value |
| Space | Toggle Flip |
| F2 | Save to CSV |
| Z | Undo current tile changes |
| ESC | Exit edit mode |

**Editable fields:**
- Xpos, Ypos - Sprite source coordinates (modifies sprites.csv)
- Width, Height - Sprite dimensions (modifies sprites.csv)
- Blit_Xpos_Offset, Blit_Ypos_Offset - Position adjustment (modifies tiles.csv)
- Flip - Horizontal flip (modifies tiles.csv)

### Grid Settings (G)

Toggle visibility of panel guide boxes:

| Key | Action |
|-----|--------|
| Arrow Keys | Navigate panels |
| Space | Toggle panel visibility |
| A | Enable all panels |
| N | Disable all panels |
| ESC | Close |

### Visual Indicators

- **Blue highlight**: Current panel position
- **Red crosshairs**: Panel center point
- **Orange text**: Modified (unsaved) values
- **Checkerboard**: Transparent areas

### Saving Changes

Press **F2** in edit mode to save:
- Sprite coordinate changes → `sprites.csv`
- Tile offset/flip changes → `tiles.csv`
- Changes persist after reload

### Tips

- Use F5 to reload after external CSV edits
- Arrow keys in edit mode adjust offsets in real-time
- Grid settings help visualize panel boundaries
- Tile picker pre-selects current tile's environment

## In-Game Hot Reload

Press **F5** during gameplay to reload:
- DungeonTileset (all sprites re-extracted)
- DungeonView (panel calculations refreshed)

Useful for testing tile_viewer changes without restarting.

## Adding New Tools

Tools should:
1. Live in `tools/` directory
2. Add project root to path: `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))`
3. Change working directory: `os.chdir(os.path.join(os.path.dirname(__file__), '..'))`
4. Import from `src/` as needed

Example boilerplate:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from src.dungeon_tileset import DungeonTileset
from src.utils import SCALE_FACTOR
```
