# Dungeon Level Encoding Guide

This guide explains how to encode a dungeon level from an Eye of the Beholder map image into Python code for Py of the Beholder.

## Map Image Legend

When reading a dungeon map image, use this legend:

| Visual Element | Meaning | Code Representation |
|----------------|---------|---------------------|
| White square | Walkable floor | `clipping = 0` |
| Black/filled area | Solid wall (impassable) | `clipping = 1` |
| Blue square | Door | `clipping = 2` (open) or `3` (closed) |
| Red square | Movable/secret wall | `clipping = 1` + special handling |
| Yellow square | Fake/illusory wall | `clipping = 0` with wall graphics |
| Arrow symbol | Switch/lever | Entry in `switches` dict |
| Numbered markers | Item locations | Future: items dict |
| "Entrance" label | Player start position | `entryPos` tuple |
| "Lv.X" label | Stairs to another level | `clipping = 4` (special) |

## Coordinate System

```
        North (Y decreases)
             ^
             |
West (X-) <--+--> East (X+)
             |
             v
        South (Y increases)

Grid origin (0,0) is top-left corner.
```

- **X-axis**: Columns, increases going RIGHT (East)
- **Y-axis**: Rows, increases going DOWN (South)
- **Array indexing**: `grid[Y][X]` (row first, then column)

## File Structure

Each level file should be located in `levels/` and follow this structure:

```python
"""
Level Name - Level N of the dungeon
Description of the level.
"""
from src.dungeon import Dungeon, DungeonLevel

environment = 'EnvironmentName'  # e.g., 'Sewer', 'Caves', 'Castle'

wallsX = [
    # 2D array of vertical wall segments (walls between cells on X-axis)
]

wallsY = [
    # 2D array of horizontal wall segments (walls between cells on Y-axis)
]

clipping = [
    # 2D array of cell properties (walkable, blocked, doors, special)
]

adornments = {
    # Dictionary of decorative objects on walls
}

switches = {
    # Dictionary of interactive switches
}

entryPos = (level_index, x, y, direction)

levels = [DungeonLevel(environment, wallsX, wallsY, clipping, adornments, switches)]

dungeon = Dungeon(levels, entryPos)
```

## Step-by-Step Encoding Process

### Step 1: Determine Grid Dimensions

1. Count the number of cells horizontally (columns) = **width**
2. Count the number of cells vertically (rows) = **height**
3. The grid arrays will be `height` rows × `width` columns

Typical Eye of the Beholder levels are approximately 30×30 cells.

### Step 2: Create the Clipping Grid

The clipping grid determines what the player can walk through.

**Values:**
- `0` = Walkable floor (player can move here)
- `1` = Solid wall (player cannot pass)
- `2` = Open door (walkable, renders as open door)
- `3` = Closed door (blocked, renders as closed door)
- `4` = Special tile (walkable, used for stairs, triggers, etc.)

**Process:**
1. Start with a grid filled with `1` (all walls)
2. For each white square on the map, set that cell to `0`
3. For each blue door square, set to `2` (open) or `3` (closed)
4. For stairs/special locations, set to `4`

**Example:**
```python
clipping = [
    [1,1,1,1,1,1,1,1,1,1],  # Row 0: all walls
    [1,1,1,0,0,0,1,1,1,1],  # Row 1: corridor at columns 3-5
    [1,1,1,0,1,0,1,1,1,1],  # Row 2: corridor with wall in middle
    [1,1,1,0,3,0,1,1,1,1],  # Row 3: closed door at column 4
    [1,1,1,0,0,0,1,1,1,1],  # Row 4: corridor continues
    [1,1,1,1,1,1,1,1,1,1],  # Row 5: all walls
]
```

### Step 3: Create the Wall Grids (wallsX and wallsY)

The wall grids define the *visual appearance* of walls, separate from collision.

**Values:**
- `'X'` = No wall (empty/transparent)
- `'A'` = Wall variant A (standard wall texture)
- `'B'` = Wall variant B (alternate wall texture for variety)

**Understanding wallsX vs wallsY:**

```
wallsY defines HORIZONTAL walls (─)
These appear when looking North or South

wallsX defines VERTICAL walls (│)
These appear when looking East or West

Cell layout with walls:
    wallsY[y][x]
        ─────
       │     │
wallsX │cell │ wallsX[y][x+1]
       │     │
        ─────
    wallsY[y+1][x]
```

**Process:**
1. Start with grids filled with `'X'` (no walls)
2. For each edge between a walkable cell and a wall cell, add a wall
3. Alternate between `'A'` and `'B'` for visual variety

**Example:**
```python
# A simple corridor going East-West
wallsX = [
    ['X','X','X','X','X','X'],
    ['X','X','X','A','X','B'],  # Vertical walls on sides of corridor
    ['X','X','X','A','X','B'],
    ['X','X','X','X','X','X'],
]

wallsY = [
    ['X','X','X','X','X','X'],
    ['X','X','X','A','B','A'],  # Horizontal wall above corridor
    ['X','X','X','X','X','X'],  # No wall in corridor
    ['X','X','X','B','A','B'],  # Horizontal wall below corridor
]
```

