
#%%
from pathlib import Path
from collections import namedtuple

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")


#%%
from dataclasses import dataclass 

File = namedtuple('File', ['name', 'size'])

@dataclass 
class Directory():
    name:str 
    parent:str 
    files:list[File]
    children:list

    @property
    def size(self):
        size = sum(file.size for file in self.files)
        size += sum(c.size for c in self.children)
        return size 

root = Directory(
    name = "/", 
    parent = None, 
    files = [], 
    children = []
)

#%%

all_directories = [root]
for idx, row in enumerate(data): 
    row = row.split(" ")

    # command
    if row[0] == "$": 
        if row[1] == "cd": 

            directory = row[2]
            # go back
            if directory == "..":
                current_dir = current_dir.parent

            # go to root 
            elif directory == "/":
                current_dir = root

            # go to directory
            else: 
                current_dir = [c for c in current_dir.children if c.name == directory][0]
        
        if row[1] == "ls": 
            pass 
    
    # is directory 
    elif row[0] == "dir": 
        new_dir = Directory(
            name = row[1], 
            parent = current_dir, 
            files = [], 
            children = []
        )
        all_directories.append(new_dir)
        current_dir.children.append(new_dir)
           
    # is file
    else:
        current_dir.files.append(
            File(name = row[1], size=int(row[0]))
        )

#%%
# part 1

threshhold = 100000
total_size = 0 

for dir in all_directories: 
    if dir.size <= threshhold: 
        total_size += dir.size 
total_size


#%%
# part 2 

total_space = 70000000
min_space = 30000000

available_space = total_space - root.size
space_to_free = min_space - available_space
space_to_free


# %%

dir_to_delete = root 
for curr_dir in all_directories: 
    # big enough?
    if curr_dir.size >= space_to_free: 
        # smaller than current selection? 
        if curr_dir.size < dir_to_delete.size:
            dir_to_delete = curr_dir 

print(dir_to_delete.name, dir_to_delete.size)

