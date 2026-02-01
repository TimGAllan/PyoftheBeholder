# Architecture

## System Overview

```
main.py (Game Loop)
    ├── Player (position, movement)
    ├── Game (window, rendering)
    │   └── DungeonView (panel system)
    │       └── DungeonTileset (sprite loading)
    └── DungeonLevel (wall grids, clipping)
```

## Core Components

### Player (`src/player.py`)
- State: `(level, x, y, direction)` where direction is N/S/E/W
- Movement table maps (key, direction) to (dx, dy, new_direction)
- Validates moves against clipping grid before executing
- Handles switch interaction for doors

### Game (`src/game.py`)
- Manages Pygame window (960x600 = 320x200 base * SCALE_FACTOR)
- 60 FPS game clock
- `redraw_window()`: Renders panels back-to-front, handles doors specially, draws UI

### DungeonView (`src/dungeon_view.py`)
The core rendering system using 33 panels for perspective:

**Panel Naming Convention:**
- Position: L(eft), C(enter), R(ight), F(ar-left), K(far-right)
- Type: F(ront), P(erpendicular), D(oor), BG(background)
- Depth: 1-4 (1=closest, 4=furthest)
- Examples: LP1 (left perpendicular depth 1), CF2 (center front depth 2)

**Render Order (back-to-front):**
```
BG → Depth 4 (FP4, KP4, LP4, RP4)
   → Depth 3 (8 panels)
   → Depth 2 (6 panels)
   → Depth 1 (6 panels)
```

**Direction-Aware Offsets:**
Each panel has 4 offset entries (N/S/E/W) determining which dungeon cell to render:
```python
panel_offsets = {
    'LP1': {'E': (0, 0), 'W': (0, 1), 'N': (0, 0), 'S': (1, 0)},
    # ... 160+ entries for all 33 panels × 4 directions
}
```

**Wall Grid Selection:**
- Facing E/W: 'P' panels use walls_x, 'F' panels use walls_y
- Facing N/S: 'F' panels use walls_x, 'P' panels use walls_y

### DungeonTileset (`src/dungeon_tileset.py`)
Three-step tile loading:
1. Load wallset images from `imagefiles.csv`
2. Load sprite coordinates from `sprites.csv`
3. Load tile mappings from `tiles.csv`, join with sprites/panels, extract sub-images

**DataFrame Structure:**
```python
wall_tiles[Environment, dungeon_map_code, Panel] → {
    Object, SpriteName, File, Xpos, Ypos, Width, Height,
    Flip, Blit_Xpos, Blit_Ypos, Blit_Xpos_Offset, Blit_Ypos_Offset, Image
}
```
Note: `dungeon_map_code` is the lookup key from level files, `Object` is the friendly name.

### DungeonLevel (`levels/sewer.py`)
- `walls_x`: 2D grid of vertical walls ('X'=none, 'A'/'B'=variants)
- `walls_y`: 2D grid of horizontal walls
- `clipping`: Walkability grid (0=walk, 1=block, 2=door open, 3=door closed, 4=special)
- `switches`: Maps (level, x, y, dir) to door positions and adornment toggles
- `adornments`: Maps (axis, x, y) to adornment names

## Data Flow

### Movement
```
Player.move(key) → validate clipping → update (x,y) → DungeonView.update_panels()
```

### Rendering
```
Game.redraw_window() → for panel in render_order:
    → DungeonTileset.image(env, wall, panel)
    → blit at DungeonTileset.blit_pos()
```

### Switch Interaction
```
Player.click_switch() → toggle clipping[door] (2↔3)
                      → toggle adornments[lever]
                      → DungeonView.update_panels()
```

## Coordinate Systems

**Dungeon Grid:**
- Indexed as `grid[y][x]`
- X-axis: 0-29 (East→West)
- Y-axis: 0-40+ (South→North)

**Screen Coordinates:**
- Origin top-left (0, 0)
- 960×600 pixels (3× scaled from 320×200)

**Blit Positions:**
- Base position from panels.csv
- Plus per-tile offset from tiles.csv
- Multiplied by SCALE_FACTOR (3)
