def direction_correct(points, i1, i2, i3):
    p1, p2, p3 = points[i1], points[i2], points[i3]
    d = direction(p1, p2, p3)
    return (
        d > 0 or
        d == 0 and
        p1.dist_to(p2) > p1.dist_to(p3)
    )


def direction(p1, p2, p3):
    return cross_product(p3 - p1, p2 - p1)


def cross_product(p1, p2):
    return p1.x * p2.y - p2.x * p1.y