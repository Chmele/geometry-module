import math
from operator import add, sub
from functools import reduce


class Point:
    def __init__(self, *args):
        self.coords = tuple(map(lambda x: float(x), args))

    def dominating(self, other):
        """True if each self coordinate is bigger than other"""
        return reduce(
            lambda a, b: a and b[0] >= b[1], zip(self.coords, other.coords), True
        )

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    @property
    def dim(self):
        return len(self.coords)

    @property
    def norm(self):
        return math.sqrt(sum(x ** 2 for x in self.coords))

    def __getitem__(self, key):
        return self.coords[key]

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.coords < other.coords

    def __add__(self, other):
        return Point(*list(map(add, self.coords, other.coords)))

    def __sub__(self, other):
        return Point(*list(map(sub, self.coords, other.coords)))

    def dist_to_point(self, other):
        s = sum([(a - b) ** 2 for a, b in zip(self.coords, other.coords)])
        return math.sqrt(s)

    def dist_to_line(self, line):
        return abs(line.A * self.x + line.B * self.y + line.C) / math.sqrt(
            line.A ** 2 + line.B ** 2
        )

    def polar_angle_with(self, other):
        return math.atan2(self.y - other.y, self.x - other.x)

    def dot_product_with(self, other):
        return sum(a * b for a, b in zip(self.coords, other.coords))

    def normalize(self):
        self.coords = tuple(x / self.norm for x in self.coords)

    def angle_with(self, point1, point2):
        """Angle point1 - self - point2 (<= pi)"""
        v1 = point1 - self
        v2 = point2 - self
        v1.normalize()
        v2.normalize()

        return math.acos(v1.dot_product_with(v2) / v1.norm * v2.norm)

    def __hash__(self):
        return hash(self.coords)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def center(point_iter):
        """returns mean of points iterable"""
        return Point(*(sum(coord) / len(coord) for coord in zip(*point_iter)))
