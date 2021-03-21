import math
from operator import add, sub
from functools import reduce
from models import Vector


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
        """Euclidean distance to point"""
        s = sum([(a - b) ** 2 for a, b in zip(self.coords, other.coords)])
        return math.sqrt(s)

    def dist_to_line(self, line):
        """Euclidean distance to the 2D line"""
        return abs(line.A * self.x + line.B * self.y + line.C) / math.sqrt(
            line.A ** 2 + line.B ** 2
        )

    def angle_with(self, point1, point2):
        """Angle point1-self-point2 in [-pi, pi]"""
        v1 = Vector.from_two_points(self, point1)
        v2 = Vector.from_two_points(self, point2)
        v1.normalize()
        v2.normalize()

        return math.acos(v1 * v2 / (v1.euclidean_norm * v2.euclidean_norm))

    def polar_angle_with(self, other):
        """Polar angle between self and other with self as origin"""
        return math.atan2(self.y - other.y, self.x - other.x)

    def __hash__(self):
        return hash(self.coords)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def direction(point1, point2, point3):
        """
        < 0 if point3 is at the left of vector point1->point2;
        > 0 if point3 is at the right of vector point1->point2;
        = 0 if point3 is at the vector point1->point2.
        """
        v1 = Vector.from_two_points(point1, point3)
        v2 = Vector.from_two_points(point1, point2)
        return v1.cross_product_with(v2)

    @staticmethod
    def centroid(point_iter):
        """Coordinate-wise mean of points iterable"""
        return Point(*(sum(coord) / len(coord) for coord in zip(*point_iter)))
