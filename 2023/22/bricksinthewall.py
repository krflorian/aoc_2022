# %%
from dataclasses import dataclass
from pathlib import Path
from tqdm import tqdm

with Path("test_data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
data


# %%
@dataclass
class Brick:
    x: list[int]
    y: list[int]
    z: list[int]


bricks: list[Brick] = []
for row in data:
    start, end = row.split("~")
    start = list(map(int, start.split(",")))
    end = list(map(int, end.split(",")))
    bricks.append(Brick([start[0], end[0]], [start[1], end[1]], [start[2], end[2]]))

bricks

# %%

for brick in bricks:
    bricks_under_brick = [
        b for b in bricks if b.y[0] <= brick.y[0] and b.y[1] <= brick.y[1]
    ]
    print(bricks_under_brick)
