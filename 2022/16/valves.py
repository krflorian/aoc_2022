#%%
from pathlib import Path
import re
import networkx as nx
from dataclasses import dataclass, field

DATA_PATH = Path("16/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

#%%

all_valves = []
valves = nx.Graph()
for row in data:

    idx = row[6:8]

    valve, connection = row.split(";")
    flow_rate = int(valve.split("=")[1])

    if flow_rate > 0:
        all_valves.append(idx)
    valves.add_node(idx, flow_rate=flow_rate)

    connection = [c for c in re.split(" |,", connection) if c != ""][4:]
    for node in connection:
        valves.add_edge(idx, node)


#%%
# pt 2
duration = {}

for node in valves.nodes:
    paths = nx.single_target_shortest_path_length(valves, node)
    if node not in duration:
        duration[node] = {}
    for p in paths:
        duration[node][p[0]] = p[1]

#%%
# pt2


@dataclass
class Path:
    current_valve: str
    current_time: int
    unopened_valves: list[str]
    opened_valves: list[str] = field(default_factory=list)
    flow_rate: int = 0


paths: list[Path] = []
visited_paths = []
max_time = 26

start = Path(
    current_valve="AA",
    current_time=0,
    unopened_valves=[v for v in all_valves if v != "AA"],
)
paths.append(start)
i = 0

while paths:
    path = paths.pop()
    i += 1
    if i % 1000 == 0:
        print(f"looking at path n {i}")

    for valve in path.unopened_valves:

        arrival_time = duration[path.current_valve][valve]
        arrival_time += path.current_time + 1

        if arrival_time <= max_time:

            remaining_time = max_time - arrival_time
            flow_rate = path.flow_rate + (
                remaining_time * valves.nodes[valve]["flow_rate"]
            )
            unopened_valves = [v for v in path.unopened_valves if v != valve]

            new_path = Path(
                current_valve=valve,
                current_time=arrival_time,
                unopened_valves=unopened_valves,
                opened_valves=path.opened_valves + [valve],
                flow_rate=flow_rate,
            )
            paths.append(new_path)
            visited_paths.append(new_path)

len(visited_paths)

#%%

from itertools import combinations
from IPython.display import clear_output

best_flow = 0
i = 0


for human_path, elephant_path in combinations(visited_paths, 2):
    i += 1
    if i % 1000000 == 0:
        clear_output()
        print(f"looking at combination number {i}")
    if all([p not in human_path.opened_valves for p in elephant_path.opened_valves]):
        total_flow = human_path.flow_rate + elephant_path.flow_rate
        if total_flow > best_flow:
            best_flow = total_flow

print("solution: ", best_flow)

#%%
# pt1
from dataclasses import dataclass, field


@dataclass
class Path:
    current_valve: str
    current_time: int
    unopened_valves: list[str]
    opened_valves: list[str] = field(default_factory=list)
    flow_rate: int = 0


paths: list[Path] = []
max_time = 26

start = Path(
    current_valve="AA",
    current_time=0,
    unopened_valves=[v for v in all_valves if v != "AA"],
)
paths.append(start)
best_path = start
i = 0

while paths:
    path = paths.pop()
    i += 1
    if i % 1000 == 0:
        print(f"looking at path n {i}")

    for valve in path.unopened_valves:

        arrival_time = len(nx.shortest_path(valves, path.current_valve, valve)) - 1
        arrival_time += path.current_time + 1

        if arrival_time <= max_time:

            remaining_time = max_time - arrival_time
            flow_rate = path.flow_rate + (
                remaining_time * valves.nodes[valve]["flow_rate"]
            )

            unopened_valves = [v for v in path.unopened_valves if v != valve]
            unopened_flow_rates = sorted(
                [valves.nodes[v]["flow_rate"] for v in unopened_valves]
            )

            time_per_unopened_valve = [
                remaining_time - i for i in range(2, len(unopened_valves) * 2 + 2, 2)
            ]

            upper_bound = flow_rate + sum(
                [
                    flow * t
                    for flow, t in zip(
                        reversed(unopened_flow_rates), time_per_unopened_valve
                    )
                    if t > 0
                ]
            )

            if best_path.flow_rate <= upper_bound:

                new_path = Path(
                    current_valve=valve,
                    current_time=arrival_time,
                    unopened_valves=unopened_valves,
                    opened_valves=path.opened_valves + [valve],
                    flow_rate=flow_rate,
                )
                paths.append(new_path)

    if path.flow_rate > best_path.flow_rate:
        best_path = path


print(f"total searched paths: {i}")
print(f"max flow rate: {best_path.flow_rate}")


#%%
