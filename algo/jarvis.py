from algo.hull_common import direction_correct


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
