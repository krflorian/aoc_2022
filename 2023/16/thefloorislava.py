# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
data


# %%
from map_2d import Map2D


cave = Map2D(data)
print(cave)


# %%


directions = {
    "right": cave.right,
    "left": cave.left,
    "up": cave.up,
    "down": cave.down,
}


def process_position(beam, value, coordinate, beams, seen_beams):
    if value is None:
        return
    else:
        energized_tiles.add(coordinate)

    seen = (coordinate[0], coordinate[1], beam["direction"])
    if seen in seen_beams:
        return
    else:
        seen_beams.append(seen)

    if value == ".":
        beams.append({"position": coordinate, "direction": beam["direction"]})
    elif value == "|":
        if beam["direction"] in ["left", "right"]:
            beams.append({"position": coordinate, "direction": "up"})
            beams.append({"position": coordinate, "direction": "down"})
        else:
            beams.append({"position": coordinate, "direction": beam["direction"]})
    elif value == "-":
        if beam["direction"] in ["up", "down"]:
            beams.append({"position": coordinate, "direction": "left"})
            beams.append({"position": coordinate, "direction": "right"})
        else:
            beams.append({"position": coordinate, "direction": beam["direction"]})
    elif value == "\\":
        if beam["direction"] == "right":
            beams.append({"position": coordinate, "direction": "down"})
        elif beam["direction"] == "left":
            beams.append({"position": coordinate, "direction": "up"})
        elif beam["direction"] == "down":
            beams.append({"position": coordinate, "direction": "right"})
        elif beam["direction"] == "up":
            beams.append({"position": coordinate, "direction": "left"})
    elif value == "/":
        if beam["direction"] == "right":
            beams.append({"position": coordinate, "direction": "up"})
        elif beam["direction"] == "left":
            beams.append({"position": coordinate, "direction": "down"})
        elif beam["direction"] == "down":
            beams.append({"position": coordinate, "direction": "left"})
        elif beam["direction"] == "up":
            beams.append({"position": coordinate, "direction": "right"})
    else:
        print("error", beam)


total_energized_tiles = []
starting_positions = []

for y in range(cave.max_y + 1):
    starting_position = (0, y)
    starting_direction = "right"
    starting_positions.append((starting_position, starting_direction))
starting_positions.append(((0, 0), "up"))
starting_positions.append(((0, cave.max_y), "down"))

for y in range(cave.max_y + 1):
    starting_position = (cave.max_x, y)
    starting_direction = "left"
    starting_positions.append((starting_position, starting_direction))
starting_positions.append(((cave.max_x, 0), "up"))
starting_positions.append(((cave.max_x, cave.max_y), "down"))

for x in range(1, cave.max_x):
    starting_position = (x, 0)
    starting_direction = "up"
    starting_positions.append((starting_position, starting_direction))
for x in range(1, cave.max_x):
    starting_position = (x, cave.max_y)
    starting_direction = "down"
    starting_positions.append((starting_position, starting_direction))
starting_positions

# %%
from tqdm import tqdm

for starting_position, starting_direction in tqdm(starting_positions):
    beam = {"position": starting_position, "direction": starting_direction}
    value = cave(starting_position)

    beams = []
    seen_beams = []
    energized_tiles = set()

    process_position(beam, value, starting_position, beams, seen_beams)

    while beams:
        beam = beams.pop(0)
        value, coordinate = directions[beam["direction"]](beam["position"])
        process_position(beam, value, coordinate, beams, seen_beams)

    # print("solution ", len(list(energized_tiles)))
    total_energized_tiles.append(len(list(energized_tiles)))

print("final solution ", max(total_energized_tiles))

# %%
