import data_getter

data = data_getter.get_data('17').splitlines()

# print(data)

# Okay, so it seems we're kind of building a computer
# This time, I'll try to build it from the main loop first, then
# build out the functions.

# wrangle the data
reg_A = int(data[0].split(':')[1].strip())
reg_B = int(data[1].split(':')[1].strip())
reg_C = int(data[2].split(':')[1].strip())
all_ops = data[4].split(':')[1].strip().split(',')
instructions = [int(num) for num in all_ops]
ops = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: reg_A,
    5: reg_B,
    6: reg_C
}

inst_ptr = 0
output = ''
while inst_ptr < len(instructions):
    operand = instructions[inst_ptr+1]
    if instructions[inst_ptr] == 0:
        print('adv')
        numerator = ops[4]
        denom = 2 ** ops[operand]
        ops[4] = numerator // denom
    elif instructions[inst_ptr] == 1:
        print('bxl')
        ops[5] = ops[5] ^ operand
    elif instructions[inst_ptr] == 2:
        print('bst')
        ops[5] = ops[operand] % 8
    elif instructions[inst_ptr] == 3:
        print('jnz')
        if ops[4] != 0:
            inst_ptr = operand
            continue
    elif instructions[inst_ptr] == 4:
        print('bxc')
        ops[5] = ops[5] ^ ops[6]
    elif instructions[inst_ptr] == 5:
        print('out')
        output += str(ops[operand] % 8) + ','
    elif instructions[inst_ptr] == 6:
        print('bdv')
        numerator = ops[4]
        denom = 2 ** ops[operand]
        ops[5] = numerator // denom
    elif instructions[inst_ptr] == 7:
        print('cdv')
        numerator = ops[4]
        denom = 2 ** ops[operand]
        ops[6] = numerator // denom
    print('reg_a',ops[4])
    print('reg_b',ops[5])
    print('reg_c',ops[6])
    inst_ptr += 2
print(output)

# part two ---------------------------------------------

# Oh jeez...