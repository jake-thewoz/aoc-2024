import data_getter
from collections import deque

data = data_getter.get_data('20').splitlines()

# print(data)

# So we need to figure out every cheat that saves 100 moves
# We can start by finding the main path using a BFS function
# from a previous puzzle day.

# data wrangling
mapgrid = data.copy()
start = [(mapgrid.index(y), y.index(x)) for y in mapgrid for x in y if x == 'S'][0]
end = [(mapgrid.index(y), y.index(x)) for y in mapgrid for x in y if x == 'E'][0]

# our BFS algorithm
def find_path_bfs(grid, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    queue = deque([(start)])
    visited = set()
    predecessors = {} # we use a predecessor dictionary, which we'll build the final path from

    visited.add(start)
    predecessors[start] = None # the start tile has no predecessor
    
    while queue:
        current = queue.popleft()
        
        # If we reach the end, return the distance
        if current == end:
            # here we reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = predecessors[current]
            path.reverse()
            return path
        
        # Explore neighbors
        for dir in directions:
            next_tile = current[0] + dir[0], current[1] + dir[1]
            if next_tile not in visited and grid[next_tile[0]][next_tile[1]] == '.' or grid[next_tile[0]][next_tile[1]] == 'E':
                visited.add(next_tile)
                predecessors[next_tile] = current # the next tile's predecessor is the current tile
                queue.append(next_tile)
    
    # If we exhaust the queue without finding the end
    return -1  # No path found

path = find_path_bfs(mapgrid, start, end)

# Now that we have the path, I think we can find all the shortcuts with a simple algorithm.
# The key insight is that any shortuct will be 2 tiles away from where it's shortcutting to.
# So to find all the ones 100+ tiles away:
#   - start from the end of our path
#       - loop all the tiles that are 100+ indexes away from this tile
#       - if any are 2 away from either y or x, they count
#   - loop until we're looking at the path[100] tile.

# CORRECTION! To account for actually travelling to the new location,
# we need to up our 'savings' by 2, since we travel two tiles to get there

# savings = 14
savings = 102

count = 0
counted = set()
for i in range(len(path)-1, savings-1, -1):
    current = path[i]
    for j in range(i-savings, -1, -1):
        tester = path[j]
        pair = frozenset([current, tester])
        if ((tester[0] == current[0] and abs(tester[1] - current[1]) == 2)
            or (tester[1] == current[1] and abs(tester[0] - current[0]) == 2)
            and (pair not in counted)):
            count += 1
            counted.add(pair)

print(f'The number of cheats that saves {savings-2} picoseconds is {count}')

# part two -----------------------------------------------------------------------------------

# Okay, I think I can do this by just modifying my previous for loop
# We can figure out if a square is reachable in 20 picoseconds pretty easily...
#   - hopefully the cheats don't need to STAY in the walls the whole cheat...
#   - this is true!
# The issue arises in that we need to add back in the steps we took to get to
# the path. This was a constant when we could only cheat with two steps, but now
# we'll need to actually calculate this in our loops.

# savings = 72
savings = 100

count = 0
counted = set()
for i in range(len(path)-1, savings-1, -1):
    current = path[i]
    for j in range(i-savings, -1, -1):
        tester = path[j]
        pair = frozenset([current, tester])
        cheat_steps = abs(tester[0] - current[0]) + abs(tester[1] - current[1])
        if (cheat_steps <= 20
            and i-j-cheat_steps >= savings
            and (pair not in counted)):
            count += 1
            counted.add(pair)

print(f'The number of 20-length cheats that saves {savings} picoseconds is {count}')

# Lessons Learned:
#   - to make a BFS function that returns the path requires:
#       - tracking the previous (current) tile
#       - you create the path in reverse once you find the end
#   - a shortcut isn't tough to figure out if you've got an array of the path
#       - we can use the indexes to figure out the savings
#       - we can figure out how far away the points are by looking at the coordinates themselves