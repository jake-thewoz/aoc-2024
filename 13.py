import data_getter
import re

data = data_getter.get_data(13).splitlines()

# print(data)

# There must be some way to elegantly do this, but I'm imaginging brute force.

# First, let's turn our data into a list of dicts
machines = [{}]
for i in range(len(data)):
    if i % 4 == 0 or i % 4 == 1 or i % 4 == 2:
        nums = re.findall(r'\d+', data[i])       
        machines[-1][data[i].split(':')[0]] = list(map(int, nums))
    else:
        machines.append({})

# print(machines)

# Now let's brute force this thang
cost = 0
for machine in machines:
    found = False
    for a in range(101):
        a_mov = [a * num for num in machine['Button A']]
        if a_mov[0] > machine['Prize'][0] or a_mov[1] > machine['Prize'][1]: break
        for b in range(101):
            coord = a_mov
            b_mov = [b * num for num in machine['Button B']]
            coord = [coord[0] + b_mov[0], coord[1] + b_mov[1]]
            if coord[0] > machine['Prize'][0] or coord[1] > machine['Prize'][1]: break
            if coord == machine['Prize']:
                cost += (3 * a) + b
                found = True
            if found: break
        if found: break

print('Total cost is',cost)

# Part Two -------------------------------------------------------------------------

# Well, there goes the brute force solution
# I know there's some kind of algebra solution, since a*(x) + b*(x) = prize[x], and a*(y) + b*(y) = prize[y]
# This problem can be represented using matrices

# First, lets correct our machines
machines = [{'Button A': m['Button A'], 'Button B': m['Button B'], 'Prize': [m['Prize'][0] + 10000000000000, m['Prize'][1] + 10000000000000]} for m in machines]

# That didn't work either. I've now given up, and looking for help  on reddit...
# Turns out there's a very simple equation for this!
# b=(py*ax-px*ay)/(by*ax-bx*ay), a=(px-b*bx)/ax
# I'm going to try to implement this in the for loop, no function needed
cost = 0
for m in machines:
    # to make it easier to read, I'll assign variables
    ax, ay = m['Button A'][0], m['Button A'][1]
    bx, by = m['Button B'][0], m['Button B'][1]
    px, py = m['Prize'][0], m['Prize'][1]

    # First we need to check the modulo to make sure the solutions are ints
    if (py*ax - px*ay) % (by*ax - bx*ay) == 0:
        # Then it's an int for b!
        b = (py*ax - px*ay) // (by*ax - bx*ay)
        if (px - b*bx) % ax == 0:
            # then it's also an int for a!
            a = (px - b*bx) // ax
            cost += (a*3) + b

print('The crazy cost is',cost)

# Lessons Learned:
#   - my brute force was effective, and didn't take too long to write
#   - I should've known it wouldn't work for part two
#   - For part two, I tried two solutions using the sympy library:
#       - I tried matrix mupltiplication
#       - I tried its diophantine and solve functions
#   - neither really worked, and I'm not sure why
#   - Eventually, I went to reddit
#       - I probably could've found this algebraic equation if I'd taken the time to write it out
#       - it feels dirty to use such a good hint, but I could see it was a simple algebra problem