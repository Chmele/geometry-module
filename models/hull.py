from models import Polygon, Point, Vector
from algo.graham import graham
from itertools import cycle, dropwhile, takewhile, chain


class Hull(Polygon):
    def __add__(self, other):
        p1, p2, p3, *rest = self.points
        centroid = Point.centroid((p1, p2, p3))
        if other.contains_point(centroid):
            points = list(self) + list(other)
        else:
            points = list(self) + list(other.get_arc(centroid))
        return list(graham(points))[2]

    def reference_points(self, point):
        v = Vector((0, 1))
        def key (end_point):
            return v.signed_angle(Vector.from_two_points(point, end_point))
        return (min(self, key=key), max(self, key=key))

    def get_arc(self, point):
        point_cycle = cycle(self)
        u, v = self.reference_points(point)
        arc1 = list(chain(takewhile(lambda x: x != v, dropwhile(lambda x: x != u, point_cycle)), (v,)))
        arc2 = list(chain(takewhile(lambda x: x != u, dropwhile(lambda x: x != v, point_cycle)), (u,)))
        def key(arc):
            return Polygon(list(arc)+[point]).area
        return max((arc1, arc2), key=key)