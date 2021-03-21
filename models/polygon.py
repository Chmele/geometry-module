from models import Point, Vector, Triangle
from functools import reduce
import math


class Polygon:
    def __init__(self, points):
        self.points = points

    @property
    def point_pairs(self):
        def cyclic_offset(li, n):
            return li[-n:] + li[:-n]

        return zip(self.points, cyclic_offset(self.points, 1))

    def contains_point(self, point):
        pairs = self.point_pairs

        def angle(center, p1, p2):
            v1 = Vector.from_two_points(p1, center)
            v2 = Vector.from_two_points(p2, center)
            return v1.signed_angle(v2)

        total_angle = reduce(
            lambda accum, a: accum + angle(point, a[0], a[1]), pairs, 0
        )
        return total_angle > math.pi

    @property
    def surface(self):
        a, b, c, *rest = self.points
        p = Point.center((a, b, c))
        pairs = self.point_pairs

        def accumulate_triangle_surface(sum, pair):
            return sum + Triangle(p, pair[0], pair[1]).surface

        return reduce(accumulate_triangle_surface, pairs, 0)
