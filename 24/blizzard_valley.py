#%%
from pathlib import Path
from dataclasses import dataclass, field
import networkx as nx
from tqdm import tqdm

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")


#%%
# setup

max_x = len(data[0]) - 1
max_y = len(data) - 1


def up(x, y):
    return x, y - 1


def down(x, y):
    return x, y + 1


def right(x, y):
    return x + 1, y


def left(x, y):
    return x - 1, y


DIRECTION_DICT = {">": right, "<": left, "^": up, "v": down}


@dataclass
class Blizzard:
    x: int
    y: int
    direction: str
    end: tuple[int, int] = field(repr=False)
    start: tuple[int, int] = field(repr=False)

    def move(self):
        x, y = DIRECTION_DICT[self.direction](self.x, self.y)

        if (x, y) == self.end:
            x, y = self.start
        self.x = x
        self.y = y


#%%
# create blizzards

blizzards = []
for y, row in enumerate(data):
    for x, val in enumerate(row):

        if val == "#":
            pass
        elif val == ".":
            pass

        else:
            if val == ">":
                end = (max_x, y)
                start = (1, y)
            elif val == "<":
                end = (0, y)
                start = (max_x - 1, y)
            elif val == "^":
                end = (x, 0)
                start = (x, max_y - 1)
            elif val == "v":
                end = (x, max_y)
                start = (x, 1)

            blizzard = Blizzard(x=x, y=y, direction=val, end=end, start=start)
            blizzards.append(blizzard)


#%%
# create state


def create_new_state(blizzards):

    state = [["#" for _ in range(len(data[0]))] for _ in range(len(data))]
    # start and end position
    state[0][1] = "."
    state[max_y][max_x - 1] = "."

    for blizzard in blizzards:
        state[blizzard.y][blizzard.x] = blizzard.direction

    for y, row in enumerate(state):
        for x, val in enumerate(row):

            if val == "#":
                if (y not in [0, max_y]) and (x not in [0, max_x]):
                    state[y][x] = "."

    return state


#%%
# create graph

graph = nx.DiGraph()
timesteps = 1000

state = create_new_state(blizzards)
last_state = [["#" for _ in range(len(data[0]))] for _ in range(len(data))]

for t in tqdm(range(timesteps)):
    start_position = (1, 0, t)
    end_position = (max_x - 1, max_y, t)

    graph.add_node(start_position)  # start t
    graph.add_node(end_position)  # end t

    """
    print("__________")
    print("T: ", t)
    for row in state:
        print("".join(row))
    """
    for y, row in enumerate(state):
        for x, val in enumerate(row):
            if (y > 0) and (x > 0) and (y < max_y) and (x < max_x):
                if val == ".":
                    # make past connected to present
                    if last_state[y - 1][x] == ".":
                        graph.add_edge((x, y - 1, t - 1), (x, y, t))
                    if last_state[y + 1][x] == ".":
                        graph.add_edge((x, y + 1, t - 1), (x, y, t))
                    if last_state[y][x + 1] == ".":
                        graph.add_edge((x + 1, y, t - 1), (x, y, t))
                    if last_state[y][x - 1] == ".":
                        graph.add_edge((x - 1, y, t - 1), (x, y, t))
                    if last_state[y][x] == ".":
                        graph.add_edge((x, y, t - 1), (x, y, t))

            if t > 0:
                if (x, y, t) == start_position:
                    graph.add_edge((x, y, t - 1), (x, y, t))
                    if last_state[y + 1][x] == ".":
                        graph.add_edge((x, y + 1, t - 1), (x, y, t))

                if (x, y, t) == end_position:
                    graph.add_edge((x, y, t - 1), (x, y, t))
                    if last_state[y - 1][x] == ".":
                        graph.add_edge((x, y - 1, t - 1), (x, y, t))

    last_state = state
    for blizzard in blizzards:
        blizzard.move()
    state = create_new_state(blizzards)


#%%
# search algo


def search_goal_node(source, target_x, target_y):
    paths = nx.single_source_shortest_path(graph, source=source)

    paths = {
        node: path
        for node, path in paths.items()
        if (node[0] == target_x) and (node[1] == target_y)
    }

    node = sorted(paths.keys(), key=lambda x: x[2])[0]
    return node


#%%
# solution

node = search_goal_node(source=(1, 0, 0), target_x=max_x - 1, target_y=max_y)
time_first_arrival = node[2]
print("shortest path to: ", node)

node = search_goal_node(
    source=node,
    target_x=1,
    target_y=0,
)

print("shortest path reverse: ", node)

node = search_goal_node(
    source=node,
    target_x=max_x - 1,
    target_y=max_y,
)

total_time = node[2]

print(f"solution 1 minutes: {time_first_arrival}")
print(f"solution 2 minutes: {total_time}")

#%%
