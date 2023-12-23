# %%
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")


instructions = data[0]
instruction_2_index = {"L": 0, "R": 1}

# %%
import re

pattern = "[A-Z]{3}"


nodes = data[2:]
nodes = [node.split("=") for node in nodes]

graph = {}
for node in nodes:
    edges = re.findall(pattern, node[1])
    graph[node[0].strip()] = edges


# %%
# part 1
steps = 0
current_node = "AAA"
for instruction in instructions * 100:
    steps += 1
    current_node = graph[current_node][instruction_2_index[instruction]]
    if current_node == "ZZZ":
        break
print(steps)


# %%
# part 2


# %%
from tqdm import tqdm

"""
instructions = "LR"
graph = {
    "11A": ("11B", "XXX"),
    "11B": ("XXX", "11Z"),
    "11Z": ("11B", "XXX"),
    "22A": ("22B", "XXX"),
    "22B": ("22C", "22C"),
    "22C": ("22Z", "22Z"),
    "22Z": ("22B", "22B"),
    "XXX": ("XXX", "XXX"),
}
"""

start_nodes = [node for node in graph if node.endswith("A")]
node_path_lengths = []

for current_node in start_nodes:
    steps = 0
    for instruction in instructions * 100000:
        steps += 1
        current_node = graph[current_node][instruction_2_index[instruction]]
        if current_node.endswith("Z"):
            break
    node_path_lengths.append(steps)


# %%

import math

math.lcm(*node_path_lengths)
