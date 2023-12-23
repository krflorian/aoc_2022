# %%

from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split(",")
data

# %%


def hash_algo(sequence):
    value = 0
    for char in sequence:
        value += ord(char)
        value = value * 17
        value = value % 256
    return value


# %%
# part 1
solution = 0
for sequence in data:
    value = hash_algo(sequence)
    # print(sequence, value)
    solution += value
solution
# %%
# part 2


boxes = []
for _ in range(256):
    boxes.append({})

for operation in data:
    if "-" in operation:
        sequence, _ = operation.split("-")
        box_id = hash_algo(sequence)
        if sequence in boxes[box_id]:
            boxes[box_id].pop(sequence)
    elif "=" in operation:
        sequence, number = operation.split("=")
        box_id = hash_algo(sequence)
        boxes[box_id][sequence] = number

boxes

# %%

solution = 0

for box_id, box in enumerate(boxes):
    box_value = box_id + 1
    for idx, (key, value) in enumerate(box.items()):
        solution += box_value * (idx + 1) * int(value)
solution

# %%
