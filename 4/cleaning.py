
#%%
from pathlib import Path
import re

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")

data = [re.split(",|-", row) for row in data]

#%%


def check_inside(number, range):
    if int(range[0]) <= int(number) <= int(range[1]):
        return True 
    return False 


counter = 0
for row in data: 
    if check_inside(row[0], row[2:]):
        counter += 1
        #print(row, True) 
    elif check_inside(row[1], row[2:]):
        counter += 1
        #print(row, True) 
    elif check_inside(row[2], row[:2]):
        counter += 1
    elif check_inside(row[3], row[:2]):
        counter += 1
    else:
        print(row, False)

counter



