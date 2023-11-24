from pathlib import Path
import networkx as nx
import string
import random
import json

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


def make_idx():
    idx = ""
    for _ in range(5):
        idx += random.choice(string.ascii_lowercase)
    return idx


make_idx()

#%%


for row_id, row in enumerate(data):
    for col_id, node in enumerate(row):
        if node == "S":
            start = (row_id, col_id)
        if node == "E":
            end = (row_id, col_id)

        # above
        if row_id > 0:
            if graph.nodes[(row_id - 1, col_id)]["height"] <= (
                graph.nodes[(row_id, col_id)]["height"] + 1
            ):
                out_graph.add_edge((row_id, col_id), (row_id - 1, col_id))
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

out_graph = nx.Graph()

node_mapper = {}
for node in graph.nodes():
    if node == start:
        idx = "start"
    elif node == end:
        idx = "end"
    else:
        idx = make_idx()

    node_mapper[node] = idx


for edge in graph.edges:
    from_node = node_mapper[edge[0]]
    to_node = node_mapper[edge[1]]

    out_graph.add_edge(from_node, to_node, distance=round(random.uniform(10, 500), 2))


#%%


data = {}
for node in out_graph.nodes:
    data[node] = {}

for from_node, to_node in out_graph.edges:
    data[from_node][to_node] = out_graph[from_node][to_node]


data

#%%

with open(DATA_PATH / "graph.json", "w") as outfile: 
    json.dump(data, outfile)
