from models import Point


def jarvis(points):
    ind = points.index(min(points, key=lambda p: p.x))
    lm, ans, length = ind, [points[ind]], len(points)

    while True:
        next = (lm + 1) % length
        for i in range(length):
            if i != lm and direction_correct(points, lm, i, next):
                    next = i
        lm = next

        if lm == ind:
            break
        ans.append(points[next])
    
    return ans


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
