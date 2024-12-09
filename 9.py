import data_getter

data = data_getter.get_data(9).splitlines()

# print(data)

# Brainstorming...
#   - file IDs can be more than one digit, so simple string manipulation probably isn't good
#   - the input is 20,000 numbers
# My first idea is to build the compacted filesystem by looping from both ends
# I think we can skip the 00...1111.. format
# Actually, I don't think we can. We'll need the left and right indexes below, and we won't have that until we build it
#   - start with the left building.
#   - when it's time for empty space, pass the left index, number of times, and right index to the right filler
#   - the right fills the number of times, then... passes the right index back?
#   - when the left index equals the right index, we stop
# Then we can calculate the checksum (index * id...)

disk_map = data[0]

expanded_disk = []

for i in range(len(disk_map)):
    # first we'll grab the value from the disk map, which is the number of times
    times = int(disk_map[i])
    # then we'll check if we're building a file or empty space
    if i % 2 == 0: # build a file
        id_number = i // 2
        # extend is a way to append a new list to a list        
        expanded_disk.extend([id_number for _ in range(times)])
    else: # build empty space
        expanded_disk.extend(['.' for _ in range(times)])

# print(expanded_disk)
compacted_disk = expanded_disk.copy()

for i in range(len(compacted_disk) - 1, -1, -1):
    # first we'll check if it's empty space:
    if compacted_disk[i] == '.':
        compacted_disk.pop(i)
    elif '.' in compacted_disk: # this location is an id, and we're not done
        dest = compacted_disk.index('.')
        compacted_disk[dest] = expanded_disk[i]
        compacted_disk.pop(i)
    elif '.' not in compacted_disk:
        break

# print(compacted_disk)

checksum = 0
for i in range(len(compacted_disk)):
    checksum += (i * compacted_disk[i])

print('The checksum is', checksum)

# part two --------------------------------------------------------------------------

# I had a feeling something like this would be asked of us!
# So files will stay the same length, but spaces will be mutilated
# Here's my plan:
#   - create a dict of file ids and their size
#   - go through the expanded_disk again, this time from the left
#       - if we come across a file id, it's removed from the dict
#   - when we find free space, we look for the largest id that will fit in the space
#       - then we swap. old spaces change to '.'
#       - moved files are removed from the dict

# Here I'll make the dict of ids and sizes
files = {}
for i in range(len(disk_map)):
    if i % 2 == 0:
        files[i // 2] = int(disk_map[i])

compacted_disk = expanded_disk.copy()

def find_best_file(files, free_space):
    """Given a dict of files, this returns the biggest file_id that will fit in a free_space"""
    best_file = None
    for file_id, file_size in files.items():
        if file_size <= free_space:
            if best_file is None or file_id > best_file:
                best_file = file_id
    return best_file

def move_file(file_id, dest, disk):
    """Given a file and dest, this function moves and replaces the old location with '.', also removing from the files dict"""
    # dest and src are indexes of the disk
    src = disk.index(file_id)
    file_size = files.pop(file_id)
    for i in range(dest, dest + file_size):
        disk[i] = file_id
    for i in range(src, src + file_size):
        disk[i] = '.'

# Now I'm gonna do a manual for loop :D
i = 0
while i < len(compacted_disk):
    if compacted_disk[i] != '.':
        file = compacted_disk[i]
        if file in files:
            files.pop(file)
    else: # empty space!
        # here we'll calculate how big the space is
        free_space = 0
        for j in range(i, len(compacted_disk)):
            if compacted_disk[j] == '.':
                free_space += 1
            else:
                break
        # then we'll find the best file to move in here
        file_to_move = find_best_file(files, free_space)
        if file_to_move is None:
            i += 1
            continue
        # Now we need to swap them
        move_file(file_to_move, i, compacted_disk)
    if files == {}:
        break
    i += 1

# print(compacted_disk)

checksum = 0
for i in range(len(compacted_disk)):
    if compacted_disk[i] != '.':
        checksum += (i * compacted_disk[i])

print('My method for disk compression has checksum of', checksum)

# Well I did this wrong, by not carefully reading the prompt.
# I need to start from the back, looking for space for the back numbers first.

# Let's try again
files = {}
for i in range(len(disk_map)):
    if i % 2 == 0:
        files[i // 2] = int(disk_map[i])

def find_space(file, file_size, disk):
    """Takes file_size and a disk, and returns the index of the first adequate space"""
    for i in range(len(disk)-file_size):
        if disk[i] == file:
            break
        if disk[i] == '.':
            for j in range(i, i+file_size):
                if disk[j] != '.':
                    break
                elif j == i+file_size-1:
                    return i
    return None           

compacted_disk = expanded_disk.copy()

for i in range(len(compacted_disk)-1, -1, -1):
    if compacted_disk[i] != '.':
        file = compacted_disk[i]
        if file in files:
            file_size = files[file]
            dest = find_space(file, file_size, compacted_disk)
            move_file(file, dest, compacted_disk) if dest else None

checksum = 0
for i in range(len(compacted_disk)):
    if compacted_disk[i] != '.':
        checksum += (i * compacted_disk[i])

print('The requested method produces', checksum)

# Lessons learned:
#   - range() is interesting:
#       - with one argument, the iterator stops just before it
#       - with two, the first arg is the start, second is end. range(1,5) = 1,2,3,4
#       - with three, it's two but the last one is step. range(1,5,2) = 1,3
#   - maybe follow along with the prompt as it solves the sample input.
#       - I used sample input, but could've saved a little time by carefully studying the methodology