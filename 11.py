import data_getter
from functools import cache

data = data_getter.get_data(11).splitlines()

# print(data)

# This seems simple enough. We just need a function to handle the blinking

def blink(stones):
    """Takes a list of stones and applies the blinking rules"""
    s = 0
    while s < len(stones):
        # rule 1
        if stones[s] == '0':
            stones[s] = '1'
        # rule 2
        elif len(stones[s]) % 2 == 0:
            midpoint = len(stones[s]) // 2
            left = str(int(stones[s][:midpoint]))
            right = str(int(stones[s][midpoint:]))
            stones[s] = left
            stones.insert(s + 1, right)
            s += 1
        # rule 3
        else:
            stones[s] = str(int(stones[s]) * 2024)

        s += 1

stones = data[0].split(' ')

for i in range(25):
    blink(stones)

print('length is', len(stones))

# part two ----------------------------------------------------------------------------

# this answer requires some regression math, which I'm unfamiliar with.
# I think I could use an online tool to solve it, but ...
# maybe I can use a cached function to return the values
# EDIT- this approach didn't work either. Final solution is below

@cache
def calculate_stone(stone: str) -> tuple:
    # rule 1
    if stone == '0':
        return ('1',)
    # rule 2
    elif len(stone) % 2 == 0:
        midpoint = len(stone) // 2
        left = str(int(stone[:midpoint]))
        right = str(int(stone[midpoint:]))
        return (left, right)
    # rule 3
    else:
        return (str(int(stone) * 2024),)

@cache
def calculate_sublist(sublist: tuple[str]) -> tuple[str]:
    new_stones = []
    for stone in sublist:
        new_stones.extend(calculate_stone(stone))
    return tuple(new_stones)

def split_into_chunks(stones: list[str], chunk_size: int) -> list[tuple[str]]:
    return [tuple(stones[i:i+chunk_size]) for i in range(0, len(stones), chunk_size)]

def cached_blink(stones: list[str]) -> list[str]:
    # return [new_stone for stone in stones for new_stone in calculate_stone(stone)]
    stones.sort()
    sublists = split_into_chunks(stones, 100)
    new_stones = []
    for sublist in sublists:
        new_stones.extend(calculate_sublist(sublist))
    return new_stones

# with this, I've learned that there are only 54 unique values by iteration i=22 when starting value was 0
stones = ['0']
sequence = []
for i in range(22):
    stones = cached_blink(stones)
print('uniques:', len(set(stones)))

# Okay, new approach! We're using lessons from Lanternfish!
# From previous work, I know there are only ever 54 unique values.
# we can make a dict where those values are the key, and the value is the number of them.

stones = data[0].split(' ')
dict_of_stones = {stone: stones.count(stone) for stone in stones}

def lantern_blink(dict_of_stones):
    dict_of_change = {stone: 0 for stone in dict_of_stones}
    for stone, count in dict_of_stones.items():
        new_stones = calculate_stone(stone)
        for new_stone in new_stones:
            if new_stone in dict_of_change:
                dict_of_change[new_stone] += count
            else:
                dict_of_change[new_stone] = count
        dict_of_change[stone] -= count
    result = {stone: dict_of_stones.get(stone, 0) + dict_of_change.get(stone, 0) for stone in set(dict_of_stones) | set(dict_of_change)}
    return result

for i in range(75):
    dict_of_stones = lantern_blink(dict_of_stones)

print('final dict of stones:',dict_of_stones)
print('count of all values:', sum(dict_of_stones.values()))

# Lessons learned:
#   - caching is really powerful, and should be used everywhere reasonable
#       - isn't a magic bullet, though
#   - exponential growth problems can sometimes be thought of in terms of the unique values
#       - this is the essence of the laternfish approach
#       - if you can turn a long list into a much shorter dict of possible values, it becomes trivial to count the length