#%%
from pathlib import Path
from itertools import combinations

DATA_PATH = Path("18/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data

#%%


def is_connected(cube, other):
    all_sides = [coor == other_coor for (coor, other_coor) in zip(cube, other)]

    if sum(all_sides) == 2:
        idx = all_sides.index(False)
        coor = cube[idx]
        other_coor = other[idx]
        if coor - 1 <= other_coor <= coor + 1:
            return True
    return False


#%%

all_cubes = [list(map(int, row.split(","))) for row in data]
all_cubes[0]

#%%

connected_sides = 0
for cube, other_cube in combinations(all_cubes, 2):
    if is_connected(cube, other_cube):
        connected_sides += 1

all_sides = len(all_cubes) * 6
print(f"solution = {all_sides-connected_sides*2}")

#%%

all_x = [c[0] for c in all_cubes]
max_x = max(all_x) + 1

all_y = [c[1] for c in all_cubes]
max_y = max(all_y) + 1

all_z = [c[2] for c in all_cubes]
max_z = max(all_z) + 1

#%%


# all_cubes = [[1, 1, 1], [1, 1, 2]]

queue = []
visited = []
queue.append([0, 0, 0])
count = 0


def check(new_cube, all_cubes, visited, queue, count):
    if (new_cube not in visited) and (new_cube not in queue):
        if new_cube not in all_cubes:
            queue.append(new_cube)
        else:
            count += 1

    return count, queue


while queue:

    cube = queue.pop(0)
    visited.append(cube[:])
    # print(cube)

    # x
    n = cube[:]
    n[0] -= 1
    if -1 <= n[0] <= max_x:
        count, queue = check(n, all_cubes, visited, queue, count)

    n = cube[:]
    n[0] += 1
    if -1 <= n[0] <= max_x:
        count, queue = check(n, all_cubes, visited, queue, count)

    n = cube[:]
    n[1] -= 1
    if -1 <= n[1] <= max_y:
        count, queue = check(n, all_cubes, visited, queue, count)

    n = cube[:]
    n[1] += 1
    if -1 <= n[1] <= max_y:
        count, queue = check(n, all_cubes, visited, queue, count)

    # z
    n = cube[:]
    n[2] -= 1
    if -1 <= n[2] <= max_z:
        count, queue = check(n, all_cubes, visited, queue, count)

    n = cube[:]
    n[2] += 1
    if -1 <= n[2] <= max_z:
        count, queue = check(n, all_cubes, visited, queue, count)


count


#%%
