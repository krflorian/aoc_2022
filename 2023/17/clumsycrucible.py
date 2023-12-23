# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
data
