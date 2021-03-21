import math


class Triangle:
    def __init__(self, A, B, C):
        self.A, self.B, self.C = A, B, C

    @property
    def sides(self):
        return (
            p1.dist_to_point(p2)
            for p1, p2 in zip((self.C, self.A, self.B), (self.B, self.C, self.A))
        )

    @property
    def area(self):
        """Heron`s formula"""
        p = sum(self.sides) / 2
        A, B, C = self.sides
        return math.sqrt(p * (p - A) * (p - B) * (p - C))
