class Vertex:
    def __init__(self, point):
        self.point = point

    def __hash__(self):
        return hash(self.point)

    def __eq__(self, other):
        return self.point == other.point

    def __getitem__(self, x):
        return self.point.coords[x]

    def __str__(self):
        return str(self.point)

    def __repr__(self):
        return str(self)
