

#%%
from tqdm import tqdm
from pathlib import Path
from functools import partial 
from dataclasses import dataclass, field
from typing import Callable

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")   

data 


#%%


def is_divisible(num, divisor): 
    return num  % divisor == 0

def operation(num, symbol, multiplikator):
    if multiplikator == "old": 
        multiplikator = num 
    if symbol == "+": 
        return num + int(multiplikator)
    elif symbol == "*": 
        return num * int(multiplikator)

@dataclass 
class Monkey(): 
    name: int
    items: list = field(default_factory=list)
    inspected_items: int = 0 
    operation : Callable = operation
    test: Callable = is_divisible
    monkey_true: int = None
    monkey_false: int = None


all_monkeys = []
least_comon_multiple = 1 
idx = 0 

for row in data: 
    if row.startswith("Monkey"):
        monkey = Monkey(name = idx)
        idx += 1

    elif row.startswith("  Starting"):
        for item in row[18:].split(", "):
            monkey.items.append(int(item))

    elif row.startswith("  Operation"):
        row = row.split(" ")
        monkey.operation = partial(
            operation, 
            symbol = row[-2], 
            multiplikator = row[-1]
        )
    
    elif row.startswith("  Test"):
        row = row.split(" ")
        monkey.test = partial(
            is_divisible, 
            divisor = int(row[-1])
        )
        least_comon_multiple *= int(row[-1])

    elif row.startswith("    If true:"):
        row = row.split(" ")
        monkey.monkey_true = int(row[-1])

    elif row.startswith("    If false"):
        row = row.split(" ")
        monkey.monkey_false = int(row[-1])

    else: 
        all_monkeys.append(monkey) 
all_monkeys.append(monkey) 


#all_monkeys[0]  

#%%

#all_monkeys[-2]

#%%

ROUNDS = 10000

for _ in tqdm(range(ROUNDS)):

    #print([(monkey.name, monkey.inspected_items) for monkey in all_monkeys])
    for monkey in all_monkeys:
        while monkey.items: 
            monkey.inspected_items += 1 
            item = monkey.items.pop(0)
            item = monkey.operation(item)
            #item = item // 3 

            #print("item worry level", item)
            test_postive =  monkey.test(item)
            if item > least_comon_multiple: 
                reminder = item % least_comon_multiple 
                item = least_comon_multiple + reminder 

            if test_postive:
                #print("monkey test True - throwing to monkey", monkey.monkey_true)
                all_monkeys[monkey.monkey_true].items.append(item)
            else: 
                #print("monkey test False - throwing to monkey", monkey.monkey_false)
                all_monkeys[monkey.monkey_false].items.append(item)


#%%

inspections = [monkey.inspected_items for monkey in all_monkeys]
inspections
# %%

max_inspections = sorted(inspections)
monkey_business = max_inspections[-1] * max_inspections[-2]
monkey_business

# %%


