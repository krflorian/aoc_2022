# %%

from pathlib import Path
import pandas as pd

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data = pd.DataFrame(
    {
        idx: row
        for (idx, row) in enumerate([list(map(int, row.split())) for row in data])
    }
)


# %%
# part 1

solution = 0
col = 0

for col in data.columns:
    diffs = []
    diffs.append(list(data[col]))
    diff_col = data[col].diff(1)
    diffs.append(list(diff_col))
    while diff_col.fillna(0).any():
        diff_col = diff_col.diff(1)
        diffs.append(list(diff_col))

    last_diff = 0
    for diff in reversed(diffs):
        this_diff = diff[-1]
        last_diff = this_diff + last_diff

    print(last_diff)
    solution += last_diff

print("_________________")
print("solution:", solution)

# %%
# part 2

solution = 0
col = 0

for col in data.columns:
    diffs = []
    diffs.append(list(data[col]))
    diff_col = data[col].diff(1)
    diffs.append(list(diff_col[~diff_col.isna()]))
    while diff_col.fillna(0).any():
        diff_col = diff_col.diff(1)
        diffs.append(list(diff_col[~diff_col.isna()]))

    last_diff = 0
    for diff in reversed(diffs):
        this_diff = diff[0]
        last_diff = this_diff - last_diff

    print(last_diff)
    solution += last_diff

print("_________________")
print("solution:", solution)

# %%
