#%%

from pathlib import Path
import pandas as pd
from tqdm import tqdm

DATA_PATH = Path("15/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data

#%%

coordinates = []
for row in data:
    row = row.split(" ")
    coordinate_pair = []
    for txt in row:
        if txt.startswith("x") or txt.startswith("y"):
            txt = txt.strip("yx=,:")
            coordinate_pair.append(int(txt))
    coordinates.append(coordinate_pair)

coordinates[0:4]


#%%

df = pd.DataFrame(
    data=coordinates, columns=["sensor_x", "sensor_y", "beacon_x", "beacon_y"]
)
df

#%%


def manhatten_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


df["distance"] = abs(df["sensor_x"] - df["beacon_x"]) + abs(
    df["sensor_y"] - df["beacon_y"]
)
df.head()

#%%

min_x = df[["beacon_x", "sensor_x"]].min().min()
max_x = df[["beacon_x", "sensor_x"]].max().max()
print(min_x, max_x)

#%%

y = 20
beacons = df[["beacon_x", "beacon_y"]].drop_duplicates()

beacons_at_y = len(beacons.query("beacon_y == @y"))
beacons_at_y
#%%

all_x = set()
for idx, row in df.iterrows():
    max_dist = row["distance"] - abs(row["sensor_y"] - y)
    if max_dist > 0:
        print(f"working on sensor {idx}")
        # print(idx, max_dist)
        for i in range(row["sensor_x"] - max_dist, row["sensor_x"] + max_dist + 1):
            all_x.add(i)

# all_x

#%%

print("solution: first part", len(all_x) - beacons_at_y)

#%%

points_to_check = set()

for row_id, row in df.iterrows():
    x = row["sensor_x"]
    y = row["sensor_y"]
    dist = row["distance"]

    print(x, y, dist)

    next_x = x + dist + 1
    next_y = y
    if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
        points_to_check.add((next_x, next_y))

    # from right to top
    while (next_x, next_y) != (x, y + dist + 1):
        next_x -= 1
        next_y += 1

        if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
            points_to_check.add((next_x, next_y))

    print(len(points_to_check))

    # from top to left
    if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
        points_to_check.add((next_x, next_y))
    while (next_x, next_y) != (x - dist - 1, y):
        next_x -= 1
        next_y -= 1

        if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
            points_to_check.add((next_x, next_y))

    print(len(points_to_check))

    # from left to bottom
    if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
        points_to_check.add((next_x, next_y))
    while (next_x, next_y) != (x, y - dist - 1):
        next_x += 1
        next_y -= 1

        if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
            points_to_check.add((next_x, next_y))

    print(len(points_to_check))

    # from bottom to right
    if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
        points_to_check.add((next_x, next_y))
    while (next_x, next_y) != (x + dist + 1, y):
        next_x += 1
        next_y += 1

        if (0 <= next_x <= 4_000_000) and (0 <= next_y <= 4_000_000):
            points_to_check.add((next_x, next_y))

    print(len(points_to_check))
print("added all relevant points! ")

#%%


for x, y in points_to_check:
    break

df["can_reach"] = abs(df["sensor_x"] - x) + abs(df["sensor_y"] - y) <= df["distance"]

print(x, y)
df.loc[df["can_reach"]]

#%%

for x, y in tqdm(points_to_check):
    df["can reach"] = (
        abs(df["sensor_x"] - x) + abs(df["sensor_y"] - y) <= df["distance"]
    )
    if not any(df["can reach"]):
        print("found point that nobody can reach")
        print(x, y)
        break


#%%

import matplotlib.pyplot as plt


for idx, row in df.iterrows():
    x = row["sensor_x"]
    y = row["sensor_y"]
    dist = row["distance"]
    plt.fill(
        [x, x + dist, x + dist, x, x, x - dist, x - dist, x],
        [y + dist, y, y, y - dist, y - dist, y, y, y + dist],
        "b",
    )
    # plt.plot([x + dist, x], [y, y - dist])
    # plt.plot([x, x - dist], [y - dist, y])
    # plt.plot([x - dist, x], [y, y + dist])
plt.plot(
    [0, 4000000, 4000000, 4000000, 4000000, 0, 0, 0],
    [0, 0, 0, 4000000, 4000000, 4000000, 0, 4000000],
    "r",
)
plt.show()

#%%
from ortools.sat.python import cp_model

model = cp_model.CpModel()

var_upper_bound = 4_000_000
M = var_upper_bound * 1000
x = model.NewIntVar(0, var_upper_bound, "x")
y = model.NewIntVar(0, var_upper_bound, "y")


#%%
# constraints
for idx, row in df.iterrows():
    bin_x = model.NewBoolVar(f"bin_x_{idx}")
    bin_y = model.NewBoolVar(f"bin_y_{idx}")

    abs_x = model.NewIntVar(0, var_upper_bound * 1000, f"abs_x_{idx}")
    abs_y = model.NewIntVar(0, var_upper_bound * 1000, f"abs_y_{idx}")

    model.Add((row["sensor_x"] - x) + M * bin_x == abs_x)
    model.Add((-(row["sensor_x"] - x) + M * (1 - bin_x)) == abs_x)

    model.Add(
        ((row["sensor_x"] - x) + M * bin_x) + ((row["sensor_y"] - y) + M * bin_y)
        > row["distance"]
    )
    model.Add(
        (-(row["sensor_x"] - x) + M * (1 - abs_x))
        + (-(row["sensor_y"] - y) + M * (1 - abs_y))
        > row["distance"]
    )


#%%

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("x = %i" % solver.Value(x))
    print("y = %i" % solver.Value(y))
else:
    print("No solution found.")


#%%
x = 2458402

df["distance_signal"] = abs(df["sensor_x"] - x)
df["closer"] = df["distance"] - 1000000 < df["distance_signal"]

df

#%%

from ortools.sat.python import cp_model

model = cp_model.CpModel()

var_upper_bound = 20
x = model.NewIntVar(0, var_upper_bound, "x")
y = model.NewIntVar(0, var_upper_bound, "x")


beacon_x = 10
beacon_y = 10
distance = 5
M = 1000

abs_x = model.NewIntVar(0, 1, "abs_x")
abs_y = model.NewIntVar(0, 1, "abs_y")
model.Add(((beacon_x - x) + M * abs_x) + ((beacon_y - y) + M * abs_y) >= distance)
model.Add(
    (-(beacon_x - x) + M * (1 - abs_x)) + (-(beacon_y - y) + M * (1 - abs_y))
    >= distance
)

solver = cp_model.CpSolver()
status = solver.Solve(model)


if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("x = %i" % solver.Value(x))
    print("y = %i" % solver.Value(y))
    print("abs_x = %i" % solver.Value(abs_x))
    print("abs_y = %i" % solver.Value(abs_y))

else:
    print("No solution found.")


value_x = solver.Value(x)
value_y = solver.Value(y)

print("manhatten distance:", abs(beacon_x - value_x) + abs(beacon_y - value_y))


#%%

x = 598586
y = 99571
distance = 888017

print((x - 0) + (y - 0), distance)
print(-((x - 0) + (y - 0)), -distance)
print(abs(x - 0) + abs(y - 0))
