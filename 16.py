import data_getter
from heapq import heappop, heappush

data = data_getter.get_data('16').splitlines()

# print(data)

# I think I can do this by collecting all possible paths with DFS,
# then calculate the value and get the lowest one.

mapgrid = data.copy()
start = [(mapgrid.index(y), y.index(x)) for y in mapgrid for x in y if x == 'S'][0]
goal = [(mapgrid.index(y), y.index(x)) for y in mapgrid for x in y if x == 'E'][0]

# let's start fresh, this time using BFS
def find_cheapest_path_bfs(grid, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    # Priority queue: (total_cost, x, y, direction_index)
    # Start with cost=0, starting point, and direction is right (0)
    pq = [(0, *start, 0)] # cost needs to be first element for the priority queue to sort on the cheapest!
    visited = set()  # Tracks (y, x, direction)

    while pq:
        total_cost, y, x, dir_idx = heappop(pq)
        
        # If we reach the end, return the distance
        if (y, x) == end:
            return total_cost

        # Check if we've visited before
        if (y, x, dir_idx) in visited:
            continue
        visited.add((y, x, dir_idx))
        
        # Explore neighbors
        for i, (dy, dx) in enumerate(directions):
            ny, nx = dy + y, dx + x
            if grid[y][x] != '#':
                move_cost = 1 if dir_idx == i else 1001
                new_cost = move_cost + total_cost

                # push the new state into the priority queue
                heappush(pq, (new_cost, ny, nx, i))
    
    # If we exhaust the queue without finding the end
    return -1  # No path found
    
# now we find the lowest cost
cost = find_cheapest_path_bfs(mapgrid, start, goal)
print('The cheapest cost is',cost)