class Vertex:
    def __init__(self, point):
        self.point = point

    def __eq__(self, other):
        return self.point.__eq__(other)

    def __getitem__(self, x):
        return self.point.coords[x]

    def __str__(self):
        return str(self.point)
