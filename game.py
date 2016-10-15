from copy import deepcopy

default_map = [['t', 'l', 'l', 'e'], ['m', 'm', 'l', 'l'], ['l', 'l', 'l', 'p']]

def load_map(map_file):
    map = []
    f = open(map_file)
    data = f.readlines()
    f.close()
    for line in data:
        map += [list(line.strip().split())]
    return map


def map_is_valid(map):
    # checks that map is a rectangular grid and that each entry is valid
    cols = len(map[0])
    for row in map[1:]: #if the map is a 1x1 this will throw an our of bounds exception
        if len(row) != cols:
            return False
    # check that only valid entries exist
    entries = []
    for row in map:
        entries += row
    entries = set(entries)
    for entry in entries:
        if entry not in ['l', 'm', 'p', 't', 'e']:
            return False
    # make sure that a player has been placed on the map, and that there is treasure to collect and walkable land
    if not entries.issuperset({'l', 't', 'p'}):
        return False
    # todo: create a solvability checker to only allow solvable maps
    return True


class Player:
    def __init__(self, r=0, c=0):
        self.r = r
        self.c = c

    def location(self):
        return (self.r, self.c)

    def set_location(self, r, c):
        self.r = r
        self.c = c


class Game:
    def __init__(self, map_file=None):
        if map_file:
            self.map = load_map(map_file)
            if not map_is_valid(self.map):
                print("Error in loaded map, initializing to default")
                self.map = default_map
        else:
            self.map = default_map
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        for i, row in enumerate(self.map):
            try:
                j = row.index('p')
            except ValueError:
                continue
            self.p1 = Player(i, j)
            self.map[i][j] = 'l'

    def visualize(self):
        # Display map in a nice way
        current_map = deepcopy(self.map)
        i, j = self.p1.location()
        current_map[i][j] = 'p'
        print("\nThe map:")
        line = '---'.join(['+']*(self.cols + 1))
        print(line)
        for r in range(self.rows):
            print('|' + '|'.join([(' ' + current_map[r][c] + ' ').center(3) for c in range(self.cols)]) + '|')
            print(line)
        print("Key: t = treasure, l = open land, m = mountains, e = enemy, p = player.")
        print('\n')

    def check_for_end(self):
        i, j = self.p1.location()
        if self.map[i][j] == 't':
            # player wins!
            return 1
        elif self.map[i][j] == 'e':
            # player dies :-(
            return -1
        # keep playing
        return 0

    def move(self, dir):
        valid_moves = []
        i, j = self.p1.location()
        if i >= 1:
            valid_moves += ['u']
        if i < (self.rows - 1):
            valid_moves += ['d']
        if j >= 1:
            valid_moves += ['l']
        if j < (self.cols - 1):
            valid_moves += ['r']
        if dir not in valid_moves:
            # we can only move up down left or right
            # and we can't fall off the map
            # return an error for unrecognised command
            return -1
        # there's too much repetition here, i can probably reduce the amount of typing with better if statements...
        if dir == 'u' and self.map[i-1][j] not in ['m']:
            # if player has chosen to move up, and there isn't a mountain in the way, move up
            self.p1.set_location(i-1, j)
            return 0
        if dir == 'd' and self.map[i+1][j] not in ['m']:
            self.p1.set_location(i+1, j)
            return 0
        if dir == 'l' and self.map[i][j-1] not in ['m']:
            self.p1.set_location(i, j-1)
            return 0
        if dir == 'r' and self.map[i][j+1] not in ['m']:
            self.p1.set_location(i, j+1)
            return 0
        # move not allowed
        return -2

    def game_loop(self):
        # main loop for repeatedly requesting moves
        print("You're playing 'Exciting Adventure Quest'!")
        print("Good luck!")
        while True:
            self.visualise()
            print("Find the treasure! Please choose a move ('u' = up, 'd' = down, 'l' = left, 'r' = right):\n")
            while True:
                m = input().strip()
                outcome = self.move(m)
                if outcome == -1:
                    print("Invalid move! Type 'u', 'd', 'r', or 'l' and make sure you aren't trying to leave the map!")
                elif outcome == -2:
                    print("Invalid move! Check that you aren't trying to climb a mountain...")
                elif outcome == 0:
                    break
            win_state = self.check_for_end()
            if win_state == 1:
                print("You found the treasure! How exciting! And adventurous!")
                break
            if win_state == -1:
                print("You got caught by the evil scary enemy... damn, you really messed this up didn't you?")
                break
        print("Thanks for playing!")
