
#%%
import string 

from pathlib import Path

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")


values = {
    st: i+1 for (i, st) in enumerate(string.ascii_lowercase)
}

uppercase_values = {
    st: i+27 for (i, st) in enumerate(string.ascii_uppercase)
}

values.update(uppercase_values)

#%%

total_value = 0
group = []
for rucksack in data:
    group.append(set(rucksack))

    if len(group) == 3: 
        items = group[0].intersection(group[1])
        item = items.intersection(group[2])
        print(item)
        total_value += values[list(item)[0]]
        group = []
        
total_value