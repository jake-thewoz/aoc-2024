import data_getter
from collections import Counter

data = data_getter.get_data(5).splitlines()

# print(data)

# So we need to get our rules into some kind of variable
# Then we'll go through each update and
#   - get only the relevant rules by filtering
#   - check if any of the rules is broken
#   - if not, grab the middle page and add it to the sum

# Splitting up the data into the two sections is harder than I thought.
# Maybe there's a better way to do this, but whatever.
two_chunks = []
current_chunk = []
for line in data:
    if line.strip() == "":
        two_chunks.append(current_chunk)
        current_chunk = []
    else:
        current_chunk.append(line)
two_chunks.append(current_chunk)

raw_rules = two_chunks[0]
raw_updates = two_chunks[1]

# I'll go ahead and map these both into lists of tuples
# since I don't need to modify anything, this should give slight performance gains
rules = [tuple(map(int, rule.split('|'))) for rule in raw_rules]
updates = [tuple(map(int, update.split(','))) for update in raw_updates]

# Now I'll loop through the updates, adding the middle number to the sum if it's good
sum = 0
for update in updates:
    # Fun note- while trying to decide how to filter the rules, I came across a blog post:
    # https://www.artima.com/weblogs/viewpost.jsp?thread=98196
    # It seems Guido himself wanted to remove lambda, map, filter, and reduce from Python
    # in favor of list comprehensions.
    relevant_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    # valid = True
    # for rule in relevant_rules:
    #     if update.index(rule[0]) > update.index(rule[1]):
    #         valid = False
    #         break
    # Trying to teach myself to use list comprehensions when possible...
    valid = all(update.index(rule[0]) < update.index(rule[1]) for rule in relevant_rules)
    sum += update[len(update) // 2] if valid else 0

print("The sum of middle digits is", sum)

# part two --------------------------------------------------------------------------------

# Dang. Well lets start by getting all the bad updates
incorrect_updates = []
for update in updates:
    relevant_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    incorrect = any(update.index(rule[0]) > update.index(rule[1]) for rule in relevant_rules)
    if incorrect:
        incorrect_updates.append(update)
    
# I need to think through how to correctly order a list.
# Something about this reminds me of sorting functions
# Question- do these updates contain numbers ONLY found in the rules? Are there any extras?
# let's find out, because if not, I can create them from the rules alone
for update in incorrect_updates:
    relevant_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    flat_rules = {digit for rule in relevant_rules for digit in rule}
    flat_update = set(update)
    if flat_rules != flat_update:
        print('damn')

# Okay! Now we know there are no digits in the updates that aren't in the rules.
# So we can just send the relevant rules to a function to create the correctly ordered update
def create_update(rules):
    fixed_update = []
    # Discovery! This can work if we sort by the count of the first element.
    first_counts = Counter(rule[0] for rule in rules)
    sorted_rules = sorted(rules, key=lambda rule: first_counts[rule[0]], reverse=True)
    rules = sorted_rules
    # We'll try looping through the rules just once
    for rule in rules:
        # There are three possibilities:
        # 1. Niether page is in the update
        if rule[0] not in fixed_update and rule[1] not in fixed_update:
            fixed_update.insert(0, rule[1])
            fixed_update.insert(0, rule[0])
        # 2. One page is in the update
        elif rule[0] not in fixed_update:
            fixed_update.insert(fixed_update.index(rule[1]), rule[0])
        elif rule[1] not in fixed_update:
            fixed_update.insert(fixed_update.index(rule[0])+1, rule[1])
        # 3. Both pages are in the update
        else:
            # Either it's already fine, or it needs to move
            if fixed_update.index(rule[0]) > fixed_update.index(rule[1]):
                fixed_update.pop(fixed_update.index(rule[0]))
                fixed_update.insert(fixed_update.index(rule[1]), rule[0])

    return fixed_update

sum = 0
for update in incorrect_updates:
    relevant_rules = [rule for rule in rules if rule[0] in update and rule[1] in update]
    fixed_update = create_update(relevant_rules)
    sum += fixed_update[len(fixed_update) // 2]

print('The fixed updates have a sum of', sum)