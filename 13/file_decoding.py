#%%

from pathlib import Path
import json 

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")   

data = [json.loads(row) for row in data if row != ""]
data

#%%

def check_elements(left, right): 
    
    # both integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            #print("left one smaller - TRUE")
            return True 
        elif right < left: 
            #print("right one smaller - FALSE")
            return False 
        return 

    # both lists 
    elif isinstance(left, list) and isinstance(right, list): 
        for (l, r) in zip(left, right):
            outcome = check_elements(l, r)
            if outcome is not None: 
                return outcome 

        # one ran out 
        if len(left) < len(right):
            #print("left side more elements - TRUE")
            return True 
        elif len(right) < len(left):
            #print("right side more elements - FALSE")
            return False 
        else: 
            return 

    # left is list 
    elif isinstance(left, list) and isinstance(right, int):
        outcome = check_elements(left, [right])
        
        if outcome is not None: 
            return outcome 
    
    # right is list 
    elif isinstance(left, int) and isinstance(right, list):
        outcome = check_elements([left], right)
        if outcome is not None: 
            return outcome 


#%%
# part 1 
right_order = []
for i in range(0, len(data), 2):
    print("next one ", i)
    right_order.append(
        check_elements(data[i], data[i+1])
    )


# %%

right_order_idxs = [idx+1 for idx, check in enumerate(right_order) if check]
sum(right_order_idxs)


#%%
# part 2 
first = sum([check_elements(row , [[2]])for row in data])
second = sum([check_elements(row, [[6]]) for row in data])

print(first +1, second +2)
print((first+1) * (second+2))

