import math


class Pos:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def north(self):
        return Pos(self.x, self.y - 1)

    @property
    def south(self):
        return Pos(self.x, self.y + 1)

    @property
    def west(self):
        return Pos(self.x - 1, self.y)

    @property
    def east(self):
        return Pos(self.x + 1, self.y)

    @property
    def neighbours(self):
        return [self.north, self.south, self.west, self.east]

    def __eq__(self, other):
        if type(other) is tuple:
            return self._x == other[0] and self._y == other[1]
        else:
            return self._x == other.x and self._y == other.y

    def __hash__(self):
        return hash((self._x, self._y))

    def euclidean_dist_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __lt__(self, other):
        return self.x < other.x

    def __repr__(self):
        return f"<Pos x:{self.x}, y:{self.y}>"

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"
