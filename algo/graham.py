import math
from models import Point
from algo.hull_common import direction


def graham(points):
    origin = min(points, key=lambda p: p.y)

    def angle_and_dist(p):
        return (p.polar_angle_with(origin), p.dist_to(origin))

    ordered = sorted(points, key=angle_and_dist)
    ans = [origin, ordered[0]]

    for p in ordered:
        while len(ans) > 1 and direction(ans[-2], ans[-1], p) >= 0:
            ans.pop()
        ans.append(p)
    
    return ans


