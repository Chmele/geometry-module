import math
from models import Point


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = (p1, p2, p3)

    @property
    def p1(self):
        return self.points[0]

    @property
    def p2(self):
        return self.points[1]

    @property
    def p3(self):
        return self.points[2]

    @property
    def sides(self):
        return (
            p1.dist_to_point(p2)
            for p1, p2 in zip((self.C, self.A, self.B), (self.B, self.C, self.A))
        )

    @property
    def area(self):
        """Heron`s formula."""
        p = sum(self.sides) / 2
        A, B, C = self.sides
        return math.sqrt(p * (p - A) * (p - B) * (p - C))

    def point_belonging(self, p: Point):
        """
        Check if given point belongs to triangle
        :param p: point to check
        :return: True if belongs, False otherwise
        """
        a = (self.p1.x - p.x) * (self.p2.y - self.p1.y) - (self.p2.x - self.p1.x) * (self.p1.y - p.y)
        b = (self.p2.x - p.x) * (self.p3.y - self.p2.y) - (self.p3.x - self.p2.x) * (self.p2.y - p.y)
        c = (self.p3.x - p.x) * (self.p1.y - self.p3.y) - (self.p1.x - self.p3.x) * (self.p3.y - p.y)
        return ((a >= 0) and (b >= 0) and (c >= 0)) or ((a <= 0) and (b <= 0) and (c <= 0))

    def __eq__(self, other):
        return set(self.points) == set(other.points)

    def __hash__(self):
        return hash(self.points)

    def __str__(self):
        return str(self.points)
