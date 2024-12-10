import data_getter

data = data_getter.get_data(10).splitlines()

# print(data)

# Okay. Not sure how exactly I'll do this.
# First step is to get all the trailheads

trailheads = [(y, x) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == '0']

# Now to count up the scores of the trailheads.
# I think we'll need functions with a flavor of recursion
# Algorithm:
#   - start at a trailhead
#   - find all adjacent tiles that are +1 of current coord
#       - change current coord to new coord
#       - repeat step 2^
#       - repeat step 3^
#       ...
#       - if current coord is 9, add 1 to the score

mapgrid = data.copy()

def count_scores(mapgrid, row, col, visited_nines=[]):
    # first, our base case
    if mapgrid[row][col] == '9':
        visited_nines.append((row,col))
        return 1

    # then, we'll look at all adjacent tiles
    # if they are valid, we call recursively for them
    adjacent_tiles = [
        (row-1, col),
        (row, col+1),
        (row+1, col),
        (row, col-1)
    ]
    bounded_adj_tiles = [(y, x) for y, x in adjacent_tiles if 0 <= y < len(mapgrid) and 0 <= x < len(mapgrid[0])]
    next_tiles = [(y, x) for y, x in bounded_adj_tiles if int(mapgrid[y][x]) == int(mapgrid[row][col]) + 1 and (y, x) not in visited_nines]

    # now we have a list of the next tiles to check
    if len(next_tiles) == 0:
        return 0
    
    # and here is our recursive loop part
    count = 0
    for tile in next_tiles:
        count += count_scores(mapgrid, tile[0], tile[1], visited_nines)
    return count

# now we just need to loop through our trailheads
total_scores = 0
for trailhead in trailheads:
    total_scores += count_scores(mapgrid, trailhead[0], trailhead[1], [])

print('The total scores is', total_scores)

# count_scores(mapgrid, trailheads[-2][0], trailheads[-2][1])

# part two -----------------------------------------------------------

# Wow! I already got this by accident when trying to make part one
# I just need to remove the 'visited_nines' stipulation
# I'll just copy the first function and tweak it, then loop again

def count_ratings(mapgrid, row, col):
    # first, our base case
    if mapgrid[row][col] == '9':
        return 1

    # then, we'll look at all adjacent tiles
    # if they are valid, we call recursively for them
    adjacent_tiles = [
        (row-1, col),
        (row, col+1),
        (row+1, col),
        (row, col-1)
    ]
    bounded_adj_tiles = [(y, x) for y, x in adjacent_tiles if 0 <= y < len(mapgrid) and 0 <= x < len(mapgrid[0])]
    next_tiles = [(y, x) for y, x in bounded_adj_tiles if int(mapgrid[y][x]) == int(mapgrid[row][col]) + 1]

    # now we have a list of the next tiles to check
    if len(next_tiles) == 0:
        return 0
    
    # and here is our recursive loop part
    rating = 0
    for tile in next_tiles:
        rating += count_ratings(mapgrid, tile[0], tile[1])
    return rating

# now we just need to loop through our trailheads
total_ratings = 0
for trailhead in trailheads:
    total_ratings += count_ratings(mapgrid, trailhead[0], trailhead[1])

print('The total ratings are', total_ratings)