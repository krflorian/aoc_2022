# %%
import re
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data

# %%

games = {}
for row in data:
    game, cubes = row.split(":")
    _, idx = game.split(" ")
    cubes = cubes.split(";")
    cubes = [cube_set.split(",") for cube_set in cubes]
    games[int(idx)] = []
    for set in cubes:
        set_dict = {}
        for cube in set:
            num, color = cube.strip().split(" ")
            set_dict[color] = int(num)
        games[int(idx)].append(set_dict)

games
# print(game, cubes)
# %%
# part 1
max_values = {"red": 12, "green": 13, "blue": 14}
good_games = 0
for idx, game in games.items():
    if all([num <= max_values[color] for set in game for color, num in set.items()]):
        print(idx)
        good_games += idx

print("solution", good_games)

# %%
# part 2

total_power = 0
for idx, game in games.items():
    colors = {"red": 0, "blue": 0, "green": 0}
    for set in game:
        for color in colors.keys():
            if set.get(color, 0) > colors[color]:
                colors[color] = set[color]
    cube_power = colors["red"] * colors["blue"] * colors["green"]
    total_power += cube_power

total_power
