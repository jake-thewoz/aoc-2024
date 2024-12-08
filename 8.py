import data_getter
from itertools import combinations

data = data_getter.get_data(8).splitlines()

# print(data)

# Interesting problem. My first thought is to create a dict of
# every frequency (0-9,a-Z), and make the values a list of coordinates.
# Then, we can go through each frequency (the keys):
#   - create every possible coordinate of antinodes
#   - then, we can filter out antinodes not on the map

map_grid = data.copy()
all_freqs = {}

for row in map_grid:
    for char in row:
        # python's "isalnum", or "Is alpha numeric" is perfect for this
        if char.isalnum():
            if char not in all_freqs:
                all_freqs[char] = [[map_grid.index(row), row.index(char)]]
            else: # char is in all_freqs
                all_freqs[char].append([map_grid.index(row), row.index(char)])

# Now we'll go through each freq, and get every pair of coords
# combinations is a good tool for making the unique pairs
every_pair = {freq: list(combinations(coord, 2)) for freq, coord in all_freqs.items()}

def find_antinodes(pair):
    """Takes two coordinates and returns the possible antinodes"""
    antinodes = []
    # First I'll find the 'slope'
    slope = [pair[1][0] - pair[0][0], pair[1][1] - pair[0][1]]
    # then I'll add it to the second coord to generate an antinode
    antinodes.append([slope[0] + pair[1][0], slope[1] + pair[1][1]])
    # then I'll subtract from first coord
    antinodes.append([pair[0][0] - slope[0], pair[0][1] - slope[1]])

    # might as well filter out bad coords before returning
    # Note- had an off-by-one error with len(map_grid) before -1. Rookie mistake!
    filtered_nodes = [
        node for node in antinodes if all(0 <= x <= len(map_grid)-1 for x in node)
    ]

    return filtered_nodes

# now we loop and use our function
result = []
for freq, pairs in every_pair.items():
    for pair in pairs:
        result.append(find_antinodes(pair))

# Now I need to flatten and count the result
# Ah, almost forgot that it needs to be UNIQUE coords!
set_result = set([tuple(pair) for nested_pairs in result for pair in nested_pairs])
print('The number of antinodes in the map are', len(set_result))

# Part Two ---------------------------------------------------------------------------------------------

# Okay, I don't think this will be too difficult. We just need to modify our calculation function
# we can still use the map_grid and every_pair from part one without modification.

def find_resonant_antinodes(pair):
    """Takes two coords and returns all the resonant antinodes"""
    antinodes = []
    antinodes.append(pair[0])
    antinodes.append(pair[1])
    # First I'll find the 'slope', like before
    slope = [pair[1][0] - pair[0][0], pair[1][1] - pair[0][1]]
    # then we'll loop in the positive slope direction, collecting antinodes
    next_node = pair[1].copy()
    while True:
        next_node = [next_node[0] + slope[0], next_node[1] + slope[1]]
        if any(x < 0 or x >= len(map_grid) for x in next_node):
            break
        else:
            antinodes.append(next_node)
    # then we'll loop in the negative direction
    next_node = pair[0].copy()
    while True:
        next_node = [next_node[0] - slope[0], next_node[1] - slope[1]]
        if any(x < 0 or x >= len(map_grid) for x in next_node):
            break
        else:
            antinodes.append(next_node)
    # since filtering is baked-in to this new method, we just return the nodes
    return antinodes

# Now we loop again, like before
result = []
for freq, pairs in every_pair.items():
    for pair in pairs:
        result.append(find_resonant_antinodes(pair))

# Now we flatten and filter by uniques
set_result = set([tuple(pair) for nested_pairs in result for pair in nested_pairs])
print('The number of resonant antinodes in the map are', len(set_result))

# Note, I had some issues with my find_resonant_antinodes() function:
#   - I needed to completely reassign the values of next_node, not do it one at a time
#   - I also needed to do .copy() on the initial value, so I didn't modifiy the original