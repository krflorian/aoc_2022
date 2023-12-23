# %%
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

# %%

patterns_as_rows = [[]]
for row in data:
    if row == "":
        patterns_as_rows.append([])
    else:
        patterns_as_rows[-1].append(row)
patterns_as_rows

# %%

patterns_as_cols = []
for pattern in patterns_as_rows:
    patterns_as_cols.append([])
    for idx in range(len(pattern[0])):
        patterns_as_cols[-1].append([])
        for row in pattern:
            patterns_as_cols[-1][-1].append(row[idx])
            print(patterns_as_cols[-1])
        patterns_as_cols[-1][-1] = "".join(patterns_as_cols[-1][-1])
patterns_as_cols


# %%

pattern_2_idx = {}
col_idxs, pattern_idxs = [], []
pattern = patterns_as_cols[0]

for pattern_idx, pattern in enumerate(patterns_as_cols):
    for idx in range(1, len(pattern)):
        offset = 1
        if pattern[idx - offset] == pattern[idx]:
            mirror = True
            offset += 1
            while (idx - offset >= 0) and (idx + offset - 1 < len(pattern)):
                if not pattern[idx - offset] == pattern[idx + offset - 1]:
                    mirror = False
                    break
                offset += 1
            if mirror:
                col_idxs.append(idx)
                pattern_idxs.append(pattern_idx)
                pattern_2_idx[pattern_idx] = {"col": idx}
col_idxs

# %%

row_idxs = []
pattern = patterns_as_cols[0]

for pattern_idx, pattern in enumerate(patterns_as_rows):
    if pattern_idx in pattern_idxs:
        continue
    for idx in range(1, len(pattern)):
        offset = 1
        if pattern[idx - offset] == pattern[idx]:
            mirror = True
            offset += 1
            while (idx - offset >= 0) and (idx + offset - 1 < len(pattern)):
                if not pattern[idx - offset] == pattern[idx + offset - 1]:
                    mirror = False
                    break
                offset += 1
            if mirror:
                row_idxs.append(idx)
                pattern_idxs.append(pattern_idx)
                pattern_2_idx[pattern_idx] = {"row": idx}
row_idxs

# %%

solution = 0
for idx in row_idxs:
    solution += 100 * idx
for idx in col_idxs:
    solution += idx
solution


# %%
# part 2


def check_patterns(row, other_row) -> bool:
    if row == other_row:
        return True, False
    matches = [r == o for (r, o) in zip(row, other_row)]
    if sum(matches) == len(row) - 1:
        return True, True
    return False, False


pattern_idx = 10
pattern = patterns_as_rows[pattern_idx]
pattern


new_pattern_idxs, new_row_idxs = [], []
for pattern_idx, pattern in enumerate(patterns_as_rows):
    old_row_idx = pattern_2_idx[pattern_idx].get("row", None)
    for idx in range(1, len(pattern)):
        if idx == old_row_idx:
            continue
        offset = 1
        has_been_altered = False
        matches, altered = check_patterns(pattern[idx - offset], pattern[idx])
        if altered:
            has_been_altered = True
        if matches:
            mirror = True
            offset += 1
            while (idx - offset >= 0) and (idx + offset - 1 < len(pattern)):
                matches, altered = check_patterns(
                    pattern[idx - offset], pattern[idx + offset - 1]
                )
                if not matches:
                    mirror = False
                    break
                if altered and has_been_altered:
                    mirror = False
                    break
                if altered:
                    has_been_altered = True
                offset += 1
            if mirror:
                new_row_idxs.append(idx)
                new_pattern_idxs.append(pattern_idx)
                break
new_pattern_idxs

# %%

new_col_idxs = []
for pattern_idx, pattern in enumerate(patterns_as_cols):
    old_col_idx = pattern_2_idx[pattern_idx].get("col", None)
    if pattern_idx in new_pattern_idxs:
        continue
    for idx in range(1, len(pattern)):
        if idx == old_col_idx:
            continue
        offset = 1
        has_been_altered = False
        matches, altered = check_patterns(pattern[idx - offset], pattern[idx])
        if altered:
            has_been_altered = True
        if matches:
            mirror = True
            offset += 1
            while (idx - offset >= 0) and (idx + offset - 1 < len(pattern)):
                matches, altered = check_patterns(
                    pattern[idx - offset], pattern[idx + offset - 1]
                )
                if not matches:
                    mirror = False
                    break
                if altered and has_been_altered:
                    mirror = False
                    break
                if altered:
                    has_been_altered = True
                offset += 1
            if mirror:
                new_col_idxs.append(idx)
                new_pattern_idxs.append(pattern_idx)
                break
new_pattern_idxs

# %%


solution = 0
for idx in new_row_idxs:
    solution += 100 * idx
for idx in new_col_idxs:
    solution += idx
solution

# %%

len(patterns_as_cols) == len(new_pattern_idxs)
