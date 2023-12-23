# %%
from pathlib import Path


with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

data = [int(d) for d in data]
data[:10]

# %%

goes_up = 0

for i in range(0, len(data) - 3):
    current_window = data[i : i + 3]
    next_window = data[i + 1 : i + 4]
    if sum(next_window) > sum(current_window):
        goes_up += 1
    # if data[i] > data[i - 1]:
    # goes_up += 1

goes_up
