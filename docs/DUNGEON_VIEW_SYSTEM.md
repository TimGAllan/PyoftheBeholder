# Dungeon View Panel System

This document explains how the first-person 3D perspective rendering works in Py of the Beholder using a panel-based system.

## Overview

The dungeon view simulates a 3D first-person perspective by rendering pre-defined 2D panels at specific screen positions. Each panel represents a wall segment at a specific position relative to the player.

## Panel Naming Convention

Each panel has a 2-3 character code:

```
[Position][Type][Depth]
```

### Position (First Letter)

| Code | Position | Description |
|------|----------|-------------|
| `F` | Far-left | Two cells to the left of center |
| `L` | Left | One cell to the left of center |
| `C` | Center | Directly ahead of player |
| `R` | Right | One cell to the right of center |
| `K` | Far-right | Two cells to the right of center |

### Type (Second Letter)

| Code | Type | Description |
|------|------|-------------|
| `P` | Perpendicular | Side walls (parallel to view direction) |
| `F` | Front | Walls facing the player (perpendicular to view direction) |
| `D` | Door | Door openings in the center of a cell |

### Depth (Number)

| Depth | Distance | Description |
|-------|----------|-------------|
| `1` | 0-1 cells | Closest to player (walls of current and adjacent cell) |
| `2` | 1-2 cells | One cell ahead |
| `3` | 2-3 cells | Two cells ahead |
| `4` | 3-4 cells | Furthest visible (perpendicular walls only) |

## Panel Layout Diagram

This diagram shows all panels from a top-down view, with the party at the bottom facing North (up):

```
                    3 cells ahead
    ┌─────────┬─────────┬─────────┬─────────┬─────────┐
    │         │         │         │         │         │
FP4 │   LD3   │   LP4   │   D3    │   RP4   │   RD3   │ KP4
    │         │         │         │         │         │
    ├─────────┼─────────┼─────────┼─────────┼─────────┤
    │         │         │         │         │         │
FF3 │   LF3   │   CF3   │         │   RF3   │   KF3   │     ← Red (Front walls depth 3)
    │         │         │         │         │         │
    ├─────────┼─────────┼─────────┼─────────┼─────────┤
                    2 cells ahead
    ┌─────────┬─────────┬─────────┬─────────┬─────────┐
    │         │         │         │         │         │
FP3 │   LD2   │   LP3   │   D2    │   RP3   │   RD2   │ KP3
    │         │         │         │         │         │
    ├─────────┼─────────┼─────────┼─────────┼─────────┤
    │         │         │         │         │         │
    │   LF2   │   CF2   │         │   RF2   │         │     ← Blue (Front walls depth 2)
    │         │         │         │         │         │
    ├─────────┼─────────┼─────────┼─────────┼─────────┤
                    1 cell ahead
    ┌─────────┬─────────┬─────────┬─────────┬─────────┐
    │         │         │         │         │         │
    │   LD1   │   LP2   │   D1    │   RP2   │   RD1   │
    │         │         │         │         │         │
    ├─────────┼─────────┼─────────┼─────────┼─────────┤
    │         │         │         │         │         │
    │   LF1   │   CF1   │         │   RF1   │         │     ← Green (Front walls depth 1)
    │         │         │         │         │         │
    ├─────────┼─────────┼─────────┼─────────┼─────────┤
                    Party's cell
    ┌─────────┬─────────┬─────────┬─────────┬─────────┐
    │         │         │         │         │         │
    │         │   LP1   │ [PARTY] │   RP1   │         │
    │         │         │    ▲    │         │         │
    └─────────┴─────────┴─────────┴─────────┴─────────┘
                        Facing North
```

## Panel Types Explained

### Perpendicular Walls (P)

Perpendicular walls run parallel to the player's view direction. They form the side walls of corridors.

```
Player facing North:

    Wall                Wall
      │                  │
      │    Corridor      │
      │                  │
      │     ▲ Player     │
      │                  │
    LP1                RP1
```

