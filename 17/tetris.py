#%%
from pathlib import Path
from collections import namedtuple

DATA_PATH = Path("17/data/")

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


import matplotlib.pyplot as plt


def plot(object):
    x = [point.x for point in object]
    y = [point.y for point in object]

    plt.xlim(1, 7)
    plt.ylim(1, max(y) + 1)

    plt.plot(x, y, "ro")
    plt.show()


#%%
objects = [broad, cross, l_shape, long, square]

move_to = {"<": move_left, ">": move_right}
tower = []

highest_y = 0
stopped_objects = 0
object = objects.pop(0)
objects.append(object)

object = move_to_starting_row(object, 3)

#%%
# print(object)
print("starting tetris ")
plot(tower + object)

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
        tower = tower[-100:]
        stopped_objects += 1
        # plot(object + tower)
        if stopped_objects == 10000:
            print("tower is full! ")
            break

        if stopped_objects % 1000 == 0:
            print(
                f"stopped_objects: {stopped_objects} / 1000000000000 - {stopped_objects / 1000000000000*100:.2f}%"
            )
        object = objects.pop(0)
        objects.append(object)

        object = move_to_starting_row(object, highest_y + 3)

#%%

plot(tower)
print("solution: ", highest_y)

#%%

tower
