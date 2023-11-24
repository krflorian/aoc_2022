
#%%
from pathlib import Path
from dataclasses import dataclass
from functools import total_ordering

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")
    data = [row.split(" ") for row in data]
data

#%%


win_conditions = {
    "A":{
        "Y": "A", 
        "Z": "B",
        "X": "C"
    },
    "B":{
        "Y": "B", 
        "Z": "C",
        "X": "A"
    },
    "C":{
        "Y": "C", 
        "Z": "A",
        "X": "B"
    }
}

#%%

point_dict = {
    "A": 1, 
    "B": 2, 
    "C": 3, 
    "Z": 6, 
    "Y": 3, 
    "X": 0
}


total_points = 0
for game in data: 
    my_hand = win_conditions[game[0]][game[1]]

    # hand 
    total_points += point_dict[my_hand]

    # win or loose 
    total_points += point_dict[game[1]]
    
total_points
