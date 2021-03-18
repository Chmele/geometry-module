from models import Point, Vector
from functools import reduce
import math


class Polygon:
    def __init__(self, points):
        self.points = points

    def contains_point(self, point):
        def cyclic_offset(li, n):
            return li[-n:] + li[:-n]

        pairs = zip(self.points, cyclic_offset(self.points, 1))
        def angle(center, p1, p2):
            v1 = Vector.from_two_points(p1, center)
            v2 = Vector.from_two_points(p2, center)
            return v1.angle(v2)
        total_angle = reduce(lambda accum, a: accum+angle(point, a[0], a[1]), pairs, 0)
        return total_angle > math.pi / 2