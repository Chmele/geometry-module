import math


class Vector:
    def __init__(self, coords):
        """Make vector from coords iterable."""
        self.coords = coords

    def __len__(self):
        """Dimension of vector instance."""
        return len(self.coords)

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
    def euclidean_norm(self):
        return math.sqrt(sum((i ** 2 for i in self.coords)))

    def __mul__(self, other):
        """Scalar vector multiplication."""
        return sum((i * j for i, j in zip(self.coords, other.coords)))

    def __getitem__(self, key):
        return self.coords[key]

    def angle(self, other):
        if len(self) == len(other):
            return math.acos(
                (self * other) / (self.euclidean_norm * other.euclidean_norm)
            )

    def signed_angle(self, other):
        def abs_vect_mul_2d(v1, v2):
            return v1[0] * v2[1] - v1[1] * v2[0]

        return math.asin(
            abs_vect_mul_2d(self, other)
            / (self.euclidean_norm * other.euclidean_norm)
        )

    @staticmethod
    def from_two_points(p1, p2):
        return Vector((p2 - p1).coords)

    def normalize(self):
        self.coords = tuple(x / self.euclidean_norm for x in self.coords)

    def cross_product_with(self, other):
        return self.x * other.y - other.x * self.y
