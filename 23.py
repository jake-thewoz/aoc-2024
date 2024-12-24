import data_getter
import networkx as nx

data = data_getter.get_data('23').splitlines()

# print(data)

# This seems pretty easy!
# I first tried a manual approach, but then I found out
# about the networkx library. So let's make a graph!

# data wrangling
pairs = [(line.split('-')[0],line.split('-')[1]) for line in data]

# create the graph data structure from the pairs
graph = nx.Graph()
graph.add_edges_from(pairs)

# find all the triangles
triangles = [set(triangle) for triangle in nx.enumerate_all_cliques(graph) if len(triangle) == 3]

# filter the triangles by 't'
t_triangles = [triangle for triangle in triangles if any(computer.startswith('t') for computer in triangle)]

print('The number of inter-connected computers with at least one t* is',len(t_triangles))

# part two -------------------------------------------------------------

# not so bad! I bet nx has a tool for this-
# It does! A set of interconnected nodes is called a clique

# here we're finding the largest clique
largest = max(nx.find_cliques(graph), key=len)

largest.sort()
print('The password to the party is', ','.join(largest))

# Lessons Learned:
#   - felt like I 'cheated' a little bit today
#   - but I learned about graphs and cliques