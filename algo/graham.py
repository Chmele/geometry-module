from math import pi as pi
from models import Point


def graham(points):
    i = 2
    while Point.direction(points[0], points[1], points[i]) == 0:
        i += 1
    origin = Point.centroid([points[0], points[1], points[i]])

    yield origin
    min_point = max(points, key=lambda p: (-p.y, p.x))
    ordered = sort_points(points, origin, min_point)
    yield [min_point] + ordered[1:]

    ordered.append(min_point)
    steps_table = []
    ans = make_hull(steps_table, ordered)
    yield steps_table
    yield ans


def sort_points(points, origin, min_point):
    min_angle = min_point.polar_angle_with(origin)

    def angle_and_dist(p):
        p_angle = p.polar_angle_with(origin)
        angle = p_angle if p_angle >= min_angle else 2 * pi + p_angle
        return (angle, p.dist_to_point(origin))

    return sorted(points, key=angle_and_dist)


def make_hull(steps_table, ordered):
    ans = ordered[:2]
    for p in ordered[2:]:
        while len(ans) > 1 and Point.direction(ans[-2], ans[-1], p) >= 0:
            steps_table.append(current_step(ordered, ans, False, p))
            ans.pop()

        if len(ans) > 1:
            steps_table.append(current_step(ordered, ans, True, p))
        ans.append(p)

    return ans[:-1]


def current_step(li, ans, add, p):
    """Current step: current points, add/delete, point to add/delete."""
    point = li.index(ans[-1])
    return ([li.index(ans[-2]), point, li.index(p)], add, point)
