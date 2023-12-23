# %%
class Map2D:
    def __init__(self, data: list[list[str]]):
        self.max_x = len(data[0]) - 1
        self.max_y = len(data) - 1
        self.data = data

        self.values = []
        for idx in range(len(data[0])):
            self.values.append([])
            for row in reversed(data):
                self.values[-1].append(row[idx])

    def __repr__(self):
        data = []
        for y in range(self.max_y + 1):
            data.append("".join([self.values[x][y] for x in range(self.max_x + 1)]))
        return "\n".join(reversed(data))

    def __call__(self, coordinate: tuple[int, int]):
        self.is_out_of_bounds(coordinate)
        return self.values[coordinate[0]][coordinate[1]]

    def __iter__(self):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                yield self((x, y)), x, y

    def set_value(self, coordinate: tuple[int, int], value: str):
        self.is_out_of_bounds(coordinate)
        self.values[coordinate[0]][coordinate[1]] = value

    def left(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[0] <= 0:
            return None, None
        new_coordinate = (coordinate[0] - 1, coordinate[1])
        return self(new_coordinate), new_coordinate

    def right(self, coordinate: tuple[int, int]) -> str:
        self.is_out_of_bounds(coordinate)
        if coordinate[0] >= self.max_x:
            return None, None
        new_coordinate = (coordinate[0] + 1, coordinate[1])
        return self(new_coordinate), new_coordinate

    def up(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[1] >= self.max_y:
            return None, None
        new_coordinate = (coordinate[0], coordinate[1] + 1)

        return self(new_coordinate), new_coordinate

    def down(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[1] <= 0:
            return None, None
        new_coordinate = (coordinate[0], coordinate[1] - 1)

        return self(new_coordinate), new_coordinate

    def up_left(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[1] >= self.max_y or coordinate[0] <= 0:
            return None
        new_coordinate = (coordinate[0] + 1, coordinate[1] - 1)

        return self(new_coordinate)

    def up_right(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[1] >= self.max_y or coordinate[0] >= self.max_x:
            return None
        new_coordinate = (coordinate[0] + 1, coordinate[1] + 1)

        return self(new_coordinate)

    def down_left(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[1] <= 0 or coordinate[0] <= 0:
            return None
        new_coordinate = (coordinate[0] - 1, coordinate[1] - 1)

        return self(new_coordinate)

    def down_right(self, coordinate: tuple[int, int]) -> tuple[str, tuple[int, int]]:
        self.is_out_of_bounds(coordinate)
        if coordinate[1] <= 0 or coordinate[0] >= self.max_x:
            return None
        new_coordinate = (coordinate[0] - 1, coordinate[1] + 1)

        return self(new_coordinate)

    def is_out_of_bounds(self, coordinate: tuple[int, int]) -> bool:
        if (
            (coordinate[0] > self.max_x)
            or (coordinate[0] < 0)
            or (coordinate[1] > self.max_y)
            or (coordinate[1] < 0)
        ):
            raise ValueError(f"Coordinate {coordinate} is out of bounds!")
