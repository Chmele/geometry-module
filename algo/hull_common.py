def direction(p1, p2, p3):
    return cross_product(p3 - p1, p2 - p1)


def cross_product(p1, p2):
    return p1.x * p2.y - p2.x * p1.y