#%%

from pathlib import Path
import string
import re


DATA_PATH = Path("22/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

with (DATA_PATH / "input_path.txt").open() as infile:
    path = infile.read()

#%%

max_row_length = max([len(row) for row in data])
data = [row.ljust(max_row_length) for row in data]


#%%
side_a = [row[50:100] for row in data[:50]]
side_b = [row[100:150] for row in data[:50]]

side_c = [row[50:100] for row in data[50:100]]

side_e = [row[:50] for row in data[100:150]]
side_d = [row[50:100] for row in data[100:150]]

side_f = [row[:50] for row in data[150:]]

all_sides = {
    "a": side_a,
    "b": side_b,
    "c": side_c,
    "d": side_d,
    "e": side_e,
    "f": side_f,
}

for s in all_sides:
    print(s, len(all_sides[s]), len(all_sides[s][0]))

#%%

connections = {"a": {}, "b": {}, "c": {}, "d": {}, "e": {}, "f": {}}

for i in range(50):
    for j in range(50):
        connections["a"][i, j] = {}
        connections["b"][i, j] = {}
        connections["c"][i, j] = {}
        connections["d"][i, j] = {}
        connections["e"][i, j] = {}
        connections["f"][i, j] = {}

for i in range(50):
    # side a
    connections["a"][i, 49]["right"] = ("b", (i, 0), "right")
    connections["a"][i, 0]["left"] = ("e", (49 - i, 0), "right")
    connections["a"][49, i]["down"] = ("c", (0, i), "down")
    connections["a"][0, i]["up"] = ("f", (i, 0), "right")

    # side b
    connections["b"][0, i]["up"] = ("f", (49, i), "up")
    connections["b"][49, i]["down"] = ("c", (i, 49), "left")
    connections["b"][i, 0]["left"] = ("a", (i, 49), "left")
    connections["b"][i, 49]["right"] = ("d", (49 - i, 49), "left")

    # side c
    connections["c"][0, i]["up"] = ("a", (49, i), "up")
    connections["c"][49, i]["down"] = ("d", (0, i), "down")
    connections["c"][i, 49]["right"] = ("b", (49, i), "up")
    connections["c"][i, 0]["left"] = ("e", (0, i), "down")

    # side d
    connections["d"][0, i]["up"] = ("c", (49, i), "up")
    connections["d"][i, 0]["left"] = ("e", (i, 49), "left")
    connections["d"][49, i]["down"] = ("f", (i, 49), "left")
    connections["d"][i, 49]["right"] = ("b", (49 - i, 49), "left")

    # side e
    connections["e"][i, 49]["right"] = ("d", (i, 0), "right")
    connections["e"][0, i]["up"] = ("c", (i, 0), "right")
    connections["e"][i, 0]["left"] = ("a", (49 - i, 0), "right")
    connections["e"][49, i]["down"] = ("f", (0, i), "down")

    # side f
    connections["f"][0, i]["up"] = ("e", (49, i), "up")
    connections["f"][i, 0]["left"] = ("a", (0, i), "down")
    connections["f"][49, i]["down"] = ("b", (0, i), "down")
    connections["f"][i, 49]["right"] = ("d", (49, i), "up")

connections

#%%
assert connections["a"][0, 0]["left"] == ("e", (49, 0), "right"), "fail"
assert connections["a"][0, 0]["up"] == ("f", (0, 0), "right"), "fail"
assert connections["a"][0, 49]["right"] == ("b", (0, 0), "right"), "fail"
assert connections["a"][0, 49]["up"] == ("f", (49, 0), "right"), "fail"
assert connections["a"][49, 49]["right"] == ("b", (49, 0), "right"), "fail"
assert connections["a"][49, 49]["down"] == ("c", (0, 49), "down"), "fail"
assert connections["a"][49, 0]["left"] == ("e", (0, 0), "right"), "fail"
assert connections["a"][49, 0]["down"] == ("c", (0, 0), "down"), "fail"

#%%
assert connections["b"][0, 0]["left"] == ("a", (0, 49), "left"), "fail"
assert connections["b"][0, 0]["up"] == ("f", (49, 0), "up"), "fail"
assert connections["b"][0, 49]["right"] == ("d", (49, 49), "left"), "fail"
assert connections["b"][0, 49]["up"] == ("f", (49, 49), "up"), "fail"
assert connections["b"][49, 49]["right"] == ("d", (0, 49), "left"), "fail"
assert connections["b"][49, 49]["down"] == ("c", (49, 49), "left"), "fail"
assert connections["b"][49, 0]["left"] == ("a", (49, 49), "left"), "fail"
assert connections["b"][49, 0]["down"] == ("c", (0, 49), "left"), "fail"


#%%
assert connections["c"][0, 0]["left"] == ("e", (0, 0), "down"), "fail"
assert connections["c"][0, 0]["up"] == ("a", (49, 0), "up"), "fail"
assert connections["c"][0, 49]["right"] == ("b", (49, 0), "up"), "fail"
assert connections["c"][0, 49]["up"] == ("a", (49, 49), "up"), "fail"
assert connections["c"][49, 49]["right"] == ("b", (49, 49), "up"), "fail"
assert connections["c"][49, 49]["down"] == ("d", (0, 49), "down"), "fail"
assert connections["c"][49, 0]["left"] == ("e", (0, 49), "down"), "fail"
assert connections["c"][49, 0]["down"] == ("d", (0, 0), "down"), "fail"

#%%
assert connections["d"][0, 0]["left"] == ("e", (0, 49), "left"), "fail"
assert connections["d"][0, 0]["up"] == ("c", (49, 0), "up"), "fail"
assert connections["d"][0, 49]["right"] == ("b", (49, 49), "left"), "fail"
assert connections["d"][0, 49]["up"] == ("c", (49, 49), "up"), "fail"
assert connections["d"][49, 49]["right"] == ("b", (0, 49), "left"), "fail"
assert connections["d"][49, 49]["down"] == ("f", (49, 49), "left"), "fail"
assert connections["d"][49, 0]["left"] == ("e", (49, 49), "left"), "fail"
assert connections["d"][49, 0]["down"] == ("f", (0, 49), "left"), "fail"

#%%
assert connections["e"][0, 0]["left"] == ("a", (49, 0), "right"), "fail"
assert connections["e"][0, 0]["up"] == ("c", (0, 0), "right"), "fail"
assert connections["e"][0, 49]["right"] == ("d", (0, 0), "right"), "fail"
assert connections["e"][0, 49]["up"] == ("c", (49, 0), "right"), "fail"
assert connections["e"][49, 49]["down"] == ("f", (0, 49), "down"), "fail"
assert connections["e"][49, 49]["right"] == ("d", (49, 0), "right"), "fail"
assert connections["e"][49, 0]["left"] == ("a", (0, 0), "right"), "fail"
assert connections["e"][49, 0]["down"] == ("f", (0, 0), "down"), "fail"

#%%

assert connections["f"][0, 0]["left"] == ("a", (0, 0), "down"), "fail"
assert connections["f"][0, 0]["up"] == ("e", (49, 0), "up"), "fail"
assert connections["f"][0, 49]["right"] == ("d", (49, 0), "up"), "fail"
assert connections["f"][0, 49]["up"] == ("e", (49, 49), "up"), "fail"
assert connections["f"][49, 49]["down"] == ("b", (0, 49), "down"), "fail"
assert connections["f"][49, 49]["right"] == ("d", (49, 49), "up"), "fail"
assert connections["f"][49, 0]["left"] == ("a", (0, 49), "down"), "fail"
assert connections["f"][49, 0]["down"] == ("b", (0, 0), "down"), "fail"


#%%

direction_mapper = {
    "R": {"down": "left", "left": "up", "up": "right", "right": "down"},
    "L": {"down": "right", "left": "down", "up": "left", "right": "up"},
}

turn_to = ["R"]
for d in path:
    if d in string.ascii_uppercase:
        turn_to.append(d)

moves = list(map(int, re.split("|".join(string.ascii_uppercase), path)))

#%%


def right(coords):
    return coords[0], coords[1] + 1


def left(coords):
    return coords[0], coords[1] - 1


def down(coords):
    return coords[0] + 1, coords[1]


def up(coords):
    return coords[0] - 1, coords[1]


move_to = {"right": right, "left": left, "down": down, "up": up}

position = ("a", (0, 0))
direction = "up"

while moves:
    turn = turn_to.pop(0)
    direction = direction_mapper[turn][direction]
    number_of_moves = moves.pop(0)

    for _ in range(number_of_moves):
        if direction in connections[position[0]][position[1]]:
            side, coords, new_direction = connections[position[0]][position[1]][
                direction
            ]
            if all_sides[side][coords[0]][coords[1]] != "#":
                position = (side, coords)
                direction = new_direction
        else:
            side = position[0]
            coords = move_to[direction](position[1])
            if all_sides[side][coords[0]][coords[1]] != "#":
                position = (side, coords)
        print(position, direction)

print(position, direction)

#%%


side, coords = position

coord_mapper = {
    "a": (0, 50),
    "b": (0, 100),
    "c": (50, 50),
    "d": (100, 50),
    "e": (100, 0),
    "f": (150, 0),
}
dir_points = {"right": 0, "down": 1, "left": 2, "up": 3}

solution = (
    (coords[0] + coord_mapper[side][0] + 1) * 1000
    + (coords[1] + coord_mapper[side][1] + 1) * 4
    + dir_points[direction]
)

print(solution)

#%%
