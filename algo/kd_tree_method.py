from models import Node, BinTree

def kd_tree(points, x_range, y_range):
    ordered = sorted(points)
    yield ordered

    root = Node(ordered[len(ordered) // 2])
    tree = BinTree(root, x_range, y_range)
    tree.make_tree(ordered, root)
    yield tree

    yield tree.region_search(root, vertical=True)
