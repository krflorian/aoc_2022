# %%

from pathlib import Path
from tqdm import tqdm

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

# %%


from map_2d import Map2D

"""
garden = Map2D(data)
print(garden)

tiles = iter(garden)
for value, x, y in tiles:
    if value == "S":
        starting_position = (x, y)
        break
starting_position
"""


# %%

_endless_data, endless_data = [], []
for row in data:
    _endless_data.append(row * 5)
endless_data

for _ in range(5):
    for row in _endless_data:
        endless_data.append(row)

len(endless_data)


# %%

garden = Map2D(endless_data)
print(garden)

starting_position = ((garden.max_x + 1) // 2, (garden.max_y + 1) // 2)
value = garden(starting_position)

assert value == "S"


# %%


def calculate_end_positions(steps):
    directions = [garden.left, garden.right, garden.up, garden.down]
    queue = [starting_position]
    for step in tqdm(range(steps)):
        new_queue = set()
        while queue:
            position = queue.pop(0)
            for direction in directions:
                value, new_position = direction(position)
                if value is None:
                    print(position)
                if value is not None and value != "#":
                    # print(new_position)
                    new_queue.add(new_position)
        queue = list(new_queue)

    return len(queue)


# %%

steps = 64
n_positions = calculate_end_positions(steps)
print("solution 1", n_positions)

# %%
import numpy as np

steps = 26501365
# garden is quadratic max x max y is the same
n = (steps - 65) / (garden.max_x + 1) // 2
n

# %%

a0 = calculate_end_positions(65)  # steps after 65
a1 = calculate_end_positions(65 + 131)  # steps after 65+131
a2 = calculate_end_positions(65 + 2 * 131)  # steps after 65+2*131

print(a0, a1, a2)

# %%

# https://de.wikipedia.org/wiki/Vandermonde-Matrix
vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
b = np.array([a0, a1, a2])
x = np.linalg.solve(vandermonde, b).astype(np.int64)
x

# %%
solution = x[0] * n * n + x[1] * n + x[2]
solution
