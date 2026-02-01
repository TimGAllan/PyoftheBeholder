# Code Style & Conventions

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `DungeonView`, `DungeonTileset` |
| Functions/Methods | snake_case | `update_panels()`, `click_switch()` |
| Private methods | Leading underscore | `_safe_grid_lookup()`, `_create_panel_dict()` |
| Constants | UPPER_CASE | `SCALE_FACTOR`, `HORIZONTAL_FACING` |
| Variables | snake_case | `wall_tiles`, `panel_offsets` |

## Direction Handling

Directions are single-character strings:
```python
'N'  # North
'S'  # South
'E'  # East
'W'  # West

HORIZONTAL_FACING = ('E', 'W')
```

Movement tables map (key, direction) to deltas:
```python
moves = {
    'w': {'N': [0, -1], 'S': [0, +1], 'E': [+1, 0], 'W': [-1, 0]},
    's': {'N': [0, +1], 'S': [0, -1], 'E': [-1, 0], 'W': [+1, 0]},
    # ...
}
```

## Grid Access

Always use `grid[y][x]` order:
```python
clipping[y][x]
walls_x[y][x]
walls_y[y][x]
```

Bounds checking pattern:
```python
def _safe_grid_lookup(self, grid, x, y):
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return grid[y][x]
    return 'X'  # Default: no wall
```

## Image Handling

Transparency via magenta colorkey:
```python
img.set_colorkey((255, 0, 255), pg.RLEACCEL)
```

Scaling convention:
```python
SCALE_FACTOR = 3  # 320×200 → 960×600
# All CSV coordinates are at 1× scale, multiplied at runtime
```

Sub-image extraction:
```python
sub_image(source, (x, y, width, height), SCALE_FACTOR, flip)
```

## DataFrame Patterns

Multi-indexed lookups:
```python
# Create multi-index (uses dungeon_map_code for level file lookups)
df = df.set_index(['Environment', 'dungeon_map_code', 'Panel'])

# Lookup
tile = df.loc[(environment, map_code, panel)]
```

Joining DataFrames:
```python
tiles_df = tiles_df.merge(sprites_df, on='SpriteName')
tiles_df = tiles_df.merge(panels_df, on='Panel')
```

## Panel Naming

Format: `{Position}{Type}{Depth}`

**Position codes:**
- `L` = Left
- `C` = Center
- `R` = Right
- `F` = Far-left
- `K` = Far-right (K for "right" to avoid conflict)

**Type codes:**
- `F` = Front wall
- `P` = Perpendicular wall
- `D` = Door
- `BG` = Background

**Depth:** 1-4 (1=closest)

Examples: `LP1`, `CF2`, `RD3`, `FP4`, `KP3`

## Error Handling

Bounds checking preferred over try/except:
```python
if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
    return grid[y][x]
return default_value
```

## Comments

- Use docstrings for classes and public methods
- Inline comments for non-obvious logic
- Panel offset tables have directional comments

```python
def update_panels(self):
    """Recalculate all panel tiles based on player position."""
    # Implementation...
```

## Import Order

1. Standard library
2. Third-party (pygame, pandas)
3. Local modules

```python
import os
import sys

import pygame as pg
import pandas as pd

from src.dungeon_tileset import DungeonTileset
from src.utils import SCALE_FACTOR
```