### Step 4: Define Adornments

Adornments are decorative objects placed on walls (torches, levers, etc.).

**Format:**
```python
adornments = {
    (axis, x, y): 'AdornmentName',
}
```

**Parameters:**
- `axis`: `'x'` for vertical walls (wallsX), `'y'` for horizontal walls (wallsY)
- `x, y`: Grid coordinates of the wall
- `AdornmentName`: Name of adornment folder in `assets/Environments/{env}/Adornments/`

**Common adornments:**
- `'LeverUp'` - Lever in up position
- `'LeverDown'` - Lever in down position
- `'Torch'` - Wall torch
- `'0'` - Empty/default adornment

**Example:**
```python
adornments = {
    ('x', 11, 12): 'LeverUp',    # Lever on vertical wall at (11, 12)
    ('y', 5, 8): 'Torch',        # Torch on horizontal wall at (5, 8)
}
```

### Step 5: Define Switches

Switches are interactive elements that trigger actions (usually opening/closing doors).

**Format:**
```python
switches = {
    (level, x, y, direction): [(door_x, door_y), (adornment_axis, adorn_x, adorn_y)],
}
```

**Parameters:**
- `level`: Level index (usually 0 for single-level)
- `x, y`: Position where player must stand to activate
- `direction`: Direction player must face (`'N'`, `'S'`, `'E'`, `'W'`)
- `door_x, door_y`: Coordinates of the door to toggle
- `adornment_axis, adorn_x, adorn_y`: Adornment to update when triggered

**Behavior:**
- When player presses SPACE at the specified position/direction:
  - Door toggles: `3` (closed) ↔ `2` (open)
  - Adornment toggles: `'LeverUp'` ↔ `'LeverDown'`

**Example:**
```python
switches = {
    # Standing at (11, 12) facing North, toggles door at (11, 12) and lever adornment
    (0, 11, 12, 'N'): [(11, 12), ('x', 11, 12)],

    # Standing at (5, 5) facing East, toggles door at (8, 5)
    (0, 5, 5, 'E'): [(8, 5), ('y', 5, 5)],
}
```

### Step 6: Set Entry Position

The entry position defines where the player starts.

**Format:**
```python
entryPos = (level_index, x, y, direction)
```

**Parameters:**
- `level_index`: Which level (0 for first level)
- `x`: Starting X coordinate (column)
- `y`: Starting Y coordinate (row)
- `direction`: Starting facing direction (`'N'`, `'S'`, `'E'`, `'W'`)

**Example:**
```python
entryPos = (0, 7, 13, 'E')  # Start at (7, 13) facing East
```

### Step 7: Choose Environment

The environment determines which tileset graphics are used.

**Available environments:**
- `'Sewer'` - Brick/sewer tileset (levels 1-4)
- `'Caves'` - Cave/cavern tileset (future)
- `'Castle'` - Stone castle tileset (future)

```python
environment = 'Sewer'
```

## Validation Checklist

Before testing your level:

- [ ] Grid dimensions match the map
- [ ] All walkable areas have `clipping = 0`
- [ ] All doors have `clipping = 2` or `3`
- [ ] Entry position is on a walkable cell (`clipping = 0`)
- [ ] Entry position faces a valid direction
- [ ] wallsX and wallsY have same dimensions as clipping
- [ ] All switch positions are on walkable cells
- [ ] All switch door targets exist in the clipping grid
- [ ] Adornment coordinates match wall positions

## Example: Encoding a Simple Room

Given this map:
```
#####
#...#
#.#.#
#...D
#####
```
Where `#` = wall, `.` = floor, `D` = door

**Clipping grid:**
```python
clipping = [
    [1, 1, 1, 1, 1],  # Row 0
    [1, 0, 0, 0, 1],  # Row 1
    [1, 0, 1, 0, 1],  # Row 2
    [1, 0, 0, 0, 3],  # Row 3 (door at column 4)
    [1, 1, 1, 1, 1],  # Row 4
]
```

**Entry position (starting in room facing East toward door):**
```python
entryPos = (0, 1, 2, 'E')
```

## Tips for Accuracy

1. **Use graph paper or a spreadsheet** to map out coordinates before coding
2. **Start from a corner** and work systematically across the map
3. **Mark the origin** on your reference map to avoid off-by-one errors
4. **Test incrementally** - add a few rows, test, then add more
5. **Use comments** in the arrays to mark significant features:
   ```python
   clipping = [
       [1,1,1,1,1,1,1,1,1,1],  # Row 0
       [1,0,0,0,1,1,1,1,1,1],  # Row 1 - entrance corridor
       [1,0,1,3,1,1,1,1,1,1],  # Row 2 - door to main hall
       # ... etc
   ]
   ```

## Reference: Original Eye of the Beholder Level Structure

The original game has 12 levels:
- Levels 1-4: Sewer/Dungeon theme
- Levels 5-7: Dwarf mines theme
- Levels 8-10: Drow caves theme
- Levels 11-12: Xanathar's lair

Each level typically contains:
- 1 entrance/exit point
- Multiple locked doors
- Several switches/levers
- Hidden areas and secret doors
- Item placement locations
- Monster spawn points (future feature)
