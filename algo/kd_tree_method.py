from models import Node, BinTree

def kd_tree(points):
    ordered = sorted(points)
    root = Node(ordered[len(ordered) // 2])
    make_tree(ordered, root)
    tree = BinTree(root)
    tree.print_tree(root)
    # TODO: bin search in this tree


def make_tree(list, node: Node, vertical=True):
    med = len(list) // 2
    if med == 0:
        return

    if vertical:
        sort_key = lambda p: p.y
    else:
        sort_key = lambda p: p.x

    list_l = sorted(list[:med], key=sort_key)
    list_r = sorted(list[-med:], key=sort_key)
    left = list_l[len(list_l) // 2]
    right = list_r[len(list_r) // 2]
    
    node.left = Node(left)
    if (node.data != right):
        node.right = Node(right)

    make_tree(list_l, node.left, not vertical)
    make_tree(list_r, node.right, not vertical)