import data_getter

data = data_getter.get_data(4).splitlines()

# print(data)
# print(len(data))
# print(len(data[0]))

# Okay, one of these.
# Here's how I think we should go about this:
#   - loop through each character, looking for Xs
#   - when we find an X, send the location to a function
#   - this function will check every relevant direction
#       - a relevant direction can be figured out based on the X's location

# note- it makes me nervous that the examples in part 1 replace irrelevant characters
# with periods. Hopefully that's not relevant in part 2...

def get_directions(x_loc):
    """This takes a location as input, and returns vectors for every valid direction."""
    # these are all our posssible directions, starting at 12pm and going clockwise
    directions = [
        [-1, 0],
        [-1, 1],
        [0, 1],
        [1, 1],
        [1, 0],
        [1, -1],
        [0, -1],
        [-1, -1],
    ]

    # now I'll filter the directions down, based on the values of y and x in x_loc
    if x_loc[0] < 3:
        directions = list(filter(lambda dir: dir[0] != -1, directions))
    if x_loc[0] > 136:
        directions = list(filter(lambda dir: dir[0] != 1, directions))
    if x_loc[1] < 3:
        directions = list(filter(lambda dir: dir[1] != -1, directions))
    if x_loc[1] > 136:
        directions = list(filter(lambda dir: dir[1] != 1, directions))
    
    return directions

def count_xmas(x_loc, directions):
    """This takes a location and a list of directions, returns a count of all XMASs"""
    count = 0
    xmas = 'MAS'
    for direction in directions:
        loc = x_loc.copy()
        match = True
        for i in range(3):
            # first we move our location with the direction
            loc = list(map(lambda coord, dir: coord + dir, loc, direction))
            # then we check if the letter is correct
            if data[loc[0]][loc[1]] != xmas[i]:
                match = False
                break
        count += 1 if match else 0
    
    return count

# Now that we have our helper functions, all we need to do is loop through
# the data, looking for Xs

count = 0
for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == 'X':
            directions = get_directions([y, x])
            count += count_xmas([y, x], directions)

print("The number of XMASs is ", count)

# part 2 -----------------------------------------------------------------------

# wow, tricky