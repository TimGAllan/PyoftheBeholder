class Player(object):

    def __init__(self, dungeon):
        self.level = dungeon.entry_pos[0]
        self.x = dungeon.entry_pos[1]
        self.y = dungeon.entry_pos[2]
        self.direction = dungeon.entry_pos[3]
        self.dungeon_pos = (self.level, self.x, self.y, self.direction)
        self.level_pos = (self.x, self.y, self.direction)

    def move(self, clipping, key):
        """
        Attempt to move or rotate the player.

        Args:
            clipping: 2D grid of walkable/blocked cells
            key: Key pressed ('w','a','s','d' for movement, 'q','e' for rotation)

        Returns:
            bool: True if the player moved or rotated, False if blocked
        """
        moves = {
            'w': {'N': [0, -1, 'N'], 'S': [0, +1, 'S'], 'E': [+1, 0, 'E'], 'W': [-1, 0, 'W']},
            's': {'N': [0, +1, 'N'], 'S': [0, -1, 'S'], 'E': [-1, 0, 'E'], 'W': [+1, 0, 'W']},
            'a': {'N': [-1, 0, 'N'], 'S': [+1, 0, 'S'], 'E': [0, -1, 'E'], 'W': [0, +1, 'W']},
            'd': {'N': [+1, 0, 'N'], 'S': [-1, 0, 'S'], 'E': [0, +1, 'E'], 'W': [0, -1, 'W']},
            'q': {'N': [0, 0, 'W'], 'S': [0, 0, 'E'], 'E': [0, 0, 'N'], 'W': [0, 0, 'S']},
            'e': {'N': [0, 0, 'E'], 'S': [0, 0, 'W'], 'E': [0, 0, 'S'], 'W': [0, 0, 'N']}
        }

        if clipping[self.y + moves[key][self.direction][1]][self.x + moves[key][self.direction][0]] in [1, 3]:
            print("You can't go that way")
            return False
        else:
            self.x += moves[key][self.direction][0]
            self.y += moves[key][self.direction][1]
            self.direction = moves[key][self.direction][2]
            self.dungeon_pos = (self.level, self.x, self.y, self.direction)
            self.level_pos = (self.x, self.y, self.direction)
            print(self.dungeon_pos)
            return True

    def click_switch(self, switches, adornments, clipping):
        if self.dungeon_pos in switches.keys():
            x = switches[self.dungeon_pos][0][0]
            y = switches[self.dungeon_pos][0][1]
            if clipping[x][y] == 3:
                clipping[x][y] = 2
                adornments[switches[self.dungeon_pos][1]] = 'LeverDown'
            else:
                clipping[x][y] = 3
                adornments[switches[self.dungeon_pos][1]] = 'LeverUp'
