#%%
from pathlib import Path


DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
    data = [row.split(": ") for row in data]


#%%

monkeys = {}
for row in data:
    monkeys[row[0]] = {}
    if len(row[1]) > 4:
        monkey_1, operation, monkey_2 = row[1].split(" ")
        monkeys[row[0]]["type"] = "calculating"
        monkeys[row[0]]["operation"] = operation
        monkeys[row[0]]["monkey_1"] = monkey_1
        monkeys[row[0]]["monkey_2"] = monkey_2
    else:
        monkeys[row[0]]["type"] = "shouting"
        monkeys[row[0]]["number"] = int(row[1])


#%%


def add(num, other):
    return num + other


def multiply(num, other):
    return num * other


def divide(num, other):
    return num / other


def subtract(num, other):
    return num - other


def match(num, other):
    return num == other


OPERATION_MAPPER = {"+": add, "*": multiply, "/": divide, "-": subtract, "=": match}


def calculate_monkey(monkey):

    if monkey["type"] == "shouting":
        return monkey["number"]
    if monkey["type"] == "calculating":
        return OPERATION_MAPPER[monkey["operation"]](
            calculate_monkey(monkeys[monkey["monkey_1"]]),
            calculate_monkey(monkeys[monkey["monkey_2"]]),
        )


#%%
"""
y = difference(right side, left side)
y = kx + d

y-d = kx 
(y-d) / k = x 
(0-d) / k = x 

"""

from sklearn.linear_model import LinearRegression
import numpy as np

model = LinearRegression()
X = np.linspace(1, 10e12, 101).reshape((-1, 1))


monkey_2 = 49624267175787.0

y = []
for x in X:

    monkeys["humn"]["number"] = x
    y.append(calculate_monkey(monkeys["pdzb"]) - monkey_2)

y = np.array(y)


model.fit(X, y)

x = -model.intercept_ / model.coef_
x


#%%

monkeys["humn"]["number"] = 3360561285172

monkey_1 = calculate_monkey(monkeys["pdzb"])

print(monkey_1 == monkey_2)
