#%%

from pathlib import Path
import pandas as pd
from tqdm import tqdm

DATA_PATH = Path("15/data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

coordinates = []
for row in data:
    row = row.split(" ")
    coordinate_pair = []
    for txt in row:
        if txt.startswith("x") or txt.startswith("y"):
            txt = txt.strip("yx=,:")
            coordinate_pair.append(int(txt))
    coordinates.append(coordinate_pair)

#%%
def manhatten_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


df = pd.DataFrame(
    data=coordinates, columns=["sensor_x", "sensor_y", "beacon_x", "beacon_y"]
)


df["distance"] = abs(df["sensor_x"] - df["beacon_x"]) + abs(
    df["sensor_y"] - df["beacon_y"]
)
df.head()

#%%
# pt 2
from ortools.sat.python import cp_model

max_value = 4_000_000

# Create the CP-SAT model.
model = cp_model.CpModel()

# Declare our two primary variables.
x = model.NewIntVar(0, max_value, "x")
y = model.NewIntVar(0, max_value, "y")

for idx, row in df.iterrows():

    # add in var that can be negative
    _a = model.NewIntVar(-max_value, max_value * 1000, f"_abs_value_{idx}_x")
    model.Add(_a == row["sensor_x"] - x)
    # add absolute int var
    a = model.NewIntVar(0, max_value, f"abs_value_{idx}_x")
    model.AddMaxEquality(a, [_a, -_a])

    _b = model.NewIntVar(-max_value, max_value, f"_abs_value_{idx}_y")
    model.Add(_b == row["sensor_y"] - y)
    b = model.NewIntVar(0, max_value, f"abs_value_{idx}_y")
    model.AddMaxEquality(b, [_b, -_b])

    model.Add(a + b > row["distance"])

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("x = %i" % solver.Value(x))
    print("y = %i" % solver.Value(y))
    print(f"solution: {solver.Value(x)*max_value + solver.Value(y)}")

else:
    print("no solution found")

#%%
# pt 1
y = 20
beacons = df[["beacon_x", "beacon_y"]].drop_duplicates()

beacons_at_y = len(beacons.query("beacon_y == @y"))

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
