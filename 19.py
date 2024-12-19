import data_getter

data = data_getter.get_data('19_s').splitlines()

# print(data)

# data wrangling -------------

# we'll make our towels into a set of tuples for speed
towels = {towel.strip() for towel in data[0].split(',')}
patterns = data[2:]

# helper function -----------------
def is_possible(pattern):
    """Takes a pattern and returns True or False if it can be made using the towels"""
    n = len(pattern)
    dp = [False] * (n+1)
    dp[0] = True # this is the base case, where an empty pattern is matchable

    for i in range(1, n+1):
        for towel in towels:
            if i >= len(towel) and pattern[i - len(towel):i] == towel:
                dp[i] = dp[i] or dp[i - len(towel)]
    
    return dp[n]

# main --------------

possible_count = sum(is_possible(pattern) for pattern in patterns)
print('The number of possible designs is', possible_count)

# part two ----------------------------------------------------------

# This isn't much more dfficult, since we're already using a dynamic programming solution.
# Instead of storing booleans in our dp list, we can store the count of combinations as ints
def count_combinations(pattern):
    """Takes a pattern and returns the number of ways it can be made using the towels"""
    n = len(pattern)
    dp = [0] * (n+1)
    dp[0] = 1 # this is the base case, where an empty pattern is matchable one way

    for i in range(1, n+1):
        for towel in towels:
            if i >= len(towel) and pattern[i - len(towel):i] == towel:
                dp[i] += dp[i - len(towel)] # here we add combinations of the previous valid states
    
    return dp[n]

# Now we run this again
all_combos = sum(count_combinations(pattern) for pattern in patterns)
print('The sum of all possible combos is', all_combos)

# Lessons Learned:
#   - this feels like my first real intro to dynamic programming
#   - my first attempt to solve was a greedy, largest-towel-first approach
#       - this worked on the sample input, and it took a lot of thinking to figure out why it failed on larger input
#       - the problem is that some patterns can only be made with a combo of small-first and large-first pattern matching
#   - gpt led me to think that DP would create an ideal solution
#       - because we need to recursively check if a pattern can be made with different towels,
#           and because DP is basically recursion but better,
#           then we know there's a good DP solution.
#   - this solution is an example of bottom-up DP
#       - what is bottom-up?
#           - we start with the smallest subproblem, and build from there
#           - we build a table as we go, using it when we solve larger subproblems
#           - uses loops isntead of recursion