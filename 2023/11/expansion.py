# %%
from pathlib import Path
from map_2d import Map2D

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

empty_y = []
for row_idx, row in enumerate(reversed(data)):
    if all([c == "." for c in row]):
        empty_y.append(row_idx)

empty_x = []
columns = []
for idx in range(len(data[0])):
    columns.append([])
    for row in reversed(data):
        columns[-1].append(row[idx])
    if all([val == "." for val in columns[-1]]):
        empty_x.append(idx)


# %%

map2d = Map2D(data)
nodes = iter(map2d)
stars = []
for val, x, y in nodes:
    if val == "#":
        stars.append((x, y))

print(map2d)


# %%
# part 1

from itertools import combinations

empty_space = 1000000


def manhatten_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


path_lengths = 0
for star, star_1 in combinations(stars, r=2):
    dist = manhatten_distance(star[0], star[1], star_1[0], star_1[1])

    for x in empty_x:
        if (x > min(star[0], star_1[0])) and (x < max(star[0], star_1[0])):
            dist += empty_space - 1
    for y in empty_y:
        if (y > min(star[1], star_1[1])) and (y < max(star[1], star_1[1])):
            dist += empty_space - 1

    path_lengths += dist
path_lengths

# %%
