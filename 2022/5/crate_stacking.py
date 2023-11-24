#%%
from pathlib import Path
from collections import namedtuple

DATA_PATH = Path("data/")

Operation = namedtuple('Operation', ['move', 'from_', 'to_'])

with (DATA_PATH / "input_operations.txt").open() as infile: 
    operations_data = infile.read()
    operations_data = operations_data.split("\n")

with (DATA_PATH / "input_stacks.txt").open() as infile: 
    stacks_data = infile.read()
    stacks_data = stacks_data.split("\n")


operations = [] 
for row in operations_data: 
    row = row.split(" ")
    operation = Operation(int(row[1]), int(row[3])-1, int(row[5])-1)
    operations.append(operation)

stacks = [] 
for row in stacks_data: 
    stacks.append([crate for crate in row])


#%%
#part 1 

print("_______________")
print("before:")
for stack in stacks:
    print(stack)

for operation in operations:
    for _ in range(operation.move): 
        crate = stacks[operation.from_].pop()
        stacks[operation.to_].append(crate)

print("_______________")
print("after:")
for stack in stacks:
    print(stack)

#%%

''.join([stack[-1] for stack in stacks])


#%%
#part 2 

print("_______________")
print("before:")
for stack in stacks:
    print(stack)

for operation in operations:
    crates = stacks[operation.from_][-operation.move:]
    stacks[operation.from_] = stacks[operation.from_][0:-operation.move]
    stacks[operation.to_] += crates

print("_______________")
print("after:")
for stack in stacks:
    print(stack)

#%%

''.join([stack[-1] for stack in stacks])
