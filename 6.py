import data_getter

data = data_getter.get_data(6).splitlines()

# print(data)

# Okay, not too bad. Let's ignore the changing character of ^,>,<,v
# I think we can accomplish this by looping:
#   - check the position in front of the guard
#       - if it's an obstacle, turn right
#           - maybe check if the new direction has an obstacle
#       - if it's off the map, end the loop
#           - count all the Xs on the map
#   - now that it's good, move the guard to the new position
#   - change the previous position to an X

map_grid = [list(row) for row in data]
game_over = False
direction = [-1, 0]
crosses = 0
# practicing list comprehensions...
guard_position = [[map_grid.index(row), row.index(char)] for row in map_grid for char in row if char == '^'][0]

def get_direction(current_position, direction):
    """This takes the current position and direction, and returns the new direction (if changed)"""
    new_position = [current_position[0] + direction[0], current_position[1] + direction[1]]
    if map_grid[new_position[0]][new_position[1]] == '#':
        direction = [direction[1], -direction[0]]
        new_position = [current_position[0] + direction[0], current_position[1] + direction[1]]
        if map_grid[new_position[0]][new_position[1]] == '#':
            direction = [direction[1], -direction[0]]

    return direction

while not game_over:
    direction = get_direction(guard_position, direction)
    new_position = [guard_position[0] + direction[0], guard_position[1] + direction[1]]
    # first we'll check if the new position is off the map
    if (   new_position[0] < 0
        or new_position[1] < 0
        or new_position[0] >= len(map_grid)
        or new_position[1] >= len(map_grid[0])
    ):
        # oops! forgot to turn the final space into an X
        map_grid[guard_position[0]][guard_position[1]] = 'X'
        game_over = True
    else:
        # now we'll paint the map!
        map_grid[new_position[0]][new_position[1]] = '^'
        map_grid[guard_position[0]][guard_position[1]] = 'X'
        guard_position = new_position

# Now we just need to count all the Xs in the map
total_Xs = sum(row.count('X') for row in map_grid)
# [print(''.join(row)) for row in map_grid]

print('The total distinct positions travelled was', total_Xs)

# part two ----------------------------------------------------------------------------------------


# Part Two ----- Fresh Start

# every turn, we need to do the following
#   - look at the next square
#       - if the next square is #, we need to turn
#           - we check again, because we may need to turn twice
#       - if the next square is ., we need to check for a loop
#           - we start by saving the start position
#           - maybe we make a copy of the map, with one new obstacle in our way 
#           - then we follow the rules:
            #   - look at the next square
            #       - if the next square is #, we need to turn
            #           - we check again, because we may need to turn twice
            #       - if the next square is ., we move forwards
            #       - if the next square is out of bounds, there's no loop
            #       - if the next square is our start position, there's a loop
#   - move to the next square

def check_next_square(pos, direction, map_v):
    """Takes a position and direction, and returns the contents of the next square"""
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    if (   new_pos[0] < 0
        or new_pos[1] < 0
        or new_pos[0] >= len(map_v)
        or new_pos[1] >= len(map_v[0])
    ):
        return 'Z' # we'll use this for out of bounds
    elif map_v[new_pos[0]][new_pos[1]] == '#':
        return '#'
    elif map_v[new_pos[0]][new_pos[1]] == '.':
        return '.'
    elif map_v[new_pos[0]][new_pos[1]] == '^':
        [print(''.join(line)) for line in map_v]
        quit()

def turn(direction):
    """Takes a direction, and turns it to the right"""
    new_direction = [direction[1], -direction[0]]
    return new_direction

def move_forward(pos, direction, map_v):
    map_v[pos[0]][pos[1]] = '.'
    map_v[pos[0] + direction[0]][pos[1] + direction[1]] = '^'
    new_pos = [pos[0] + direction[0],pos[1] + direction[1]]
    return new_pos

def check_for_loop(start_pos, direction):
    map_copy = map_grid.copy()
    map_copy[start_pos[0] + direction[0]][start_pos[1] + direction[1]] = '#'
    check_over = False
    current_pos = start_pos
    visited_vectors = set()
    while not check_over:
        next_square = check_next_square(current_pos, direction, map_copy)
        current_vector = tuple(current_pos + direction)
        if current_vector in visited_vectors:
            map_copy[current_pos[0]][current_pos[1]] = '.'
            return True
        elif next_square == '#':
            direction = turn(direction)
            continue
        elif next_square == '.':
            visited_vectors.add(current_vector)
            current_pos = move_forward(current_pos, direction, map_copy)
            continue
        elif next_square == 'Z':
            map_copy[current_pos[0]][current_pos[1]] = '.'
            return False
            
map_grid = [list(row) for row in data]
game_over = False
loop_count = 0
current_pos = [[map_grid.index(row), row.index(char)] for row in map_grid for char in row if char == '^'][0]
direction = [-1, 0]

while not game_over:
    next_square = check_next_square(current_pos, direction, map_grid)
    if next_square == '#':
        direction = turn(direction)
        continue
    elif next_square == '.':
        if check_for_loop(current_pos, direction):
            loop_count += 1
        current_pos = move_forward(current_pos, direction, map_grid)
    elif next_square == 'Z':
        game_over = True

print('loop count', loop_count)