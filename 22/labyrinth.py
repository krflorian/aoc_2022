#%%

from pathlib import Path


DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

with (DATA_PATH / "input_path.txt").open() as infile:
    path = infile.read()


path
#%%
data

#%%

board = {}
max_row_length = max([len(row) for row in data])
data = [row.ljust(max_row_length) for row in data]

for row_id, row in enumerate(data):
    for col_id, val in enumerate(row):
        if val == " ":
            pass

        if val == ".":
            board[(row_id, col_id)] = {}
            # right
            if (col_id + 1 >= len(row)) or row[col_id + 1] == " ":
                for v_id, v in enumerate(row):
                    if v == " ":
                        pass
                    elif v == "#":
                        break
                    elif v == ".":
                        board[(row_id, col_id)]["right"] = (row_id, v_id)
                        break

            elif data[row_id][col_id + 1] == ".":
                board[(row_id, col_id)]["right"] = (row_id, col_id + 1)

            # left
            if (col_id - 1 >= len(data[row_id])) or data[row_id][col_id - 1] == " ":
                for v_id, v in enumerate(reversed(data[row_id])):
                    if v == " ":
                        pass
                    elif v == "#":
                        break
                    elif v == ".":
                        board[(row_id, col_id)]["left"] = (
                            row_id,
                            len(data[row_id]) - 1 - v_id,
                        )
                        break
            elif data[row_id][col_id - 1] == ".":
                board[(row_id, col_id)]["left"] = (row_id, col_id - 1)

            # down
            if (row_id + 1 >= len(data)) or data[row_id + 1][col_id] == " ":
                for v_id, v in enumerate(data):
                    if v[col_id] == " ":
                        pass
                    elif v[col_id] == "#":
                        break
                    elif v[col_id] == ".":
                        board[(row_id, col_id)]["down"] = (v_id, col_id)
                        break

            elif data[row_id + 1][col_id] == ".":
                board[(row_id, col_id)]["down"] = (row_id + 1, col_id)

            # up
            if (row_id - 1 < 0) or (data[row_id - 1][col_id] == " "):

                for v_id, v in enumerate(reversed(data)):
                    if v[col_id] == " ":
                        pass
                    elif v[col_id] == "#":
                        break
                    elif v[col_id] == ".":
                        board[(row_id, col_id)]["up"] = (len(data) - 1 - v_id, col_id)
                        break

            elif data[row_id - 1][col_id] == ".":
                board[(row_id, col_id)]["up"] = (row_id - 1, col_id)

#%%
# 10R5L5R10L4R5L5
import string
import re

direction_mapper = {
    "R": {"down": "left", "left": "up", "up": "right", "right": "down"},
    "L": {"down": "right", "left": "down", "up": "left", "right": "up"},
}

directions = ["right"]
direction = "right"
for i in path:
    if i in string.ascii_uppercase:
        direction = direction_mapper[i][direction]
        directions.append(direction)

moves = list(map(int, re.split("|".join(string.ascii_uppercase), path)))


#%%

# position = (0, 8)
position = (0, 50)

print(position)

while moves:
    heading = directions.pop(0)
    number_of_moves = moves.pop(0)
    # print(f"heading {heading}: {number_of_moves} tiles")
    for _ in range(number_of_moves):
        if heading in board[position]:
            position = board[position][heading]
            # print(position)
        else:
            break

position

#%%

values = {"right": 0, "down": 1, "left": 2, "up": 3}

solution = values[heading] + (position[0] + 1) * 1000 + (position[1] + 1) * 4
solution

#%%
