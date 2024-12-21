import data_getter
from functools import cache
from itertools import chain

data = data_getter.get_data('21').splitlines()

# print(data)

# wow, this is interesting...
# I think we can do this by creating coordinates for both
# the numpad and the dpad

# data wrangling ------------------------------------------

codes = [tuple(datum) for datum in data]

# constants -----------------------------------------------
numpad = {
    '7': (0,0), '8': (0,1), '9': (0,2),
    '4': (1,0), '5': (1,1), '6': (1,2),
    '1': (2,0), '2': (2,1), '3': (2,2),
                '0': (3,1), 'A': (3,2)
}

printpad = {
                (-1,0):'^', 'A': 'A',
    (0,-1):'<', (1,0):'v', (0,1):'>'
}
# maybe storing them as their (y,x) values is better
dpad = {
                  (-1,0): (0,1),  'A' : (0,2),
    (0,-1): (1,0), (1,0): (1,1), (0,1): (1,2),
}

# helper functions ---------------------------------------------------

# now we need to calculate the 'gaps' between the numbers.
# to calculate the instructions for a robot to command another
# to push the buttons, it's really about finding the difference
# between the numbers.

@cache
def sign(x):
    """Takes any integer and returns 1 if positive, -1 if neg, 0 if 0"""
    return x // abs(x) if x != 0 else 0

memo_table = {}

@cache
def expand_tuple(tup, pad, danger=False):
    """This takes the difference between two points, and expand it into one-step moves"""
    if pad == 'dpad' and tup in memo_table:
        return memo_table[tup]
    part1 = []
    part2 = []
    # we'll start with the default optimization
    # I discovered that we need to prioritize < over ^ over v over >
    if sign(tup[1]) == -1:
        part1 = [(0,sign(tup[1]))] * abs(tup[1])
        part2 = [(sign(tup[0]),0)] * abs(tup[0])
    elif sign(tup[0]) == -1:
        part1 = [(sign(tup[0]),0)] * abs(tup[0])
        part2 = [(0,sign(tup[1]))] * abs(tup[1])
    elif sign(tup[0]) == 1:
        part1 = [(sign(tup[0]),0)] * abs(tup[0])
        part2 = [(0,sign(tup[1]))] * abs(tup[1])
    elif sign(tup[1]) == 1:
        part1 = [(0,sign(tup[1]))] * abs(tup[1])
        part2 = [(sign(tup[0]),0)] * abs(tup[0])
    else: # nothing else matters
        part1 = [(sign(tup[0]),0)] * abs(tup[0])
        part2 = [(0,sign(tup[1]))] * abs(tup[1])

    # but here, we'll map out our exceptions to the general rules above
    if pad == 'numpad':
        if tup[0] > 0 and tup[1] > 0 and danger:
            # go right first
            part1 = [(0,1)] * tup[1]
            part2 = [(1,0)] * tup[0]
        elif tup[0] < 0 and tup[1] < 0 and danger:
            # go up first
            part1 = [(-1,0)] * abs(tup[0])
            part2 = [(0,-1)] * abs(tup[1])
    elif pad == 'dpad':
        if tup[0] == 1 and tup[1] == -2:
            # go down first
            part1 = [(1,0)] * tup[0]
            part2 = [(0,-1)] * abs(tup[1])
        elif tup[0] == -1 and tup[1] == 2:
            # go right first
            part1 = [(0,1)] * tup[1]
            part2 = [(-1,0)] * abs(tup[0])

    # sequences always end with pushing 'A'
    memo_table[tup] = part1 + part2 + ['A']
    return part1 + part2 + ['A']

def get_instructions(nums, pad):
    """This takes the numbers from the numpad and turns them into instructions"""
    nums = ('A',) + nums
    numbers = []
    if pad == 'numpad':
        numbers = [numpad[num] for num in nums] # we turn them into coords here
    else:
        numbers = [dpad[num] for num in nums] # we turn them into coords here

    # then we find the difference between all the coordinates
    diffs = []
    for i in range(1, len(numbers)):
        diff = (numbers[i][0] - numbers[i-1][0], numbers[i][1] - numbers[i-1][1])
        diffs.append(diff)

    # now we turn these differences into instructions
    instructions = []
    if pad == 'numpad':
        for i in range(len(diffs)):
            # this is an ugly if statement, but we need to know if it's possible
            # to accidentally hit the no-go space
            if ((numbers[i][1] == 0 and numbers[i+1][0] == 3)
                or (numbers[i+1][1] == 0 and numbers[i][0] == 3)):
                instructions += expand_tuple(diffs[i], pad, True)
            else:
                instructions += expand_tuple(diffs[i], pad, False)
    else:
        instructions = list(chain.from_iterable(expand_tuple(diff, pad, False) for diff in diffs))

    # insts = [printpad[dir] for dir in instructions]
    # print(''.join(insts))
    return tuple(instructions)

# main entry point --------------------------------------------------------------------

# now we loop through our codes, and generate the result
complexities = []
for code in codes:
    depressurized_robot = get_instructions(code, 'numpad')
    radiation_robot = get_instructions(depressurized_robot, 'dpad')
    cold_robot = get_instructions(radiation_robot, 'dpad')
    sequence = len(cold_robot)
    numeric = int(''.join([num for num in code if num.isdigit()]))
    complexities.append(numeric * sequence)

print('The sum of the complexities is',sum(complexities))

# part two ----------------------------------------------------------------------------

# let's see if brute force will work with caching!

complexities = []
robot_count = 25
for code in codes:
    print('code:',code)
    robots = [None] * robot_count
    for i in range(len(robots)):
        print('robot:',i)
        if i == 0:
            robots[i] = get_instructions(code, 'numpad')
        else:
            robots[i] = get_instructions(robots[i-1], 'dpad')

    sequence = len(robots[-1])
    numeric = int(''.join([num for num in code if num.isdigit()]))
    complexities.append(numeric * sequence)

print('The sum of the complexities is',sum(complexities))