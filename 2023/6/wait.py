# %%
from pathlib import Path

with Path("data.txt").open() as infile:
    data = infile.read()
    data = data.split("\n")

times = list(map(int, data[0].split()[1:]))
distances = list(map(int, data[1].split()[1:]))
distances

# %%

time = 7
goal_distance = 9

counts = []
for time, goal_distance in zip(times, distances):
    count = 0
    for speed in range(1, time):
        remaining_time = time - speed
        final_distance = remaining_time * speed
        if final_distance > goal_distance:
            count += 1
    counts.append(count)

solution = 1
for count in counts:
    solution *= count
solution

# %%
# part 2
time = int("".join(data[0].split()[1:]))
goal_distance = int("".join(data[1].split()[1:]))


count = 0
for speed in range(1, time):
    remaining_time = time - speed
    final_distance = remaining_time * speed
    if final_distance > goal_distance:
        count += 1

count
