
#%%
import numpy as np 
from pathlib import Path

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")        


#%%
"""
# part 1 

visible_grid = np.zeros((len(data), len(data[0])))

for row_id, row in enumerate(data): 

    highest = -1
    hightest_top = -1
    for col_id, val in enumerate(row):
        # from left 
        if int(val) > highest: 
            visible_grid[row_id, col_id] = 1
            highest = int(val)

        # top to bottom
        if int(data[col_id][row_id]) > hightest_top: 
            visible_grid[col_id, row_id] = 1
            hightest_top = int(data[col_id][row_id]) 

    highest = -1 
    highest_bottom = -1
    for col_id, val in reversed(list(enumerate(row))):
    
        # from right to left
        if int(val) > highest: 
            visible_grid[row_id, col_id] = 1
            highest = int(val)
        
        # bottom to top 
        if int(data[col_id][row_id]) > highest_bottom: 
            visible_grid[col_id, row_id] = 1
            highest_bottom = int(data[col_id][row_id]) 

visible_grid
np.sum(visible_grid)

"""
#%%


visible_grid = np.ones((len(data), len(data[0])))

# for every tree in grid 
for row_id, row in enumerate(data): 
    for col_id, val in enumerate(row):

        # go right 
        score = 0 
        for idx in range(col_id+1, len(data[0])):
            score += 1
            if (int(data[row_id][idx]) >= int(val)) or (idx == len(data)-1):
                visible_grid[row_id, col_id] *= score
                break 
        
        # go left 
        score = 0
        for idx in reversed(range(col_id)):
            score += 1
            if (int(data[row_id][idx]) >= int(val)) or (idx == 0):
                visible_grid[row_id, col_id] *= score
                break 
          
        # go down 
        score = 0 
        for idx in range(row_id+1, len(data)):
            score += 1
            if (int(data[idx][col_id]) >= int(val)) or (idx == len(data)-1):
                visible_grid[row_id, col_id] *= score
                break 

        # go up 
        score = 0 
        for idx in reversed(range(row_id)):
            score += 1
            if (int(data[idx][col_id]) >= int(val)) or (idx == 0):
                visible_grid[row_id, col_id] *= score
                break 

#%%
visible_grid[1:-1, 1:-1]

#%%

np.max(visible_grid[1:-1, 1:-1])

# %%

