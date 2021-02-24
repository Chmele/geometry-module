from models import Node, BinTree

def kd_tree(points, x_range, y_range):
    # Stage 1
    ordered = sorted(points)
    
    # Stage 2
    root = Node(ordered[len(ordered) // 2])
    tree = BinTree(root, x_range, y_range)
    tree.make_tree(ordered, root)

    # Stage 3
    return tree.region_search(root, vertical=True)
