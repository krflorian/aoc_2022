# %%

from pathlib import Path
from map_2d import Map2D

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
data


# %%

operations = []
for row in data:
    direction, length, color = row.split()
    operations.append((direction, int(length), color))
operations

# %%

map_data = []
for _ in range(10000):
    map_data.append("." * 10000)

lava_map = Map2D(map_data)

# %%


direction_mapper = {
    "R": lava_map.right,
    "L": lava_map.left,
    "U": lava_map.up,
    "D": lava_map.down,
}

# %%
# part 1

position = (lava_map.max_x // 2, lava_map.max_y // 2)
lava_map.set_value(position, "#")

for direction, length, color in operations:
    for _ in range(length):
        value, coordinate = direction_mapper[direction](position)
        if value is not None:
            position = coordinate
            lava_map.set_value(position, "#")
        else:
            print(position)
            print("error")

print(lava_map)

queue = [(lava_map.max_x // 2 + 1, lava_map.max_y // 2 - 1)]
visited = set()
while queue:
    position = queue.pop(0)
    for direction in direction_mapper.values():
        value, coordinate = direction(position)
        if value is None:
            continue
        elif value != "#":
            if coordinate not in visited:
                queue.append(coordinate)
                visited.add(coordinate)
                lava_map.set_value(coordinate, "o")
        else:
            visited.add(coordinate)

points = iter(lava_map)
solution = 0
for var, x, y in points:
    if var != ".":
        solution += 1
solution


# %%
# part 2
c_map = ["R", "D", "L", "U"]

operations = []
for row in data:
    direction, length, color = row.split()
    length = int(row[-7:-2], 16)
    direction = c_map[int(color[-2])]
    operations.append((direction, int(length), color))
operations

# %%


def left(position, length):
    return (position[0] - length, position[1])


def right(position, length):
    return (position[0] + length, position[1])


def up(position, length):
    return (position[0], position[1] + length)


def down(position, length):
    return (position[0], position[1] - length)


direction_mapper = {
    "R": right,
    "L": left,
    "U": up,
    "D": down,
}

position = (0, 0)
lava_map = []
total_length = 0
for direction, length, color in operations:
    new_position = direction_mapper[direction](position, length)
    lava_map.append(new_position)
    position = new_position
    total_length += length
assert len(lava_map) % 2 == 0
lava_map

# %%

import numpy as np


# https://en.wikipedia.org/wiki/Shoelace_formula
def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


area = PolyArea(
    np.array([float(pos[0]) for pos in lava_map]),
    np.array([float(pos[1]) for pos in lava_map]),
)

# https://en.wikipedia.org/wiki/Pick's_theorem
solution = area + 1 - total_length // 2 + total_length
solution

# %%
