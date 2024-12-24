import data_getter
from collections import deque
import multiprocessing

data = data_getter.get_data('24').splitlines()

# print(data)

# Okay, so we just need to wrangle the data,
# run the operations, and calculate the result.

# data wrangling
blank_line = data.index('')
vars = {line.split(': ')[0]: int(line.split(': ')[1]) for line in data[:blank_line]}
ops = [
    {'var1': line.split(' ')[0],
     'op':line.split(' ')[1],
     'var2':line.split(' ')[2],
     'result':line.split(' ')[4]} 
     for line in data[blank_line+1:]]

# helper functions
def do_and(var1, var2):
    return var1 and var2

def do_or(var1, var2):
    return var1 or var2

def do_xor(var1, var2):
    return var1 ^ var2

# setting up our main
up_next = deque()
# this comprehension doesn't work
# [up_next.append(op) for op in ops[:] if op['var1'] in vars and op['var2'] in vars and ops.remove(op)]

for op in ops[:]:
    if op['var1'] in vars and op['var2'] in vars:
        up_next.append(op)
        ops.remove(op)

# now our main
while up_next:
    current_op = up_next.popleft()
    result = 0

    if current_op['op'] == 'AND':
        result = do_and(vars[current_op['var1']], vars[current_op['var2']])
    elif current_op['op'] == 'OR':
        result = do_or(vars[current_op['var1']], vars[current_op['var2']])
    elif current_op['op'] == 'XOR':
        result = do_xor(vars[current_op['var1']], vars[current_op['var2']])
    else:
        print('no operation found')
        quit()

    vars[current_op['result']] = result

    for op in ops[:]:
        if op['var1'] in vars and op['var2'] in vars:
            up_next.append(op)
            ops.remove(op)

z_vars = sorted({name: value for name, value in vars.items() if name[0] == 'z'}.keys(), reverse=True)
bit_string = ''
for z in z_vars:
    bit_string += str(vars[z])

output = int(bit_string, 2)
print('The output of the program is',output)

# part two --------------------------------------------------------------------------------

# hmm, I bet we could figure this out by just trying some basic values, like 0 and 0

# let's put the main part into a function
def calculate_output(initials, operations):
    up_next = deque()
    for op in operations[:]:
        if op['var1'] in initials and op['var2'] in initials:
            up_next.append(op)
            operations.remove(op)
    while up_next:
        current_op = up_next.popleft()
        result = 0
        if current_op['op'] == 'AND':
            result = do_and(initials[current_op['var1']], initials[current_op['var2']])
        elif current_op['op'] == 'OR':
            result = do_or(initials[current_op['var1']], initials[current_op['var2']])
        elif current_op['op'] == 'XOR':
            result = do_xor(initials[current_op['var1']], initials[current_op['var2']])
        else:
            print('no operation found')
            quit()
        initials[current_op['result']] = result
        for op in operations[:]:
            if op['var1'] in initials and op['var2'] in initials:
                up_next.append(op)
                operations.remove(op)
    z_vars = sorted({name: value for name, value in initials.items() if name[0] == 'z'}.keys(), reverse=True)
    bit_string = ''
    for z in z_vars:
        bit_string += str(initials[z])
    output = int(bit_string, 2)
    return output

# let's just try brute forcing this thing

inits = {line.split(': ')[0]: int(line.split(': ')[1]) for line in data[:blank_line]}
def check_if_fixed(operations):
    bad_starting_values = []
    for var in inits:
        inits.update((key, 0) for key in inits)
        inits[var] = 1
        result = calculate_output(inits.copy(), operations[:])
        if result != 2 ** int(var[1:]):
            bad_starting_values.append(var)
    return len(bad_starting_values)

def try_swap(args):
    index1, index2, ops, check_function = args
    op1, op2 = ops[index1], ops[index2]

    # do the swap
    op1['result'], op2['result'] = op2['result'], op1['result']

    # run the check
    is_successful = check_function(ops[:])

    # undo swap
    op1['result'], op2['result'] = op2['result'], op1['result']

    return (op1['result'], op2['result']) if is_successful else None

if __name__ == "__main__":
    # data wrangling
    blank_line = data.index('')
    inits = {line.split(': ')[0]: int(line.split(': ')[1]) for line in data[:blank_line]}
    cops = [
        {'var1': line.split(' ')[0],
        'op':line.split(' ')[1],
        'var2':line.split(' ')[2],
        'result':line.split(' ')[4]} 
        for line in data[blank_line+1:]]
    # generating all possible pairs of indices
    all_swaps = [
        (i, j, cops, check_if_fixed)
        for i in range(len(cops))
        for j in range(i + 1, len(cops))
    ]

    with multiprocessing.Pool() as pool:
        results = pool.map(try_swap, all_swaps)

    swaps = list(filter(None, results))

    print('The swappable results are',swaps)
    print('Length of swaps is',len(swaps))