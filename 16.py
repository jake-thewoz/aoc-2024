import data_getter
import sys

data = data_getter.get_data(16).splitlines()

# print(data)

# I think I can do this by collecting all possible paths with DFS,
# then calculate the value and get the lowest one.

mapgrid = data.copy()
directions = ((0,1),(1,0),(0,-1),(-1,0))
all_paths = []
start = [(mapgrid.index(y), y.index(x)) for y in mapgrid for x in y if x == 'S'][0]
goal = [(mapgrid.index(y), y.index(x)) for y in mapgrid for x in y if x == 'E'][0]

def find_paths_with_pruning(maze, start, goal, best_score=float('inf')):

    def dfs(current, path, direction, score):
        nonlocal best_score

        # Stop early if the current turns exceed the best score
        if score >= best_score:
            return

        if current == goal:
            yield path, score
            best_score = min(best_score, score)  # Update the best score
            return

        for new_dir in directions:
            new_row, new_col = current[0] + new_dir[0], current[1] + new_dir[1]
            neighbor = (new_row, new_col)

            # Check if the neighbor is valid
            if maze[new_row][new_col] != '#' and neighbor not in path:
                # Determine if this move causes a turn
                new_score = score + (1001 if direction != new_dir else 1)

                # Recur with the new state
                yield from dfs(neighbor, path + [neighbor], new_dir, new_score)

    # Start the DFS generator
    yield from dfs(start, [start], None, 0)

def find_best_path(maze, start, goal):
    best_path = None
    best_score = float('inf')

    for path, score in find_paths_with_pruning(maze, start, goal, best_score):
        if score < best_score:
            best_path = path
            best_score = score

    return best_path, best_score

sys.setrecursionlimit(10000)
best_path, best_score = find_best_path(mapgrid, start, goal)
print(best_score)