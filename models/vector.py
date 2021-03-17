import math


class Vector:
    def __init__(self, coords):
        self.coords = coords
    
    def __len__(self):
        return len(self.coords)

    @property
    def euclidean_module(self):
        return math.sqrt(sum((i**2 for i in self.coords)))

    def __mul__(self, other):
        return sum((i * j for i, j in zip(self.coords, other.coords)))

    def angle(self, other):
        if len(self) == len(other):
            return math.acos((self*other)/(self.euclidean_module*other.euclidean_module))
            
    @classmethod
    def from_two_points( p1, p2):
        return Vector((p1 - p2).coords)