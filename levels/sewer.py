"""
Sewer - Level 1 of the dungeon
The starting area of the game.
"""
from src.dungeon import Dungeon, DungeonLevel

environment = 'Sewer'

walls_x = [
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','A','B','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','A','B','A','X','B','X','A','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','A','X','A','B','B','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','A','X','X','B','X','B','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','B','A','X','B','A','A','B','A','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','A','B','A','X','X','B','X','X','A','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','A','X','X','B','A','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','A','B','A','X','X','B','B','X','X','X','X','A','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','B','A','B','A','X','X','B','X','X','B','B','X','A','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','A','B','A','A','B','B','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','B','A','X','X','X','A','B','X','B','X','X','X','B','B','X','A','X','A','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','B','X','X','X','A','B','X','A','B','B','X','X','B','X','A','A','X','A','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','B','A','B','X','X','B','A','B','X','X','X','B','X','A','A','X','A','X','X','X','X','X'],
    ['X','X','X','X','A','B','X','A','B','A','B','A','B','A','X','A','B','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','A','X','A','B','A','B','A','B','A','B','X','X','X','A','A','X','B','B','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','A','B','A','B','A','B','A','B','A','B','A','X','A','X','B','X','A','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','A','B','A','X','X','X','A','B','X','A','B','X','B','A','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','B','X','X','B','A','B','A','B','A','B','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','A','X','B','B','A','B','B','X','B','X','B','A','X','A','B','A','B','A','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','B','A','B','X','B','A','B','A','B','A','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','A','B','A','B','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','A','B','A','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
]


walls_y = [
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','B','X','A','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','A','X','B','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','B','X','X','B','X','A','X','B','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','A','B','B','X','X','A','A','A','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','B','A','X','B','X','X','X','X','A','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','B','B','X','X','X','A','X','X','X','X','B','X','X','B','X','B','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','A','A','X','X','X','B','B','X','X','B','A','A','A','A','B','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','B','B','X','X','B','X','A','A','X','X','B','B','B','B','A','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','A','X','X','X','X','X','X','A','A','X','A','A','X','X','B','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','B','X','A','X','B','A','A','X','B','B','A','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','B','X','X','B','X','A','A','A','B','B','X','A','A','B','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','A','X','X','X','X','X','X','X','X','X','A','A','A','A','X','X','B','B','B','X','X','X','X','X'],
    ['X','X','X','X','X','X','B','A','A','X','X','B','X','A','A','X','A','X','B','X','A','B','B','X','X','B','X','X','X','X'],
    ['X','X','X','X','X','X','A','B','X','X','X','X','X','X','B','X','X','X','A','A','X','X','B','B','B','X','X','X','X','X'],
    ['X','X','X','X','B','X','X','X','X','X','X','X','X','X','X','A','X','A','B','B','X','X','A','A','A','X','X','X','X','X'],
    ['X','X','X','X','A','B','B','B','X','X','X','X','X','X','X','X','X','B','X','B','B','A','A','X','B','X','X','X','X','X'],
    ['X','X','X','X','B','A','A','X','X','X','X','X','X','X','X','X','X','A','B','X','X','X','X','B','X','X','X','X','X','X'],
    ['X','X','X','X','A','B','B','X','X','B','X','X','B','X','X','B','X','X','X','X','A','A','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','B','A','A','X','X','A','A','A','A','A','X','B','X','X','X','X','X','B','X','X','X','X','X','X','X','X'],
    ['X','X','X','B','X','X','A','X','X','A','X','X','X','X','X','X','B','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','A','X','X','X','X','X','X','A','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','B','X','X','A','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X','X'],
]

clipping = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1,2,1,0,1,2,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,4,1,1,1,0,0,1,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,2,0,0,0,0,1,2,1,0,0,0,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,0,0,0,1,1,0,1,1,0,0,1,1,2,1,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,1,1,1,1],
    [1,1,1,1,0,1,2,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,0,0,1,1,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,1,1,1,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


adornments = {
    # Door buttons/levers - key format: (wall_direction, x, y)
    # wall_direction: 'x' = on X-axis wall (vertical), 'y' = on Y-axis wall (horizontal)
    # Doors in clipping grid: 2 = open, 3 = closed

    # Rockfall at entry position - player sees this when entering facing East
    ('x', 7, 13): 'R',

    # Door at clipping[9][14] - Upper corridor door
    ('y', 14, 8): 'LeverUp',     # Button north of door

    # Door at clipping[11][12] - Original door (closed)
    ('x', 11, 12): 'LeverUp',    # Original lever

    # Door at clipping[11][16] - Central area door
    ('x', 17, 10): 'LeverUp',    # Button east of corridor

    # Door at clipping[11][20] - East corridor door
    ('y', 20, 10): 'LeverUp',    # Button in east passage

    # Door at clipping[16][11] - Western passage door
    ('y', 11, 15): 'LeverUp',    # Button north of door

    # Door at clipping[16][17] - Central-east door
    ('x', 18, 16): 'LeverUp',    # Button east of door

    # Door at clipping[17][20] - East passage door
    ('y', 20, 16): 'LeverUp',    # Button north of door

    # Door at clipping[20][6] - West lower door
    ('x', 6, 19): 'LeverUp',     # Button north of door

    # Door at clipping[21][15] - South central door
    ('y', 15, 20): 'LeverUp',    # Button north of door

    # Door at clipping[22][20] - Southeast door
    ('y', 20, 21): 'LeverUp',    # Button north of door
}


switches = {
    # Format: (level, player_x, player_y, facing_direction): [(door_y, door_x), (adornment_key)]
    # The switch toggles the door at clipping[door_y][door_x]
    # Player must be at position (player_x, player_y) facing direction to activate

    # Door at clipping[9][14] - Upper corridor door
    # Player stands at (14, 9) facing North to see button on north wall
    (0, 14, 9, 'N'): [(9, 14), ('y', 14, 8)],

    # Door at clipping[11][12] - Original door (closed by default)
    # Player stands at (11, 12) facing North to see lever
    (0, 11, 12, 'N'): [(11, 12), ('x', 11, 12)],

    # Door at clipping[11][16] - Central area door
    # Player stands at (16, 10) facing East to see button
    (0, 16, 10, 'E'): [(11, 16), ('x', 17, 10)],

    # Door at clipping[11][20] - East corridor door
    # Player stands at (20, 11) facing North to see button
    (0, 20, 11, 'N'): [(11, 20), ('y', 20, 10)],

    # Door at clipping[16][11] - Western passage door
    # Player stands at (11, 16) facing North to see button
    (0, 11, 16, 'N'): [(16, 11), ('y', 11, 15)],

    # Door at clipping[16][17] - Central-east door
    # Player stands at (17, 16) facing East to see button
    (0, 17, 16, 'E'): [(16, 17), ('x', 18, 16)],

    # Door at clipping[17][20] - East passage door
    # Player stands at (20, 17) facing North to see button
    (0, 20, 17, 'N'): [(17, 20), ('y', 20, 16)],

    # Door at clipping[20][6] - West lower door
    # Player stands at (6, 20) facing North to see button (on west wall)
    (0, 6, 20, 'N'): [(20, 6), ('x', 6, 19)],

    # Door at clipping[21][15] - South central door
    # Player stands at (15, 21) facing North to see button
    (0, 15, 21, 'N'): [(21, 15), ('y', 15, 20)],

    # Door at clipping[22][20] - Southeast door
    # Player stands at (20, 22) facing North to see button
    (0, 20, 22, 'N'): [(22, 20), ('y', 20, 21)],
}


entry_pos = (0, 7, 13, 'N')

levels = [DungeonLevel(environment, walls_x, walls_y, clipping, adornments, switches)]

dungeon = Dungeon(levels, entry_pos)