- `LP1`, `RP1`: Walls on immediate left/right of player's cell
- `LP2`, `RP2`: Walls on left/right of cell 1 ahead
- `LP3`, `RP3`: Walls on left/right of cell 2 ahead
- `LP4`, `RP4`: Walls on left/right of cell 3 ahead
- `FP3`, `FP4`: Far-left perpendicular walls (visible in wide areas)
- `KP3`, `KP4`: Far-right perpendicular walls (visible in wide areas)

### Front Walls (F)

Front walls face the player directly. They block forward movement and are the most prominent visual element.

```
Player facing North:

    ════════════════════════
         Front Wall (CF1)
    ════════════════════════
              │
              │
              ▲ Player
```

- `LF1`, `CF1`, `RF1`: Front walls 1 cell ahead (left, center, right)
- `LF2`, `CF2`, `RF2`: Front walls 2 cells ahead
- `FF3`, `LF3`, `CF3`, `RF3`, `KF3`: Front walls 3 cells ahead (including far-left and far-right)

**Note:** There are no front walls at depth 4. Depth 3 is the maximum visible distance for front walls.

### Door Panels (D)

Door panels render doorways (open or closed) at specific positions.

```
Player facing North:

    ┌───┐   ┌─────┐   ┌───┐
    │   │   │ D1  │   │   │
    │   │   │door │   │   │
    └───┘   └─────┘   └───┘
              │
              ▲ Player
```

- `D1`, `LD1`, `RD1`: Doors 1 cell ahead (center, left-side, right-side)
- `D2`, `LD2`, `RD2`: Doors 2 cells ahead
- `D3`, `LD3`, `RD3`: Doors 3 cells ahead

## Wall Grid Mapping

The rendering system uses two wall grids depending on player direction:

### When Facing North or South

| Panel Type | Wall Grid | Reason |
|------------|-----------|--------|
| `P` (Perpendicular) | `wallsX` | Side walls are vertical (X-axis edges) |
| `F` (Front) | `wallsY` | Front walls are horizontal (Y-axis edges) |

### When Facing East or West

| Panel Type | Wall Grid | Reason |
|------------|-----------|--------|
| `P` (Perpendicular) | `wallsY` | Side walls are horizontal (Y-axis edges) |
| `F` (Front) | `wallsX` | Front walls are vertical (X-axis edges) |

## Rendering Order

