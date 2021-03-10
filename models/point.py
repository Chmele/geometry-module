import math
from operator import add, sub

class Point:

    def __init__(self, *args):
        self.coords = tuple(map(lambda x: float(x), args))

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

    def dist_to(self, other):
        s = sum([(a - b) ** 2 for a, b in zip(self.coords, other.coords)])
        return math.sqrt(s)
    
    def polar_angle_with(self, other):
        return math.atan2(self.y - other.y, self.x - other.x)
