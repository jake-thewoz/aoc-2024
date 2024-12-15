import data_getter
import time
import os

data = data_getter.get_data(15).splitlines()

# print(data)

# I guess we just start doing this!
# I think I'll try displaying the grid every time
#   - get the data in a good format
#   - loop through the moves
#       - if next space is ., move to it
#       - if next space is #, don't move
#       - if next is O, check if we can push
#           - if we can push, we push
#   - calculate results

# Wrangle data
split_index = data.index('')
mapgrid = [list(line) for line in data[:split_index]]
moves = ''.join(data[split_index+1:])
robot_pos = [(mapgrid.index(y),y.index(x)) for y in mapgrid for x in y if x == '@'][0]

directions = {
    '<': (0, -1),
    '>': (0, 1),
    '^': (-1, 0),
    'v': (1, 0)
}

# helper functions
def print_mapgrid():
    [print(''.join(line)) for line in mapgrid]

def check_next_space(pos, dir):
    return mapgrid[pos[0]+dir[0]][pos[1]+dir[1]]

def check_to_push(pos, dir):
    i = 2
    while True:
        next_pos = (pos[0]+(dir[0]*i), pos[1]+(dir[1]*i))
        if not 0 <= next_pos[0] < len(mapgrid) or not 0 <= next_pos[1] < len(mapgrid[0]):
            return False
        elif mapgrid[next_pos[0]][next_pos[1]] == '#':
            return False
        elif mapgrid[next_pos[0]][next_pos[1]] == '.':
            opposite_dir = (dir[0]*-1, dir[1]*-1)
            while True:
                prev_pos = next_pos
                next_pos = (prev_pos[0]+(opposite_dir[0]), prev_pos[1]+(opposite_dir[1]))
                if mapgrid[next_pos[0]][next_pos[1]] == '@':
                    mapgrid[prev_pos[0]][prev_pos[1]] = '@'
                    mapgrid[next_pos[0]][next_pos[1]] = '.'
                    return True
                else:
                    mapgrid[prev_pos[0]][prev_pos[1]] = 'O'
        i += 1

# now we loop
for move in moves:
    dir = directions[move]
    # os.system('cls')
    # print(move)
    next_space = check_next_space(robot_pos, dir)
    if next_space == '.':
        mapgrid[robot_pos[0]][robot_pos[1]] = '.'
        robot_pos = (robot_pos[0] + dir[0], robot_pos[1] + dir[1])
        mapgrid[robot_pos[0]][robot_pos[1]] = '@'
    elif next_space == '#':
        1 + 1 # do nothing
    elif next_space == 'O':
        pushed = check_to_push(robot_pos, dir)
        if pushed:
            robot_pos = [(mapgrid.index(y),y.index(x)) for y in mapgrid for x in y if x == '@'][0]
    # print_mapgrid()
    # time.sleep(0.017)
    
gps_sum = sum([100 * y_idx + x_idx for y_idx, y in enumerate(mapgrid) for x_idx, x in enumerate(y) if x == 'O'])
print(gps_sum)




