
#%%
from pathlib import Path
from dataclasses import dataclass
from functools import total_ordering

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")


#%%

@total_ordering
@dataclass
class Elf():
    calories:int

    def __lt__(self, other):
        return ((self.calories) < (other.calories))

    def __eq__(self, other: object) -> bool:
        return self.calories == other.calories

#%%

elf1 = Elf(calories = 10)
elf2 = Elf(calories = 5)

elf1 == elf2 


#%%


current_elf = Elf(calories = 0)
all_elves = []

for val in data:
    if val == "":
        all_elves.append(current_elf)
        current_elf = Elf(calories=0)
    else:
        current_elf.calories += int(val)

all_elves

#%%

sum([elf.calories for elf in reversed(sorted(all_elves))][:3])


#%%


