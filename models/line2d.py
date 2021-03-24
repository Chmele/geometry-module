from models import Point


class Line2D:
    """A 2D line represented by the equation Ax + By + C = 0"""

    def __init__(self, p1: Point, p2: Point):
        """Constuct line by two points."""
        self.p1 = p1
        self.p2 = p2

    @property
    def A(self):
        return self.p1.y - self.p2.y

    @property
    def B(self):
        return self.p2.x - self.p1.x

    @property
    def C(self):
        return self.p1.x * self.p2.y - self.p2.x * self.p1.y
