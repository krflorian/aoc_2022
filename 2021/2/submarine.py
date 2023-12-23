# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data = [d.split(" ") for d in data]
data = [(d[0], int(d[1])) for d in data]
data

# %%


def forward(steps, position):
    position[0] += steps
    position[1] += position[2] * steps
    return position


def down(steps, position):
    position[2] += steps
    return position


def up(steps, position):
    position[2] -= steps
    return position


movement = {"forward": forward, "down": down, "up": up}

position = [0, 0, 0]  # horizontal, depth, aim
for move in data:
    position = movement[move[0]](move[1], position)
position

# %%

position[0] * position[1]
