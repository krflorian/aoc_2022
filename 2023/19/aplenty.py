# %%

from pathlib import Path
from tqdm import tqdm

with Path("test_data.txt").open() as infile:
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

# %%

boundary_ranges = {"x": [], "m": [], "a": [], "s": []}
for letter, boundary in boundaries.items():
    last_value = 1
    last_operator = None
    for bound in boundary:
        operator = bound[0]
        # if last_operator == "<" and operator == ">":
        #    last_value = bound[1] + 1
        #    pass
        if bound[0] == "<":
            b = range(last_value, bound[1] - 1)
            last_value = bound[1]
            boundary_ranges[letter].append(b)
        elif bound[0] == ">":
            b = range(last_value, bound[1])
            last_value = bound[1] + 1
            boundary_ranges[letter].append(b)
        else:
            print("error")
        last_operator = operator
    b = range(last_value, 4000)
    boundary_ranges[letter].append(b)


# %%

possible_values = {"x": [], "m": [], "a": [], "s": []}
possible_value_lenghts = {"x": [], "m": [], "a": [], "s": []}
for letter, ranges in boundary_ranges.items():
    for r in ranges:
        possible_values[letter].append(r.start)
        possible_value_lenghts[letter].append(r.stop - r.start + 1)

# %%

len(possible_values["x"]) * len(possible_values["m"]) * len(possible_values["a"]) * len(
    possible_values["s"]
)

# %%
# solution


def work_on(workflow, part):
    result = None
    for rule in workflow:
        if len(rule) > 1:
            letter, operator, value, result = rule

            if operations[operator](part[letter], value):
                break
        else:
            result = rule[0]

    if result is None:
        print("error", workflow, part)

    if result == "A":
        return True
    elif result == "R":
        return 0
    else:
        workflow = workflows[result]
        return work_on(workflow, part)


operations = {
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
}

solution = 0
for x in tqdm(possible_values["x"]):
    for m in possible_values["m"]:
        for a in possible_values["a"]:
            for s in possible_values["s"]:
                part = {"x": x, "m": m, "a": a, "s": s}

                workflow_name = "in"
                multiplier = 1
                for val in [
                    possible_value_lenghts[letter][possible_values[letter].index(value)]
                    for letter, value in part.items()
                ]:
                    multiplier *= val

                workflow = workflows[workflow_name]
                num_possible = work_on(workflow, part)
                solution += num_possible * multiplier

solution

# %%


part = {"x": 134, "m": 1, "a": 1, "s": 1}

workflow_name = "in"
num_possible = work_on(workflow, part)
num_possible

# %%
