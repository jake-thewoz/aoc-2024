import data_getter
from functools import reduce

data = data_getter.get_data('22').splitlines()

# print(data)

# Hmm... so we need to make an efficient number machine.
# Maybe it's best to put these operations into functions so we can
# apply them vectorized

# data wrangling
initial_numbers = [int(line) for line in data]

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def first_step(a):
    b = a * 64
    c = mix(a, b)
    return prune(c)

def second_step(a):
    b = a // 32
    c = mix(a, b)
    return prune(c)

def third_step(a):
    b = a * 2048
    c = mix(a, b)
    return prune(c)

end_numbers = [
    reduce(lambda x, _: third_step(second_step(first_step(x))), range(2000), num)
    for num in initial_numbers
]

print('After 2000 generations, the sum of the secret numbers is', sum(end_numbers))