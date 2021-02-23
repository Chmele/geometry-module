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

    def __lt__(self, other):
        return self.coords < other.coords
