import data_getter

data = data_getter.get_data(1).splitlines()

# print(data)

left_list = []
right_list = []

for pair in data:
    left_list.append(int(pair.split("   ")[0]))
    right_list.append(int(pair.split("   ")[1]))

left_list.sort()
right_list.sort()

difference = 0

for l_val, r_val in zip(left_list, right_list):
    difference += abs(l_val - r_val)

print(difference)

# part two ---------------------

# this part is totally different!

similarity = 0

for value in left_list:
    similarity += value * right_list.count(value)

print(similarity)