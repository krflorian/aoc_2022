# %%
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")
data

# %%


def is_valid_position(hotsprings, start_idx, length):
    end_idx = start_idx + length - 1
    max_idx = len(hotsprings) - 1

    if any([val == "." for val in hotsprings[start_idx : start_idx + length]]):
        return False
    elif end_idx > max_idx:
        return False
    elif start_idx == 0 and hotsprings[end_idx + 1] != "#":
        return True
    elif end_idx == max_idx and hotsprings[start_idx - 1] != "#":
        return True
    elif hotsprings[start_idx - 1] != "#" and hotsprings[end_idx + 1] != "#":
        return True
    return False


# %%
# sequence = [1, 1, 3]
# hotsprings = "???.???"

import re

pattern = "#+"

queue = []
idx_2_sequence = {}
for idx, row in enumerate(data[:1]):
    # row = data[idx]
    hotsprings, sequence = row.split()
    sequence = list(map(int, sequence.split(",")))
    queue.append((idx, -1, hotsprings, sequence))
    idx_2_sequence[idx] = sequence

queue

# %%

valid_hotsprings = []
while queue:
    original_idx, last_idx, hotsprings, sequence = queue.pop(0)
    possible_locations = [
        idx
        for idx in range(len(hotsprings))
        if hotsprings[idx] != "." and idx > last_idx
    ]
    for idx in possible_locations:
        if is_valid_position(hotsprings, idx, sequence[0]):
            new_hotsprings = (
                hotsprings[:idx] + "#" * sequence[0] + hotsprings[idx + sequence[0] :]
            )
            if len(sequence) == 1:
                original_sequence = idx_2_sequence[original_idx]
                matches = re.findall(pattern, hotsprings)
                if len(matches) == len(sequence):
                    if all(
                        [len(match) == seq for match, seq in zip(matches, sequence)]
                    ):
                        valid_hotsprings.append((original_idx, new_hotsprings))
            elif sum(sequence) + len(sequence[1:]) > len(hotsprings) - idx:
                break
            else:
                queue.append((original_idx, idx, new_hotsprings, sequence[1:]))
        else:
            print("discarding", idx, hotsprings, sequence)

print("solution ", len(valid_hotsprings))


# %%
import re

pattern = "#+"

idx, hotsprings = valid_hotsprings[0]
sequence = idx_2_sequence[idx]
matches = re.findall(pattern, hotsprings)
if len(matches) == len(sequence):
    if all([len(match) == seq for match, seq in zip(matches, sequence)]):
        print(hotsprings, sequence)


# %%

is_valid_position(".?#..?#...?##.", 10, 3)

# %%


hotsprings = "???.???"
sequence = [3]
idx = 0


new_hotsprings = hotsprings[:idx] + "." * sequence[0] + hotsprings[idx + sequence[0] :]

new_hotsprings

# %%

new_hotsprings = hotsprings[:idx] + "." * sequence[0] + hotsprings[idx + sequence[0] :]
new_hotsprings

# %%

sequence = [1, 1, 3]

seq = []
for num in sequence:
    seq.append("." + "#" * num + ".")
seq
