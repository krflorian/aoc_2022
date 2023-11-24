#%%
from pathlib import Path
import re
from tqdm import tqdm

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
    data = [list(map(int, re.split(",| -> ", row))) for row in data]

# %%

cave = set()
for row in data:
    last_x = None
    last_y = None
    for i in range(0, len(row), 2):
        x = row[i]
        y = row[i + 1]
        if last_x and (x != last_x):
            for X in range(min(last_x, x), max(last_x, x) + 1):
                cave.add((X, y))
        if last_y and (y != last_y):
            for Y in range(min(last_y, y), max(last_y, y) + 1):
                cave.add((x, Y))

        last_x = x
        last_y = y

print(f"{len(cave)} rocks in the cave")

# %%


def move(x, y):
    new_position = (x, y + 1)
    # down
    if new_position not in cave:
        return new_position, False
    # left
    if (x - 1, y + 1) not in cave:
        return (x - 1, y + 1), False
    # right
    if (x + 1, y + 1) not in cave:
        return (x + 1, y + 1), False
    return (x, y), True


#%%
max_x = max([pos[0] for pos in list(cave)])
min_x = min([pos[0] for pos in list(cave)])
max_y = max([pos[1] for pos in list(cave)])

for X in range(min_x - 1500, max_x + 1500):
    cave.add((X, max_y + 2))

#%%
pos = (500, 0)
came_to_rest = False
stopped_sand = 0
last_two_positions = []

for _ in tqdm(range(100000000)):
    # last_two_positions.append(pos)
    # last_two_positions = last_two_positions[-2:]
    pos, came_to_rest = move(pos[0], pos[1])

    if pos[0] < max_y + 2:
        print("something is wrong - falling endlessly")
        break
    # end condition
    if pos == (500, 0):
        stopped_sand += 1

        print(f"falling endlessly down at {pos}")
        break

    # sand stopped
    if came_to_rest:
        # print(f"sand stopped at {pos}")
        cave.add(pos)
        stopped_sand += 1
        pos = (500, 0)

print(f"solution: {stopped_sand}")

# %%

len(list(cave))

import matplotlib.pyplot as plt

plt.plot([pos[0] for pos in cave], [pos[1] for pos in cave], "o")


# %%
