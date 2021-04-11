from models import Point
from typing import Tuple, List
from sys import maxsize


def closest_points(points: List[Point]):
    Ux, Uy = init_points(points)
    return closest_pair(Ux, Uy)


def init_points(points: List[Point]):
    Ux = sorted(points, key=lambda point: point.x)
    Uy = sorted(points, key=lambda point: point.y)
    #U = {point: {"x": Ux.index(point), "j": Uy.index(point)} for point in points}
    return Ux, Uy


def closest_pair_split(
    points_sorted_x: List[Point], points_sorted_y: List[Point], delta: float
):
    """Finding closest pair of points splited by the line"""
    length_x = len(points_sorted_x)
    middle = length_x // 2
    middle_point = points_sorted_x[middle]
    points_sorted_x = list(
        filter(
            lambda point: point.dist_to_point(middle_point) <= delta, points_sorted_x
        )
    )
    left_points_x = list(
        filter(lambda point: point.x <= middle_point.x, points_sorted_x)
    )
    right_points_x = list(
        filter(lambda point: point.x > middle_point.x, points_sorted_x)
    )

    left_points_x.sort(key=lambda point: point.y)
    right_points_x.sort(key=lambda point: point.y)

    min_dist_pairs: List[Tuple] = []

    for point_left in left_points_x:
        in_range = list(
            filter(
                lambda point_right: abs(point_right.y - point_left.y) < delta,
                right_points_x,
            )
        )
        if in_range:
            min_dist_pair = (
                point_left,
                min(in_range, key=lambda point: point_left.dist_to_point(point)),
            )
            min_dist_pairs.append(min_dist_pair)

    if min_dist_pairs:
        return min(min_dist_pairs, key=lambda pair: pair[0].dist_to_point(pair[1]))
    else:
        return None


def closest_pair(points_sorted_x: List[Point], points_sorted_y: List[Point]):
    """Finding closest pair of points"""
    length_x = len(points_sorted_x)
    dist_left, dist_right, dist_split = 3*[maxsize]

    if length_x < 2:
        return None
    elif length_x == 2:
        point1, point2 = points_sorted_x
        return (point1, point2)
    else:
        middle = length_x // 2
        middle_point = points_sorted_x[middle]

        left_sorted_y = sorted(
            list(filter(lambda point: point.x < middle_point.x, points_sorted_y)),
            key=lambda p: p.y,
        )

        right_sorted_y = sorted(
            list(filter(lambda point: point.x >= middle_point.x, points_sorted_y)),
            key=lambda p: p.y
        )

        closest_points_left: Tuple[Point] = closest_pair(
            points_sorted_x[:middle], left_sorted_y
        )
        closest_points_right: Tuple[Point] = closest_pair(
            points_sorted_x[middle:], right_sorted_y
        )

        if closest_points_left:
            dist_left = closest_points_left[0].dist_to_point(closest_points_left[1])

        if closest_points_right:
            dist_right = closest_points_right[0].dist_to_point(closest_points_right[1])

        delta = min(dist_left, dist_right)

        closest_points_split: Tuple[Point] = closest_pair_split(
            points_sorted_x, points_sorted_y, delta
        )

        if closest_points_split:
            dist_split = closest_points_split[0].dist_to_point(closest_points_split[1])

        minimum = min(dist_left, dist_right, dist_split)
        if minimum == dist_left:
            return closest_points_left
        elif minimum == dist_right:
            return closest_points_right
        else:
            return closest_points_split
