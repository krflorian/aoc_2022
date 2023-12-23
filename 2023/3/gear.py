# %%
import re
from pathlib import Path

with Path("test_data.txt").open() as infile:
    data = infile.read()
    schema = data.split("\n")

# %%

not_symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

number_coordinates = [[]]
for row_idx, row in enumerate(schema):
    if len(number_coordinates[-1]) > 0:
        number_coordinates.append([])
    for col_index in range(len(row)):
        if row[col_index] in numbers:
            number_coordinates[-1].append((row_idx, col_index))
        elif row[col_index] not in numbers:
            if len(number_coordinates[-1]) > 0:
                number_coordinates.append([])


# %%
# part 1
part_numbers = []

for number in number_coordinates:
    for coordinate in number:
        # left
        if (
            coordinate[1] > 0
            and schema[coordinate[0]][coordinate[1] - 1] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # right
        elif (
            coordinate[1] < len(schema[0]) - 1
            and schema[coordinate[0]][coordinate[1] + 1] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # down
        elif (
            coordinate[0] < len(schema) - 1
            and schema[coordinate[0] + 1][coordinate[1]] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # up
        elif (
            coordinate[0] > 0
            and schema[coordinate[0] - 1][coordinate[1]] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # upper left
        elif (
            coordinate[1] > 0
            and coordinate[0] > 0
            and schema[coordinate[0] - 1][coordinate[1] - 1] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # upper right
        elif (
            coordinate[0] > 0
            and coordinate[1] < len(schema[0]) - 1
            and schema[coordinate[0] - 1][coordinate[1] + 1] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # lower left
        elif (
            coordinate[1] > 0
            and coordinate[0] < len(schema) - 1
            and schema[coordinate[0] + 1][coordinate[1] - 1] not in not_symbols
        ):
            part_numbers.append(number)
            break
        # lower right
        elif (
            coordinate[1] < len(schema[0]) - 1
            and coordinate[0] < len(schema) - 1
            and schema[coordinate[0] + 1][coordinate[1] + 1] not in not_symbols
        ):
            part_numbers.append(number)
            break


# %%
for coordinates in part_numbers:
    for coor in coordinates:
        print(schema[coor[0]][coor[1]])
    print("___________")

# %%

part_sum = 0
part_numbers_numbers = []
for coordinates in part_numbers:
    num = ""
    for coor in coordinates:
        num += str(schema[coor[0]][coor[1]])
    part_numbers_numbers.append(int(num))
    part_sum += int(num)
part_sum

# %%
# part 2
part_numbers = []

for number in number_coordinates:
    for coordinate in number:
        # left
        if coordinate[1] > 0 and schema[coordinate[0]][coordinate[1] - 1] == "*":
            gear = (coordinate[0], coordinate[1] - 1)
            part_numbers.append((number, gear))
            break
        # right
        elif (
            coordinate[1] < len(schema[0]) - 1
            and schema[coordinate[0]][coordinate[1] + 1] == "*"
        ):
            gear = (coordinate[0], coordinate[1] + 1)
            part_numbers.append((number, gear))
            break
        # down
        elif (
            coordinate[0] < len(schema) - 1
            and schema[coordinate[0] + 1][coordinate[1]] == "*"
        ):
            gear = (coordinate[0] + 1, coordinate[1])
            part_numbers.append((number, gear))
            break
        # up
        elif coordinate[0] > 0 and schema[coordinate[0] - 1][coordinate[1]] == "*":
            gear = (coordinate[0] - 1, coordinate[1])
            part_numbers.append((number, gear))
            break
        # upper left
        elif (
            coordinate[1] > 0
            and coordinate[0] > 0
            and schema[coordinate[0] - 1][coordinate[1] - 1] == "*"
        ):
            gear = (coordinate[0] - 1, coordinate[1] - 1)
            part_numbers.append((number, gear))
            break
        # upper right
        elif (
            coordinate[0] > 0
            and coordinate[1] < len(schema[0]) - 1
            and schema[coordinate[0] - 1][coordinate[1] + 1] == "*"
        ):
            gear = (coordinate[0] - 1, coordinate[1] + 1)
            part_numbers.append((number, gear))

            break
        # lower left
        elif (
            coordinate[1] > 0
            and coordinate[0] < len(schema) - 1
            and schema[coordinate[0] + 1][coordinate[1] - 1] == "*"
        ):
            gear = (coordinate[0] + 1, coordinate[1] - 1)
            part_numbers.append((number, gear))

            break
        # lower right
        elif (
            coordinate[1] < len(schema[0]) - 1
            and coordinate[0] < len(schema) - 1
            and schema[coordinate[0] + 1][coordinate[1] + 1] == "*"
        ):
            gear = (coordinate[0] + 1, coordinate[1] + 1)
            part_numbers.append((number, gear))
            break


# %%

gear_numbers = 0
gear_coordinates = []
for idx, (coordinates, gear) in enumerate(part_numbers):
    for other_idx, (other_coordinates, other_gear) in enumerate(part_numbers):
        if idx == other_idx:
            continue
        if gear == other_gear and coordinates not in gear_coordinates:
            gear_coordinates.append(coordinates)
            gear_coordinates.append(other_coordinates)
            num = ""
            for coor in coordinates:
                num += str(schema[coor[0]][coor[1]])
            other_num = ""
            for coor in other_coordinates:
                other_num += str(schema[coor[0]][coor[1]])
            print(num, "*", other_num)
            gear_numbers += int(num) * int(other_num)
gear_numbers
