import data_getter

data = data_getter.get_data(7).splitlines()

# print(data)

# Maybe I need more coffee, but I think there's only one way to do this:
#   - loop through the list of equations
#       - loop through the right side
#       - try every combo of operands
#       - quit if we find a correct answer

equations = data.copy()
total = 0

for equation in equations:
    # first we'll do some data wrangling
    answer = int(equation.split(':')[0])
    str_digits = equation.split(' ')[1:]
    digits = [int(digit) for digit in str_digits]

    # now we'll loop over the digits 2^(len(digits)-1) times for all the combos
    for i in range(2 ** (len(digits)-1)):
        guess = digits[0] # we start with the first digit
        # then loop over the operators
        for j in range(len(digits)-1):
            # now we'll do some binary work on i in the outside loop.
            # starting with the least significant digit (0), we'll
            # add or multiply if that digit is 0 or 1
            if i & (1 << j):
                guess += digits[j+1]
            else:
                guess *= digits[j+1]
        if guess == answer:
            total += answer
            break

print('The sum of all correct equations is', total)

# part two --------------------------------------------------------------------

# okay, not much harder. we just need to add the || to the combinations 

equations = data.copy()
total = 0

for equation in equations:
    # again, we'll do some data wrangling
    answer = int(equation.split(':')[0])
    str_digits = equation.split(' ')[1:]
    digits = [int(digit) for digit in str_digits]

    # now we'll loop over the digits 3^(len(digits)-1) times for all the combos
    for i in range(3 ** (len(digits)-1)):
        guess = digits[0]

        for j in range(len(digits)-1):
            # since there's no base 3 format (like how binary is base 2), we'll have to simulate it
            # we can do this with the % operator, but we just need to shift i to the correct digit
            shifted = i // (3 ** j)
            # now we can get 0,1,2 from i reliably
            flag = shifted % 3

            if flag == 0: # this is our * case
                guess *= digits[j+1]
            elif flag == 1: # this is +
                guess += digits[j+1]
            else: # and now ||
                guess = int(str(guess) + str(digits[j+1]))

        if guess == answer:
            total += answer
            break

print('The new sum of all correct equations is', total)

# Lesson for next time: I lost a lot of time because I misunderstood the prompt.
# Specifically, how || was supposed to work. Next time, I'll start with the 
# sample input, and make sure I understand what's asked.