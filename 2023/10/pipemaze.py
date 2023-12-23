# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")


# %%
import networkx as nx
from map_2d import Map2D


map2d = Map2D(data)
# print(map2d)
nodes = iter(map2d)
graph = nx.Graph()
start_coordinates = None

for node, x, y in nodes:
    if x == 1 and y == 4:
        print(node)
    if node == ".":
        continue
    if node == "|":
        val, coordinates = map2d.down((x, y))
        if coordinates:
            if val in ["L", "J", "|", "S"]:
                graph.add_edge((x, y), coordinates)
        val, coordinates = map2d.up((x, y))
        if coordinates:
            if val in ["7", "F", "|", "S"]:
                graph.add_edge((x, y), coordinates)
    elif node == "-":
        val, coordinates = map2d.left((x, y))
        if coordinates:
            if val in ["-", "L", "F", "S"]:
                graph.add_edge((x, y), coordinates)
        val, coordinates = map2d.right((x, y))
        if coordinates:
            if val in ["J", "-", "7", "S"]:
                graph.add_edge((x, y), coordinates)
    elif node == "L":
        val, coordinates = map2d.up((x, y))
        if coordinates:
            if val in ["7", "F", "|", "S"]:
                graph.add_edge((x, y), coordinates)
        val, coordinates = map2d.right((x, y))
        if coordinates:
            if val in ["J", "-", "7", "S"]:
                graph.add_edge((x, y), coordinates)
    elif node == "J":
        val, coordinates = map2d.up((x, y))
        if coordinates:
            if val in ["7", "F", "|", "S"]:
                graph.add_edge((x, y), coordinates)
        val, coordinates = map2d.left((x, y))
        if coordinates:
            if val in ["-", "L", "F", "S"]:
                graph.add_edge((x, y), coordinates)
    elif node == "7":
        val, coordinates = map2d.down((x, y))
        if coordinates:
            if val in ["L", "J", "|", "S"]:
                graph.add_edge((x, y), coordinates)
        val, coordinates = map2d.left((x, y))
        if coordinates:
            if val in ["-", "L", "F", "S"]:
                graph.add_edge((x, y), coordinates)
    elif node == "F":
        val, coordinates = map2d.down((x, y))
        if coordinates:
            if val in ["L", "J", "|", "S"]:
                graph.add_edge((x, y), coordinates)
        val, coordinates = map2d.right((x, y))
        if coordinates:
            if val in ["J", "-", "7", "S"]:
                graph.add_edge((x, y), coordinates)
    elif node == "S":
        start_coordinates = (x, y)
    else:
        print("error", node, x, y)

# %%
# part 1


shortest_paths = nx.single_source_shortest_path(graph, start_coordinates)
shortest_paths

# %%

longest_path = sorted([path for path in shortest_paths.values()], key=lambda x: len(x))[
    -1
]
print("solution ", len(longest_path) - 1)


# %%
# part 2


cycle = nx.find_cycle(graph, start_coordinates)
nodes = []
for edges in cycle:
    nodes.extend(edges)
cycle_nodes = list(set(nodes))

print(map2d)
cycle_nodes


# %%

nodes = iter(map2d)
for val, x, y in nodes:
    if (x, y) not in cycle_nodes:
        map2d.values[x][y] = "."

# %%

new_map = []
for y in range(map2d.max_y + 1):
    new_map.append(" ".join([map2d.values[x][y] for x in range(map2d.max_x + 1)]))

print("\n".join(reversed(new_map)))


# %%

enclosed_nodes = []
for y in range(map2d.max_y + 1):
    vertical_nodes = [
        node
        for node in cycle_nodes
        if (node[1] == y) and map2d(node)[0] in ["|", "L", "J"]
    ]

    for x in range(map2d.max_x):
        if (x, y) not in cycle_nodes:
            nodes_to_right = [node for node in vertical_nodes if node[0] > x]
            if len(nodes_to_right) % 2 == 1:
                enclosed_nodes.append((x, y))

print(len(enclosed_nodes))

# %%
