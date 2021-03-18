import math


class Vector:
    def __init__(self, coords):
        self.coords = coords

    def __len__(self):
        return len(self.coords)

    @property
    def euclidean_module(self):
        return math.sqrt(sum((i ** 2 for i in self.coords)))

    def __mul__(self, other):
        return sum((i * j for i, j in zip(self.coords, other.coords)))

    def __getitem__(self, key):
        return self.coords[key]

    def angle(self, other):
        if len(self) == len(other):
            return math.acos(
                (self * other) / (self.euclidean_module * other.euclidean_module)
            )

    def signed_angle(self, other):
        def abs_vect_mul_2d(v1, v2):
            return v1[0] * v2[1] - v1[1] * v2[0]

        return math.asin(
            abs_vect_mul_2d(self, other)
            / (self.euclidean_module * other.euclidean_module)
        )

    @staticmethod
    def from_two_points(p1, p2):
        return Vector((p1 - p2).coords)
