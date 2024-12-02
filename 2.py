import data_getter

data = data_getter.get_data(2).splitlines()

# print(data)

# okay, we've got to find which reports are safe
# a report is safe only if
#   - all levels are increasing or decreasingg
#   - adjacent levels differ by at least 1 and at most 3

# I think we can do this in one loop

safe_count = 0
asc = 1  # we'll use this to determine if the list is going up or down

for raw_report in data:
    report = [int(level) for level in raw_report.split(" ")]
    # first we'll check for the asc/desc direction
    if report[0] - report[1] > 0:
        asc = 1
    elif report[0] - report[1] < 0:
        asc = -1
    else:
        continue # if two numbers are the same, the report isn't safe

    safe = True
    for i in range(1, len(report)):
        left_level = report[i-1]
        right_level = report[i]

        # now we go through the rules
        if (left_level - right_level)*asc < 1:
            safe = False
            break
        elif (left_level - right_level)*asc > 3:
            safe = False
            break
    
    safe_count += 1 if safe else 0

print(safe_count)

# part two -------------------------------------------------

# interesting... we'll have to figure out a way to remove a level and run again
# let's start with the same loop from part one

# okay, I'm going to brute force these erroneous reports

# this is the function that we send any reeports to that fail at least one time
def damper_check(report):
    for x in range(len(report)):
        new_report = report.copy()
        new_report.pop(x)

        asc = 1
        if new_report[0] - new_report[1] > 0:
            asc = 1
        elif new_report[0] - new_report[1] < 0:
            asc = -1

        safe = True
        for i in range(1, len(new_report)):
            left_level = new_report[i-1]
            right_level = new_report[i]

            # now we go through the rules
            if (left_level - right_level)*asc < 1:
                safe = False
                break
            elif (left_level - right_level)*asc > 3:
                safe = False
                break
        if safe:
            return safe
            
    return safe # this is if it fails

# now we're done with the helper function, here's our 'main' section

safe_count = 0
for raw_report in data:
    report = [int(level) for level in raw_report.split(" ")]

    asc = 1
    if report[0] - report[1] > 0:
        asc = 1
    elif report[0] - report[1] < 0:
        asc = -1

    safe = True
    for i in range(1, len(report)):
        left_level = report[i-1]
        right_level = report[i]

        # now we go through the rules
        # if there are any problems, we do the damper check
        if (left_level - right_level)*asc < 1:
            safe = damper_check(report)
            break
        elif (left_level - right_level)*asc > 3:
            safe = damper_check(report)
            break
    
    safe_count += 1 if safe else 0

print(safe_count)