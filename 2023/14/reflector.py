# %%
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
data


# %%

from map_2d import Map2D

rock_map = Map2D(data)
print(rock_map)


def cycle_rocks(rock_map):
    for y in reversed(range(rock_map.max_y + 1)):
        for x in range(rock_map.max_x + 1):
            old_coordinates = (x, y)
            value = rock_map(old_coordinates)
            if value == "O":
                while True:
                    new_value, new_coordinates = rock_map.up(old_coordinates)
                    if new_value == ".":
                        rock_map.set_value(new_coordinates, "O")
                        rock_map.set_value(old_coordinates, ".")
                        old_coordinates = new_coordinates
                    else:
                        break
    for x in range(rock_map.max_x + 1):
        for y in range(rock_map.max_y + 1):
            old_coordinates = (x, y)
            value = rock_map(old_coordinates)
            if value == "O":
                while True:
                    new_value, new_coordinates = rock_map.left(old_coordinates)
                    if new_value == ".":
                        rock_map.set_value(new_coordinates, "O")
                        rock_map.set_value(old_coordinates, ".")
                        old_coordinates = new_coordinates
                    else:
                        break

    for y in range(rock_map.max_y + 1):
        for x in range(rock_map.max_x + 1):
            old_coordinates = (x, y)
            value = rock_map(old_coordinates)
            if value == "O":
                while True:
                    new_value, new_coordinates = rock_map.down(old_coordinates)
                    if new_value == ".":
                        rock_map.set_value(new_coordinates, "O")
                        rock_map.set_value(old_coordinates, ".")
                        old_coordinates = new_coordinates
                    else:
                        break
    for x in reversed(range(rock_map.max_x + 1)):
        for y in range(rock_map.max_y + 1):
            old_coordinates = (x, y)
            value = rock_map(old_coordinates)
            if value == "O":
                while True:
                    new_value, new_coordinates = rock_map.right(old_coordinates)
                    if new_value == ".":
                        rock_map.set_value(new_coordinates, "O")
                        rock_map.set_value(old_coordinates, ".")
                        old_coordinates = new_coordinates
                    else:
                        break


# %%
from tqdm import tqdm

last_seen = 0
seen_formations = []
cycles = 1000000000

for i in tqdm(range(cycles)):
    # print(rock_map)
    # print("____________")
    cycle_rocks(rock_map)

    # print(rock_map)
    # print("_________")
    formation = []
    for y in range(rock_map.max_y + 1):
        formation.append(
            "".join([rock_map.values[x][y] for x in range(rock_map.max_x + 1)])
        )
    formation = "\n".join(reversed(formation))
    if formation in seen_formations:
        for last_seen, f in enumerate(seen_formations):
            if f == formation:
                cycle_size = i - last_seen
                print("cycle size ", cycle_size)
                break
        break
    seen_formations.append(formation)


# %%

remainder = (cycles - (i + 1)) % (cycle_size)
remainder

for i in tqdm(range(remainder)):
    # print(rock_map)
    # print("____________")
    cycle_rocks(rock_map)

# %%

values = iter(rock_map)
solution = 0
for value, x, y in values:
    if value == "O":
        solution += y + 1
solution

# %%
