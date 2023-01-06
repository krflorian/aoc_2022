#%%

from pathlib import Path
import matplotlib.pyplot as plt

import re
from tqdm import tqdm

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
# data

#%%
from collections import namedtuple

Elf = namedtuple("Elf", ["x", "y"])


elves = []

for y, row in enumerate(reversed(data)):
    for x, val in enumerate(row):
        if val == "#":
            elves.append(Elf(x, y))

len(elves)

plt.plot([elf.x for elf in elves], [elf.y for elf in elves], "o")
plt.xlim([-5, len(data[0]) + 5])
plt.ylim([-5, len(data) + 5])

#%%

# north
def check_north(elf, elf_positions):
    positions = set(
        [
            Elf(elf.x, elf.y + 1),
            Elf(elf.x + 1, elf.y + 1),
            Elf(elf.x - 1, elf.y + 1),
        ]
    )
    elfs_around = elf_positions.intersection(positions)
    if not elfs_around:
        new_position = Elf(elf.x, elf.y + 1)
        return True, (new_position, elf)
    return False, None


# south
def check_south(elf, elf_positions):
    positions = set(
        [
            Elf(elf.x, elf.y - 1),
            Elf(elf.x + 1, elf.y - 1),
            Elf(elf.x - 1, elf.y - 1),
        ]
    )
    elfs_around = elf_positions.intersection(positions)
    if not elfs_around:
        new_position = Elf(elf.x, elf.y - 1)
        return True, (new_position, elf)
    return False, None


# west
def check_west(elf, elf_positions):
    positions = set(
        [
            Elf(elf.x - 1, elf.y),
            Elf(elf.x - 1, elf.y - 1),
            Elf(elf.x - 1, elf.y + 1),
        ]
    )
    elfs_around = elf_positions.intersection(positions)
    if not elfs_around:
        new_position = Elf(elf.x - 1, elf.y)
        return True, (new_position, elf)
    return False, None


# east
def check_east(elf, elf_positions):
    positions = set(
        [
            Elf(elf.x + 1, elf.y),
            Elf(elf.x + 1, elf.y - 1),
            Elf(elf.x + 1, elf.y + 1),
        ]
    )
    elfs_around = elf_positions.intersection(positions)
    if not elfs_around:
        new_position = Elf(elf.x + 1, elf.y)
        return True, (new_position, elf)
    return False, None


def check_move(elf, elf_positions, checks):

    possible_moves = [
        Elf(elf.x + 1, elf.y),
        Elf(elf.x - 1, elf.y),
        Elf(elf.x, elf.y + 1),
        Elf(elf.x, elf.y - 1),
        Elf(elf.x + 1, elf.y + 1),
        Elf(elf.x - 1, elf.y - 1),
        Elf(elf.x + 1, elf.y - 1),
        Elf(elf.x - 1, elf.y + 1),
    ]

    elfs_around = elf_positions.intersection(set(possible_moves))
    if not elfs_around:
        return False, elf

    for check in checks:
        moved, proposal = check(elf, elf_positions)
        if moved:
            return moved, proposal

    return False, elf


#%%

checks = [check_north, check_south, check_west, check_east]

for i in tqdm(range(10000)):

    # check moves
    moving_elves = []
    new_elves = []

    for elf in elves:

        moves, proposed_move = check_move(elf, set(elves), checks)

        if moves:
            moving_elves.append(proposed_move)
        else:
            new_elves.append(elf)

    if not moving_elves:
        print(f"round {i+1} no elf moves!")
        break

    # move elves
    elves_move = 0
    while moving_elves:
        proposed_position, old_position = moving_elves.pop(0)

        other_elves = [elf for elf in moving_elves if elf[0] == proposed_position]

        if other_elves:
            new_elves.append(old_position)
            new_elves.extend([elf[1] for elf in other_elves])
            moving_elves = [elf for elf in moving_elves if elf not in other_elves]
        else:
            elves_move += 1
            new_elves.append(proposed_position)

    if elves_move == 0:
        print(f"round {i+1} no elf moves!")
        break
    # else:
    # print(f"round {i+1}: {elves_move} elves move")

    elves = new_elves[:]
    check = checks.pop(0)
    checks.append(check)

#%%

print(i)
plt.plot([elf.x for elf in elves], [elf.y for elf in elves], "o")
plt.xlim([-5, len(data[0]) + 5])
plt.ylim([-5, len(data) + 5])
plt.show()


#%%

x_coordinates = [elf.x for elf in new_elves]
y_coordinates = [elf.y for elf in new_elves]

max_x = max(x_coordinates)
max_y = max(y_coordinates)
min_x = min(x_coordinates)
min_y = min(y_coordinates)

(max_x + 1 - min_x) * (max_y + 1 - min_y) - len(new_elves)

#%%
