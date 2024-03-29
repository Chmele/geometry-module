from models import Point


def jarvis(points):
    return list(jarvis_gen(points))[-1]

def jarvis_gen(points):
    min_point = min(points, key=lambda p: p.x)
    yield min_point

    ind = points.index(min_point)
    lm, ans, length = ind, [points[ind]], len(points)

    while True:
        nxt = (lm + 1) % length
        for i in range(length):
            if i != lm and direction_correct(points, lm, i, nxt):
                nxt = i
        lm = nxt

        if lm == ind:
            break
        ans.append(points[nxt])

    yield ans


def direction_correct(points, i1, i2, i3):
    p1, p2, p3 = points[i1], points[i2], points[i3]
    d = Point.direction(p1, p2, p3)
    return (
        d < 0 or
        d == 0 and
        p1.dist_to_point(p2) > p1.dist_to_point(p3)
    )
