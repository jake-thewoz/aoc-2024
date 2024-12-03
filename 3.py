import data_getter
import re

data = data_getter.get_data(3).splitlines()

# print(data)

# sounds like this is a perfect excuse to use some regex

combined_data = ''.join(data)
muls = re.findall(r"mul\(\d{1,3},\d{1,3}\)", combined_data)

# now we have all our instructions, we just need to multiply and add them

sum = 0
for instruction in muls:
    string_versions = instruction.split(",")
    left = int(''.join(c for c in string_versions[0] if c.isdigit()))
    right = int(''.join(c for c in string_versions[1] if c.isdigit()))
    sum += (left * right)

print("sum = ", sum)
        
# part 2 --------------------------------------

# ah, a tricky variation on the previous problem
# should still be fairly simple, if we can get all the dos and don'ts
    # into one list

# I'm not sure if this is the best way to write this regex, but it works.
# the ?: makes the groups non-capturing, so I don't end up with empty results in tuples

instructions = re.findall(r"(?:mul\(\d{1,3},\d{1,3}\))|(?:do\(\))|(?:don't\(\))", combined_data)

# now we loop through again, this time with a flag for do or don't

sum = 0
do = True
for instruction in instructions:
    if instruction == 'do()':
        do = True
    elif instruction == "don't()":
        do = False
    elif do and 'mul' in instruction:
        string_versions = instruction.split(",")
        left = int(''.join(c for c in string_versions[0] if c.isdigit()))
        right = int(''.join(c for c in string_versions[1] if c.isdigit()))
        sum += (left * right)
        
print("new sum = ", sum)