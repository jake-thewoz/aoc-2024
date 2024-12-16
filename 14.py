import data_getter

data = data_getter.get_data(14).splitlines()

# print(data)

# Interesting. I think we can solve this without brute forcing the movement
# if we:
#   - multiply the velocities by the count
#   - add the starting position
#   - modulus by the dimensions of the grid
# This should give us the coordinates. Then we can filter by grid and multiply

# First step is to get our data into a usable format
robots = []
for line in data:
    p = line.split(' ')[0].split('=')[1].split(',')
    v = line.split(' ')[1].split('=')[1].split(',')
    robots.append(
        {
            'p': (int(p[0]), int(p[1])),
            'v': (int(v[0]), int(v[1]))
        }
    )

# here are our grid dimensions
# width = 11
# height = 7
width = 101
height = 103

# and our seconds
seconds = 100

# Now we add the endpoint of the robots
for robot in robots:
    ex = (seconds * robot['v'][0] + robot['p'][0]) % width
    ey = (seconds * robot['v'][1] + robot['p'][1]) % height
    if ex < 0:
        ex = width - ex
    if ey < 0:
        ey = height - ey
    robot['ep'] = (ex, ey)

# Let's make some quadrants to add up the robots
nw = ne = sw = se = 0

for robot in robots:
    if robot['ep'][0] < width // 2:
        if robot['ep'][1] < height // 2:
            nw += 1
        elif robot['ep'][1] > height // 2:
            sw += 1
    elif robot['ep'][0] > width // 2:
        if robot['ep'][1] < height // 2:
            ne += 1
        elif robot['ep'][1] > height // 2:
            se += 1

safety = nw*ne*sw*se

print('The safety factor is',safety)

# part two ----------------------------------------------------------------

# I guess I'll just brute force this

# display = [[0 for _ in range(width)] for _ in range(height)]

# [print(''.join(map(str, line))) for line in display]

# okay, now I need to change the position one by one, and use a keystroke to do it

for i in range(100000):
    # display = [[0 for _ in range(width)] for _ in range(height)]
    for robot in robots:
        ex = (i * robot['v'][0] + robot['p'][0]) % width
        ey = (i * robot['v'][1] + robot['p'][1]) % height
        if ex < 0:
            ex = width - ex
        if ey < 0:
            ey = height - ey
        robot['cp'] = (ex, ey)
        # display[robot['cp'][1]][robot['cp'][0]] += 1

    nw = ne = sw = se = 0
    
    for robot in robots:
        if robot['cp'][0] < width // 2:
            if robot['cp'][1] < height // 2:
                nw += 1
            elif robot['cp'][1] > height // 2:
                sw += 1
        elif robot['cp'][0] > width // 2:
            if robot['cp'][1] < height // 2:
                ne += 1
            elif robot['cp'][1] > height // 2:
                se += 1
    
    if nw == ne and sw == se:
        print('i=',i)
        break
    # [print(''.join(map(str, line))) for line in display]
    # print('i=',i)
    # input()
