import math
from operator import itemgetter
from models import Point


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = (p1, p2, p3)

    @property
    def a(self):
        return self.points[0]

    @property
    def b(self):
        return self.points[1]

    @property
    def c(self):
        return self.points[2]

    @property
    def sides(self):
        ig = itemgetter(2, 3, 1)
        return (
            p1.dist_to_point(p2)
            for p1, p2 in zip(self.points, ig(self.points))
        )

    @property
    def area(self):
        """Heron`s formula."""
        p = sum(self.sides) / 2
        ab, bc, ca = self.sides
        return math.sqrt(p * (p - ab) * (p - bc) * (p - ca))

    def point_belonging(self, p: Point):
        """
        Check if given point belongs to triangle
        :param p: point to check
        :return: True if belongs, False otherwise
        """
        a = (self.a.x - p.x) * (self.b.y - self.a.y) - (self.b.x - self.a.x) * (self.a.y - p.y)
        b = (self.b.x - p.x) * (self.c.y - self.b.y) - (self.c.x - self.b.x) * (self.b.y - p.y)
        c = (self.c.x - p.x) * (self.a.y - self.c.y) - (self.a.x - self.c.x) * (self.c.y - p.y)
        return ((a >= 0) and (b >= 0) and (c >= 0)) or ((a <= 0) and (b <= 0) and (c <= 0))

    def __eq__(self, other):
        return set(self.points) == set(other.points)

    def __hash__(self):
        return hash(self.points)

    def __str__(self):
        return str(self.points)
