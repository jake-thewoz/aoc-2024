import data_getter

data = data_getter.get_data(12).splitlines()

# print(data)

# So we need to find two things:
#   - the area of each region
#   - the perimeter of each region
# We'll look at every tile on the map
#   - if the tile hasn't been visited, we create a new region to track
#       - maybe the id is the letter + str(coord)
#   - then we pass the region, tile, to our search function
#       - look at the four surrounding tiles
#           - add 1 fence for each foreign and out of bounds tile
#           - for each same tile, call the function again with that tile

def survey_plot(region, plot):
    """Takes a region and the current plot, and adds to the area and perimeter accordingly"""
    # This is a necessary check because of backtracking recursion
    if plot in visited_plots: return
    
    # First we add the plot to visited and increment area
    visited_plots.add(plot)
    region['area'] += 1

    # I'll make some row col variables for readability
    row = plot[0]
    col = plot[1]
    adjacent_plots = [
        (row-1, col),
        (row, col+1),
        (row+1, col),
        (row, col-1)
    ]
    foreign_plots = [(y, x) for y, x in adjacent_plots if not 0 <= y < len(mapgrid) or not 0 <= x < len(mapgrid[y]) or mapgrid[y][x] != mapgrid[row][col]]
    # the perimeter for any tile is the number of bad adjacent tiles
    region['perimeter'] += len(foreign_plots)

    next_plots = [(y, x) for y, x in adjacent_plots if (y, x) not in visited_plots and (y, x) not in foreign_plots]
    # we can use a comprehension to loop through all the next_plots
    [survey_plot(region, next_plot) for next_plot in next_plots]
    

# Now for our main program

mapgrid = data.copy()
regions = {}
visited_plots = set()

for y in range(len(mapgrid)):
    for x in range(len(mapgrid[y])):
        if (y, x) not in visited_plots:
            region_id = mapgrid[y][x] + '-' + str(y) + ',' + str(x)
            regions[region_id] = {
                'area': 0,
                'perimeter': 0
            }
            survey_plot(regions[region_id], (y, x))

price = sum([r['area'] * r['perimeter'] for r in regions.values()])

print('The total price for fencing is', price)

# Part Two ---------------------------------------------------------------------

# Actually, I don't think this will be too hard.
# At first It looks pretty scary, but the posts (where fences change direction) equal in 
# number to the fences. Finding the posts isn't that difficult.
# Let's modify the previous function to account for this

def discount_survey(region, plot):
    """Takes a region and the current plot, and adds to the area and perimeter accordingly"""
    # This is a necessary check because of backtracking recursion
    if plot in visited_plots: return
    
    # First we add the plot to visited and increment area
    visited_plots.add(plot)
    region['area'] += 1

    # I'll make some row col variables for readability
    row = plot[0]
    col = plot[1]
    # These are the plots in a + sign around the current plot
    adjacent_plots = [
        (row-1, col),
        (row, col+1),
        (row+1, col),
        (row, col-1)
    ]
    # And these are the complete neighbors, including diagonals
    all_neighbors = [
        (row-1, col),
        (row-1, col+1),
        (row, col+1),
        (row+1, col+1),
        (row+1, col),
        (row+1, col-1),
        (row, col-1),
        (row-1, col-1)
    ]
    # Like last time, we'll track all of the naughty neighbors
    foreign_plots = [(y, x) for y, x in all_neighbors if not 0 <= y < len(mapgrid) or not 0 <= x < len(mapgrid[y]) or mapgrid[y][x] != mapgrid[row][col]]

    # But this time, we'll loop through the neighbors in a plus sign
    for n in range(len(adjacent_plots)):
        current = adjacent_plots[n]
        previous = adjacent_plots[n-1] # thank you python negative indexing!
        # I had to look up how to figure out the diagonal from 3 coordinates, but it works
        diag = (current[0] + previous[0] - row, current[1] + previous[1] - col)

        # There are just two conditions where we'll know a corner exists:
        if current in foreign_plots and previous in foreign_plots:
            # this is a convex corner
            region['posts'] += 1
        elif current not in foreign_plots and previous not in foreign_plots and diag in foreign_plots:
            # this is a concave corner
            region['posts'] += 1

    # Like before, we can make a quick list of the next non-visited neighbors
    next_plots = [(y, x) for y, x in adjacent_plots if (y, x) not in visited_plots and (y, x) not in foreign_plots]
    # we can use a comprehension to loop through all the next_plots
    [discount_survey(region, next_plot) for next_plot in next_plots]

# Now we just need to run the main loop again

mapgrid = data.copy()
regions = {}
visited_plots = set()

for y in range(len(mapgrid)):
    for x in range(len(mapgrid[y])):
        if (y, x) not in visited_plots:
            region_id = mapgrid[y][x] + '-' + str(y) + ',' + str(x)
            regions[region_id] = {
                'area': 0,
                'posts': 0
            }
            discount_survey(regions[region_id], (y, x))

price = sum([r['area'] * r['posts'] for r in regions.values()])

print('The total price for discounted fencing is', price)

# Lessons learned:
# - today, I was really helped by insights into the data/problem
#   - quickly seeing the simplicity in calculating the fences helped
# - for part 2, figuring out how to check for convex/concave corners took some time and thought
#   - but, I saw fairly quickly that the key was finding the corners and not counting the straight lines
# - in the end, I never really used the region_ids I created. Oh well
# - today might be the first time I used a recursive function that doesn't return anything. neat
#   - putting the function calls in a comprehension was useful