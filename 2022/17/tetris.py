#%%
from pathlib import Path
from collections import namedtuple

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile:
    data = infile.read()
    data = [direction for direction in data]


#%%

Coordinate = namedtuple("Coordinate", ["x", "y"])

square = [Coordinate(3, 1), Coordinate(4, 1), Coordinate(3, 2), Coordinate(4, 2)]
cross = [
    Coordinate(4, 1),
    Coordinate(3, 2),
    Coordinate(4, 2),
    Coordinate(5, 2),
    Coordinate(4, 3),
]
l_shape = [
    Coordinate(3, 1),
    Coordinate(4, 1),
    Coordinate(5, 1),
    Coordinate(5, 2),
    Coordinate(5, 3),
]
long = [Coordinate(3, 1), Coordinate(3, 2), Coordinate(3, 3), Coordinate(3, 4)]
broad = [Coordinate(3, 1), Coordinate(4, 1), Coordinate(5, 1), Coordinate(6, 1)]

#%%


def move_right(object: list[Coordinate], tower):
    new_object = []
    for point in object:
        shifted_point = Coordinate(x=point.x + 1, y=point.y)
        if (shifted_point.x <= 7) and (shifted_point not in tower):
            new_object.append(shifted_point)
        else:
            return object
    return new_object


def move_left(object: list[Coordinate], tower):
    new_object = []
    for point in object:
        shifted_point = Coordinate(x=point.x - 1, y=point.y)
        if (shifted_point.x >= 1) and (shifted_point not in tower):
            new_object.append(shifted_point)
        else:
            return object
    return new_object


def move_down(object: list[Coordinate], tower: list[Coordinate]):
    new_object = []
    for point in object:
        shifted_point = Coordinate(x=point.x, y=point.y - 1)
        if (shifted_point.y >= 1) and (shifted_point not in tower):
            new_object.append(shifted_point)
        else:
            return object, False
    return new_object, True


def move_to_starting_row(object, starting_idx):
    new_object = []
    for point in object:
        shifted_point = Coordinate(x=point.x, y=point.y + starting_idx)
        new_object.append(shifted_point)
    return new_object


"""
import matplotlib.pyplot as plt


def plot(object):
    x = [point.x for point in object]
    y = [point.y for point in object]

    plt.xlim(1, 7)
    plt.ylim(1, max(y) + 1)

    plt.plot(x, y, "ro")
    plt.show()
"""

#%%
object_names = ["broad", "cross", "l_shape", "long", "square"]
objects = [broad, cross, l_shape, long, square]

move_to = {"<": move_left, ">": move_right}
tower = []

highest_y = 0
stopped_objects = 0
object = objects.pop(0)
objects.append(object)
object_name = object_names.pop(0)
object_names.append(object_name)

cycle_objects = []

states = []  # rock, starting jet, last_two rocks
last_n_objects = []
found_circles = {}
heights = []
n = 20

object = move_to_starting_row(object, 3)

#%%
# print(object)
print("starting tetris ")
# plot(tower + object)

# for _ in range(100):
while True:

    direction = data.pop(0)
    data.append(direction)
    object = move_to[direction](object, tower)
    # plot(tower + object)
    object, did_move = move_down(object, tower)
    # plot(tower + object)

    if did_move:
        pass
    else:
        for point in object:
            if point.y > highest_y:
                highest_y = point.y
            tower.append(point)

        tower = tower[-1000:]
        stopped_objects += 1
        # plot(object + tower)
        if stopped_objects == 10000:
            print("tower is full! ")
            break

        if stopped_objects % 1000 == 0:
            print(
                f"stopped_objects: {stopped_objects} / 1000000000000 - {stopped_objects / 1000000000000*100:.2f}%"
            )

        # next object
        object = objects.pop(0)
        objects.append(object)

        # set state
        object_name = object_names.pop(0)
        object_names.append(object_name)

        y_positions = []
        for i in range(n):
            y_positions.extend([(i, pos.x) for pos in tower if pos.y == highest_y - i])
        next_n_moves = tuple(data[:n])

        new_state = (object_name, data[0], tuple(y_positions))

        # print(new_state)
        states.append(new_state)
        heights.append(highest_y)
        cycle_objects.append(stopped_objects)
        if new_state in found_circles:
            found_circles[new_state] += 1
            if found_circles[new_state] > 1:
                break
        else:
            found_circles[new_state] = 0

        object = move_to_starting_row(object, highest_y + 3)

#%%

cycle_heights = [height for height, state in zip(heights, states) if state == new_state]
cycle_objects = [n for n, state in zip(cycle_objects, states) if state == new_state]

for idx, h in enumerate(cycle_heights[1:]):
    print(h - cycle_heights[idx])

cycle_height = h - cycle_heights[idx]

#%%

for idx, h in enumerate(cycle_objects[1:]):
    print(h - cycle_objects[idx])
n_objects_per_cycle = h - cycle_objects[idx]


#%%

max_stopped_objects = 1000000000000
missing_objects = (max_stopped_objects - stopped_objects) % n_objects_per_cycle
missing_n_cycles = (max_stopped_objects - stopped_objects) // n_objects_per_cycle
_highest_y_last = highest_y
_highest_y = missing_n_cycles * cycle_height + highest_y

object = move_to_starting_row(object, _highest_y_last + 3)
stopped_objects = 0
missing_objects
#%%

while True:

    direction = data.pop(0)
    data.append(direction)
    object = move_to[direction](object, tower)
    # plot(tower + object)
    object, did_move = move_down(object, tower)
    # plot(tower + object)

    if did_move:
        pass
    else:
        for point in object:
            if point.y > highest_y:
                highest_y = point.y
            tower.append(point)

        tower = tower[-1000:]
        stopped_objects += 1
        # plot(object + tower)
        if stopped_objects == missing_objects:
            print("tower is full! ")
            break

        if stopped_objects % 1000 == 0:
            print(
                f"stopped_objects: {stopped_objects} / 1000000000000 - {stopped_objects / 1000000000000*100:.2f}%"
            )

        # next object
        object = objects.pop(0)
        objects.append(object)

        object = move_to_starting_row(object, highest_y + 3)


#%%

highest_y - _highest_y_last + _highest_y
