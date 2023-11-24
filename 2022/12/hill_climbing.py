#%%

from pathlib import Path
import networkx as nx
import string

DATA_PATH = Path("12/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data = [[v for v in row] for row in data]
data

#%%

height_dict = {letter: idx for idx, letter in enumerate(string.ascii_lowercase)}
height_dict["S"] = 0
height_dict["E"] = 25

#%%
graph = nx.DiGraph()

for row_id, row in enumerate(data):
    for col_id, node in enumerate(row):
        graph.add_node((row_id, col_id), height=height_dict[node])

#%%

lowest_points = []
for row_id, row in enumerate(data):
    for col_id, node in enumerate(row):
        if node == "S":
            start = (row_id, col_id)
            lowest_points.append((row_id, col_id))
        if node == "E":
            end = (row_id, col_id)
        if node == "a":
            lowest_points.append((row_id, col_id))

        # above
        if row_id > 0:
            if graph.nodes[(row_id - 1, col_id)]["height"] <= (
                graph.nodes[(row_id, col_id)]["height"] + 1
            ):
                graph.add_edge((row_id, col_id), (row_id - 1, col_id))
        # under
        if row_id < len(data) - 1:
            if graph.nodes[(row_id + 1, col_id)]["height"] <= (
                graph.nodes[(row_id, col_id)]["height"] + 1
            ):
                graph.add_edge((row_id, col_id), (row_id + 1, col_id))
        # left
        if col_id > 0:
            if graph.nodes[(row_id, col_id - 1)]["height"] <= (
                graph.nodes[(row_id, col_id)]["height"] + 1
            ):
                graph.add_edge((row_id, col_id), (row_id, col_id - 1))

        # right
        if col_id < len(data[0]) - 1:
            if graph.nodes[(row_id, col_id + 1)]["height"] <= (
                graph.nodes[(row_id, col_id)]["height"] + 1
            ):
                graph.add_edge((row_id, col_id), (row_id, col_id + 1))
# graph.edges

#%%

# nx.draw(graph, with_labels=True)

#%%

data = {}
for node in graph.nodes:
    data[node] = {}



# %%
# TODO from end to start
all_paths = []

path_from_start = nx.shortest_path(graph, start, end)

print("pathlenght from start: ", len(path_from_start) - 1)

for start_node in lowest_points:
    try:
        path = nx.shortest_path(graph, start_node, end)
    except:
        # print("no path between ", start_node, end)
        pass
    all_paths.append(path)

all_path_lenghts = sorted([len(path) for path in all_paths])

# print(f"shortest path steps: {len(path)-1}")
print(f"the shortest path is: {all_path_lenghts[0]-1} long")

#%%
