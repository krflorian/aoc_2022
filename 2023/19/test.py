# %%

from pathlib import Path
from tqdm import tqdm

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")


# %%
import json
import re

workflows = {}
for idx, row in enumerate(data):
    if row == "":
        break
    row = re.split("{|}", row)
    workflow_name = row[0]
    workflow = row[1]
    workflow = workflow.split(",")
    rules = [rule.split(":") for rule in workflow]
    workflows[workflow_name] = []
    for rule in rules:
        if len(rule) > 1:
            letter = rule[0][0]
            operator = rule[0][1]
            value = int(rule[0][2:])
            result = rule[1]
            workflows[workflow_name].append((letter, operator, value, result))
        else:
            workflows[workflow_name].append(rule)


parts = []
for row in data[idx + 1 :]:
    pairs = re.findall(r"(\w+)=(\d+)", row)
    parts.append({key: int(value) for key, value in pairs})
parts


# %%

boundaries = {"x": [], "m": [], "a": [], "s": []}
for workflow in workflows.values():
    for rule in workflow:
        if len(rule) > 1:
            letter, operator, value, result = rule
            boundaries[letter].append((operator, value))
boundaries = {
    letter: sorted(list(set(value)), key=lambda x: x[1])
    for letter, value in boundaries.items()
}

print(len(boundaries["x"]))

# %%
