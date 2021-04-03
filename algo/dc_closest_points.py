from models import Point
from typing import Tuple, List

def init_points(points: List[Point]):
    Ux = sorted(points, key=lambda point: point.x)
    Uy = sorted(points, key=lambda point: point.y)
    U = {point: {"x": Ux.index(point), "j": Uy.index(point)} for point in points}
    yield Ux, Uy, U

def closest_pair_split(points_sorted_x: List[Point], points_sorted_y: List[Point], delta: float):
    '''Finding closest pair of points splited by the line'''
    pass

def closest_pair(points_sorted_x: List[Point], points_sorted_y: List[Point]):
    '''Finding closest pair of points'''
    length_x = len(points_sorted_x)
    if length_x == 2:
        point1, point2 = points_sorted_x
        yield (point1, point2)
    else:
        middle = length_x // 2 
        middle_point = points_sorted_x[middle]

        left_sorted_y = list(filter(lambda point: point.x <= middle_point.x, points_sorted_y))
        left_sorted_y.sort(key = lambda point: point.y) # may be useless cause points_sorted_y is already sorted

        right_sorted_y = list(filter(lambda point: point.x > middle_point.x, points_sorted_y))
        right_sorted_y.sort(key = lambda point: point.y) # may be useless cause points_sorted_y is already sorted

        closest_points_left: Tuple[Point] = closest_pair(points_sorted_x[:middle], left_sorted_y)
        closest_points_right: Tuple[Point] = closest_pair(points_sorted_x[middle:], right_sorted_y)

        dist_left = closest_points_left[0].dist_to_point(closest_points_left[1])
        dist_right = closest_points_right[0].dist_to_point(closest_points_left[1])
        delta = min(dist_left, dist_right)

        closest_points_split: Tuple[Point] = closest_pair_split(points_sorted_x, points_sorted_y, delta)

        dist_split = closest_points_split[0].dist_to_point(closest_points_split[1])

        minimum = min(dist_left, dist_right, dist_split)
        if minimum == dist_left:
            yield closest_points_left
        elif minimum == dist_right:
            yield closest_points_right
        else:
            yield closest_points_split
