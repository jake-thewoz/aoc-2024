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

# wow.
# I think I've got it! Blocking opportunities come from two situations:
#   - when you cross a path you've been on 
#   - when the next non '.' tile to your right is either a turn or a line in the direction you're looking!
# This requires me to rewrite part one, so I'll reset variables and go again down here.

map_grid = [list(row) for row in data]
game_over = False
direction = [-1, 0]
opportunities = 0
guard_position = [[map_grid.index(row), row.index(char)] for row in map_grid for char in row if char == '^'][0]

def see_loop(position, direction, original_position, times=1):
    if times > 900:
        return False
    loop = False
    # first we turn our head to the right
    direction = [direction[1], -direction[0]]
    # then we scan ahead, looking for the next non '.'
    still_looking = True
    while still_looking:
        new_position = [position[0] + direction[0], position[1] + direction[1]]
        # checking bounds
        if (   new_position[0] < 0
            or new_position[1] < 0
            or new_position[0] >= len(map_grid)
            or new_position[1] >= len(map_grid[0])
        ):
            still_looking = False
        else:
            if new_position == original_position:
                loop = True
                still_looking = False
            elif map_grid[new_position[0]][new_position[1]] == '+':
                loop = True
                still_looking = False
            elif map_grid[new_position[0]][new_position[1]] == '^':
                loop = True
                still_looking = False
            elif (map_grid[new_position[0]][new_position[1]] == '#'
                and map_grid[position[0]][position[1]] == 'X'):
                loop = True
                still_looking = False
            elif map_grid[new_position[0]][new_position[1]] == '#':
                loop = see_loop(position, direction, original_position, times+1)
                still_looking = False
        position = new_position

    return loop

while not game_over:
    new_direction = get_direction(guard_position, direction)
    turned = True if new_direction != direction else False
    direction = new_direction
    new_position = [guard_position[0] + direction[0], guard_position[1] + direction[1]]
    # first we'll check if the new position is off the map
    if (   new_position[0] < 0
        or new_position[1] < 0
        or new_position[0] >= len(map_grid)
        or new_position[1] >= len(map_grid[0])
    ):
        game_over = True
    elif turned:
        # don't check for loop
        continue
    else:
        # first we'll check if there's a loop made from turning right
        opportunities += 1 if see_loop(new_position, direction, new_position) else 0
        # next, we'll paint the map, painting + if we turned here
        map_grid[new_position[0]][new_position[1]] = '^'
        map_grid[guard_position[0]][guard_position[1]] = '+' if turned else 'X'

        guard_position = new_position

# [print(''.join(row)) for row in map_grid]

print('The number of obstruction possibilities amount to', opportunities)