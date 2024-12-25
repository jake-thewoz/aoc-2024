import data_getter

data = data_getter.get_data('25').splitlines()

# print(data)

# Merry Christmas!
# Okay, this one isn't too bad. Let's convert all our
# keys and locks into little lists

keys = []
locks = []
# first, we loop over every key/lock
for i in range(0, len(data), 8):
    new_one = [None] * 5
    # then we loop over every column
    for j in range(5):
        count = 0
        # in each column, we loop down the rows to get the count
        for c in range(7):
            if data[i+c][j] == '#':
                count += 1
        # and we subtract one for either the top or bottom row
        new_one[j] = count-1
    if data[i][0] == '#':
        # lock
        locks.append(new_one)
    else: # key
        keys.append(new_one)

# now, let's just brute force this and check every lock against every key
count = 0
for lock in locks:
    for key in keys:
        fits = all(a + b <= 5 for a, b in zip(lock, key))
        count += 1 if fits else 0 

print('The count of combos that work is', count)