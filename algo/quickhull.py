from models import Line2D, Node, BinTree, point
from algo.hull_common import direction


sort_lr = lambda p: (p.x, -p.y)
sort_rl = lambda p: (-p.x, p.y)


def quickhull(points):
    lp = min(points, key=lambda p: p.coords)
    rp = max(points, key=lambda p: p.coords)
    
    s1 = sorted(left_points(points, lp, rp), key=sort_lr)
    s2 = sorted(left_points(points, rp, lp), key=sort_rl)
    
    tree = BinTree(Node(s1 + s2[1:-1]))
    tree.root.left, tree.root.right = Node(s1), Node(s2)

    ans = partition(s1, lp, rp, tree.root.left) + \
        partition(s2, rp, lp, tree.root.right)[1:-1]
    
    yield tree
    yield ans


def partition(points, left, right, node):
    if len(points) == 2:
        return [left, right]
    
    lr = Line2D(left, right)
    pts = filter(lambda x: x != left and x != right, points)
    h = max(pts, key=lambda p: (p.dist_to_line(lr), p.angle_with(left, right)))

    s1 = left_points(points, left, h)
    s2 = left_points(points, h, right)
    node.left, node.right = Node(s1), Node(s2)

    return (
        partition(s1, left, h, node.left) +
        partition(s2, h, right, node.right)[1:]
    )


def make_subset(points, left, right, sort_key):
    return sorted(
        left_points(points, left, right),
        key=sort_key
    )


def left_points(points, p1, p2):
    '''Points at the left of vector p1->p2 and p1, p2'''
    return (
        [p1] +
        list(filter(lambda p: direction(p1, p2, p) < 0, points)) +
        [p2]
    )
