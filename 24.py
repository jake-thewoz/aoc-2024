import data_getter
from collections import deque

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
