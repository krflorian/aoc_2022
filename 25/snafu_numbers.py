#%%

from pathlib import Path


DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")


#%%

snafu_dict = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}

multiplicators = [1, 5]
for _ in range(60):
    multiplicators.append(multiplicators[-1] * 5)
multiplicators

#%%

total_value = 0

for row in data:
    decimal_value = 0
    for mult, val in zip(multiplicators, reversed(row)):
        decimal_value += mult * (snafu_dict[val])
    print(row, " | ", decimal_value)
    total_value += decimal_value

total_value

#%%

from pulp import *

stellen = 21

prob = LpProblem("snafu problem", LpMaximize)

variables = []
for i in range(stellen):
    for snafu in snafu_dict:
        variables.append(f"{i}_{snafu}")

vars = LpVariable.dicts("snafu", variables, cat="Binary")

prob += pulp.lpSum([var for key, var in vars.items()])

for i in range(stellen):
    prob += lpSum([vars[f"{i}_{snafu}"] for snafu in snafu_dict]) <= 1

prob += (
    lpSum(
        [
            var * (multiplicators[int(key[:-2])] * snafu_dict[key[-1]])
            for key, var in vars.items()
        ]
    )
    == total_value
)

prob.solve()
print("Status:", LpStatus[prob.status])

solution = "".join(
    list(
        reversed(
            "".join([key[-1] for key, var in vars.items() if var.value() == 1]).rstrip(
                "0"
            )
        )
    )
)
print("snafu value = ", solution)

# %%

row = "2-2=21=0021=-02-1=-0"

decimal_value = 0
for mult, val in zip(multiplicators, reversed(row)):
    decimal_value += mult * (snafu_dict[val])
print(row, " | ", decimal_value)
decimal_value

# %%
