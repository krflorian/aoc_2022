# %%
import re
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")


# %%

char_2_numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
pattern = "(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))"
numbers = []
for row in data:
    row_numbers = re.findall(pattern, row)
    row_numbers = [char_2_numbers.get(num, num) for num in row_numbers]
    print(row_numbers)
    numbers.append(row_numbers)

numbers

# %%
pattern = "(?=(eight|two|four))"
pattern = "(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))"
text = "cheightwofourxt2"

row_numbers = re.findall(pattern, text)
row_numbers


# %%
solution_values = []
solution = 0
for row in numbers:
    print(int(row[0] + row[-1]))
    solution_values.append(int(row[0] + row[-1]))
    solution += int(row[0] + row[-1])

solution
