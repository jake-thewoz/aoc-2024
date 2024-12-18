import data_getter
from collections import deque

data = data_getter.get_data('18').splitlines()

# print(data)

# Okay, so we just build a map and find the shortest path

# map_dimensions = 7
map_dimensions = 71
# how_many_bites = 12
how_many_bites = 1024

start = (0, 0)
end = (map_dimensions-1, map_dimensions-1)

bytes = [(int(byte.split(',')[0]), int(byte.split(',')[1])) for byte in data]
mapgrid = [['.' for _ in range(map_dimensions)] for _ in range(map_dimensions)]

# for obs in obstacles:
for i in range(how_many_bites):
    byte = bytes[i]
    mapgrid[byte[1]][byte[0]] = '#'

# Now we write a BFS function
def find_shortest_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    queue = deque([(*start, 0)])  # (row, col, distance)
    visited = set()
    visited.add(start)
    
    while queue:
        row, col, dist = queue.popleft()
        
        # If we reach the end, return the distance
        if (row, col) == end:
            return dist
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == '.':
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    # If we exhaust the queue without finding the end
    return -1  # No path found

# now we just run the thing
shortest_path = find_shortest_path(mapgrid, start, end)
print('The shortest path is', shortest_path)

# part two -------------------------------------------------------------------------

# pretty easy! hopefully brute-forcing this works

for i in range(how_many_bites, len(bytes)):
    byte = bytes[i]
    mapgrid[byte[1]][byte[0]] = '#'
    shortest_path = find_shortest_path(mapgrid, start, end)
    if shortest_path == -1:
        print('The final straw was', byte)
        break

# Lessons Learned:
#   - sometimes the puzzles are easy!
#   - the deque module is super fast and useful for implementing algorithms
#   - python has an unpacker with *
#       - ie, (*start, 0) from above is the same as (0, 0, 0)