Panels are rendered back-to-front to ensure proper layering (painter's algorithm):

1. **Background** (`BG`)
2. **Depth 4** - Furthest perpendicular walls (`FP4`, `KP4`, `LP4`, `RP4`)
3. **Depth 3** - Far walls and doors (`FF3`, `LF3`, `CF3`, `RF3`, `KF3`, `CD3`, `LD3`, `RD3`, `FP3`, `LP3`, `RP3`, `KP3`)
4. **Depth 2** - Middle distance (`LF2`, `CF2`, `RF2`, `CD2`, `LD2`, `RD2`, `LP2`, `RP2`)
5. **Depth 1** - Closest walls (`LF1`, `CF1`, `RF1`, `CD1`, `LD1`, `RD1`, `LP1`, `RP1`)

## Panel Offset System

Each panel has direction-dependent offsets that determine which dungeon cell to sample.

### Offset Format

```python
panelsOffsets = {
    'panel_name': {
        'N': (dx, dy),  # Offset when facing North
        'S': (dx, dy),  # Offset when facing South
        'E': (dx, dy),  # Offset when facing East
        'W': (dx, dy),  # Offset when facing West
    }
}
```

The offset is added to the player's position to find the target cell:
```python
target_x = player_x + offset[0]
target_y = player_y + offset[1]
```

### Example: Panel CF1 (Center Front, Depth 1)

```python
'CF1': {'E': (1, 0), 'W': (0, 0), 'N': (0, 0), 'S': (0, 1)}
```

- Facing **North**: Check cell at `(x+0, y+0)` - same cell, north wall
- Facing **South**: Check cell at `(x+0, y+1)` - cell to south, its north wall
- Facing **East**: Check cell at `(x+1, y+0)` - cell to east, its west wall
- Facing **West**: Check cell at `(x+0, y+0)` - same cell, west wall

### Example: Panel RP2 (Right Perpendicular, Depth 2)

```python
'RP2': {'E': (1, 1), 'W': (-1, 0), 'N': (1, -1), 'S': (0, 1)}
```

- Facing **North**: Check cell at `(x+1, y-1)` - one right, one ahead
- Facing **South**: Check cell at `(x+0, y+1)` - one ahead (in south direction)
- Facing **East**: Check cell at `(x+1, y+1)` - one ahead, one right (south)
- Facing **West**: Check cell at `(x-1, y+0)` - one ahead (in west direction)

## Visibility Rules

### Occlusion

Closer walls occlude (hide) further walls:
- A wall at `CF1` hides `CF2` and `CF3` behind it
- Side walls (`LP1`) partially block diagonal views

### Wide Area Visibility

The far panels (`F`, `K` prefix) are only visible in wide open areas:
- `FF3`, `KF3` require no walls at `LF2`/`RF2` and `LF1`/`RF1`
- `FP4`, `KP4` require open space at depth 3

## Complete Panel List

### All 33 Panels

| Panel | Position | Type | Depth |
|-------|----------|------|-------|
| `BG` | - | Background | - |
| `FP4` | Far-left | Perpendicular | 4 |
| `KP4` | Far-right | Perpendicular | 4 |
| `LP4` | Left | Perpendicular | 4 |
| `RP4` | Right | Perpendicular | 4 |
| `FF3` | Far-left | Front | 3 |
| `LF3` | Left | Front | 3 |
| `CF3` | Center | Front | 3 |
| `RF3` | Right | Front | 3 |
| `KF3` | Far-right | Front | 3 |
| `CD3` | Center | Door | 3 |
| `LD3` | Left | Door | 3 |
| `RD3` | Right | Door | 3 |
| `FP3` | Far-left | Perpendicular | 3 |
| `LP3` | Left | Perpendicular | 3 |
| `RP3` | Right | Perpendicular | 3 |
| `KP3` | Far-right | Perpendicular | 3 |
| `LF2` | Left | Front | 2 |
| `CF2` | Center | Front | 2 |
| `RF2` | Right | Front | 2 |
| `CD2` | Center | Door | 2 |
| `LD2` | Left | Door | 2 |
| `RD2` | Right | Door | 2 |
| `LP2` | Left | Perpendicular | 2 |
| `RP2` | Right | Perpendicular | 2 |
| `LF1` | Left | Front | 1 |
| `CF1` | Center | Front | 1 |
| `RF1` | Right | Front | 1 |
| `CD1` | Center | Door | 1 |
| `LD1` | Left | Door | 1 |
| `RD1` | Right | Door | 1 |
| `LP1` | Left | Perpendicular | 1 |
| `RP1` | Right | Perpendicular | 1 |

## Screen Positions

Each panel has a fixed screen position and size that creates the perspective effect:

- **Depth 1 panels**: Largest, positioned at screen edges
- **Depth 2 panels**: Medium size, positioned more centrally
- **Depth 3 panels**: Smaller, near center
- **Depth 4 panels**: Smallest, at vanishing point

The viewport is 528x360 pixels (before scaling).

## Implementation Notes

### updatePanels() Method

The `updatePanels()` method in `DungeonView` class:

1. Determines which wall grid to use based on player direction
2. Iterates through all panels
3. Calculates the target dungeon cell using offsets
4. Looks up the wall value from the appropriate grid
5. Stores the result for rendering

### Rendering in Game.redrawWindow()

1. Iterates through panels in render order
2. Skips panels with value `'X'` (no wall) or clipping values `0`, `1`, `4`
3. Retrieves the tile image from `DungeonTileset`
4. Blits the image at the panel's screen position
5. Renders adornments on top of walls
6. Renders UI overlay last

## Debugging Tips

1. **Wrong wall showing**: Check the panel offset for that direction
2. **Missing wall**: Verify the wall grid has a value other than `'X'`
3. **Wall in wrong position**: Check if using `wallsX` vs `wallsY` correctly
4. **Rendering order issues**: Verify panels list is in correct back-to-front order
