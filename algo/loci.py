from models import Point


class Loci:
    """Is a wrap of a dict {Point: int}, int is amount of points smaller than key point"""

    def __init__(self):
        self.repr = {}

    def append_points(self, *li):
        for point in li:
            self.append_point(point)

    def append_point(self, point):
        self.repr.update({point: self.query(point) + 1})
        self.repr.update(
            {p: self.query(p) + 1 for p in self.get_dominating_points(point, 0)}
        )
        self.repr.update(
            {p: self.query(p) + 1 for p in self.get_dominating_points(point, 1)}
        )

    def query(self, point):
        mins = list(filter(point.dominating, self.repr))
        if mins:
            return self.repr[max(mins)]
        return 0

    def get_dominating_points(self, point, dimension):
        dim_coords = (
            i[dimension] for i in self.repr if point[dimension] < i[dimension]
        )
        p_coords = list(point.coords)

        def new_dot(value):
            ret = list(p_coords)
            ret[dimension] = value
            return Point(*ret)

        return map(new_dot, dim_coords)

    def get_points_in_rect(self, rect):
        x, y = rect
        q = self.query
        return (
            q(Point(x[1], y[1]))
            - q(Point(x[0], y[1]))
            - q(Point(x[1], y[0]))
            + q(Point(x[0], y[0]))
        )
