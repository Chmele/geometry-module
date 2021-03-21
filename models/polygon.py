from models import Point, Vector, Triangle
from functools import reduce
import math


class Polygon:
    def __init__(self, points):
        self.points = points

<<<<<<< HEAD
    def __getitem__(self, key):
        return self.points[key]

    @property
    def point_pairs(self):
=======
    @property
    def point_pairs(self):
        def cyclic_offset(li, n):
            return li[-n:] + li[:-n]

        return zip(self.points, cyclic_offset(self.points, 1))

    def contains_point(self, point):
        pairs = self.point_pairs
    def contains_point(self, point):
>>>>>>> main
        def cyclic_offset(li, n):
            return li[-n:] + li[:-n]

        return zip(self.points, cyclic_offset(self.points, 1))

    def contains_point(self, point):
        pairs = self.point_pairs

        def angle(center, p1, p2):
            v1 = Vector.from_two_points(center, p1)
            v2 = Vector.from_two_points(center, p2)
            return v1.signed_angle(v2)

        total_angle = reduce(
            lambda accum, a: accum + angle(point, a[0], a[1]), pairs, 0
        )
        return total_angle > math.pi

    @property
    def area(self):
        a, b, c, *rest = self.points
        p = Point.centroid((a, b, c))
        pairs = self.point_pairs

        def accumulate_triangle_area(sum, pair):
            return sum + Triangle(p, pair[0], pair[1]).area

        return reduce(accumulate_triangle_area, pairs, 0)
