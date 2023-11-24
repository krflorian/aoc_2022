
#%%

from pathlib import Path

DATA_PATH = Path("data/")


with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()


#%%

buffer = []
for idx, character in enumerate(data): 
    buffer.append(character)

    if len(buffer) > 14:
        buffer.pop(0)
        
        if len(set(buffer)) == 14:
            print(idx+1, buffer)
            break 

