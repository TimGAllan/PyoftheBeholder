# Data Files

All game data is stored in CSV files under `data/`. This data-driven approach enables runtime modification via the tile_viewer tool.

## tiles.csv

Maps tile combinations to sprites. Each row defines how a specific (Environment, Wall, Panel) combination renders.

| Column | Type | Description |
|--------|------|-------------|
| Environment | string | Tileset theme (e.g., "Sewer") |
| Wall | string | Wall variant ("A", "B", "BG1", "0"-"4" for doors) |
| Panel | string | Screen panel ("LP1", "CF2", etc.) |
| SpriteName | string | Reference to sprite in sprites.csv |
| Flip | bool | Horizontally flip the sprite |
| Blit_Xpos_Offset | int | Per-tile X position adjustment |
| Blit_Ypos_Offset | int | Per-tile Y position adjustment |

**Example:**
```csv
Environment,Wall,Panel,SpriteName,Flip,Blit_Xpos_Offset,Blit_Ypos_Offset
Sewer,A,LP1,BRICK_WALLS_1_1_24_120,False,0,0
Sewer,A,RP1,BRICK_WALLS_1_1_24_120,True,0,0
```

## sprites.csv

Defines sprite source coordinates within wallset images.

| Column | Type | Description |
|--------|------|-------------|
| SpriteName | string | Unique identifier |
| File | string | Source image filename |
| Xpos | int | Left edge in source (1× scale) |
| Ypos | int | Top edge in source (1× scale) |
| Width | int | Sprite width (1× scale) |
| Height | int | Sprite height (1× scale) |

**Example:**
```csv
SpriteName,File,Xpos,Ypos,Width,Height
BRICK_WALLS_1_1_24_120,BRICK_WALLS.png,1,1,24,120
BRICK_BACKGROUND_0_0_176_120,BRICK_BACKGROUND.png,0,0,176,120
```

## panels.csv

Defines screen panel positions and dimensions.

| Column | Type | Description |
|--------|------|-------------|
| Panel | string | Panel code (e.g., "LP1") |
| Blit_Xpos | int | Base X position (1× scale) |
| Blit_Ypos | int | Base Y position (1× scale) |
| Width | int | Panel width (1× scale) |
| Height | int | Panel height (1× scale) |

**Example:**
```csv
Panel,Blit_Xpos,Blit_Ypos,Width,Height
LP1,0,0,24,120
CF1,24,8,128,96
CF2,48,16,80,64
```

## imagefiles.csv

Lists wallset image files to load.

| Column | Type | Description |
|--------|------|-------------|
| Environment | string | Tileset theme |
| File | string | Image filename in assets/Environments/ |

**Example:**
```csv
Environment,File
Sewer,BRICK_WALLS.png
Sewer,BRICK_BACKGROUND.png
```

## walls.csv

Wall type definitions (currently minimal).

## Scale Factor

All coordinates in CSV files are at **1× scale** (320×200 base resolution). At runtime, positions and dimensions are multiplied by `SCALE_FACTOR = 3` to produce 960×600 output.

**Final blit position calculation:**
```python
blit_x = (panels.Blit_Xpos + tiles.Blit_Xpos_Offset) * SCALE_FACTOR
blit_y = (panels.Blit_Ypos + tiles.Blit_Ypos_Offset) * SCALE_FACTOR
```

## Level Data (levels/sewer.py)

Level data is Python, not CSV:

```python
walls_x = [...]    # 2D grid: 'X'=no wall, 'A'/'B'=wall variants
walls_y = [...]    # Horizontal walls
clipping = [...]   # 0=walk, 1=block, 2=door open, 3=door closed, 4=special

switches = {
    (0, 7, 13, 'E'): [(7, 13), ('y', 6, 13)],  # level, x, y, dir → door pos, adornment
}

adornments = {
    ('y', 6, 13): "LeverUp",  # axis, x, y → adornment name
}

entry_pos = (0, 7, 13, 'E')  # Starting level, x, y, direction
```

## Adding New Content

### New Sprite
1. Add row to `sprites.csv` with coordinates in source image
2. Reference SpriteName in `tiles.csv`

### New Tile
1. Add row to `tiles.csv` linking (Environment, Wall, Panel) to SpriteName
2. Set Flip and offsets as needed

### New Panel
1. Add row to `panels.csv` with position and size
2. Add panel to render order in `dungeon_view.py`
3. Add offset entries in `panel_offsets` dict

### New Environment
1. Add wallset images to `assets/Environments/`
2. Add entries to `imagefiles.csv`
3. Add sprite definitions to `sprites.csv`
4. Add tile mappings to `tiles.csv`
