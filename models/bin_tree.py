from models import Node, Point, NodeWithParent, Edge
from typing import Tuple, List


class BinTree:
    def __init__(self, root: Node):
        self.root = root

    def __eq__(self, other):
        return self.root == other.root

    def print_tree(self, root):
        print("data = " + str(root.data))
        print("left = " + str(root.left.data)) if root.left else print("left = None")
        print("right = " + str(root.right.data)) if root.right else print("right = None")
        print("----")

        if root.left:
            self.print_tree(root.left)
        if root.right:
            self.print_tree(root.right)


class ChainsBinTree(BinTree):
    def __init__(self, root: Node):
        super().__init__(root)

    def make_tree(self, list: List, node: Node):
        mid = len(list) // 2

        if mid == 0:
            return

        list_l = list[:mid]
        list_r = list[-mid:]
        left, right = list_l[mid // 2], list_r[mid // 2]

        node.left = NodeWithParent(left, node)
        if node.data != right:
            node.right = NodeWithParent(right, node)

        self.make_tree(list_l, node.left)
        self.make_tree(list_r, node.right)

    def _point_in_edge(self, edge: Edge, point):
        if edge.v1[1] <= point.y and edge.v2[1] >= point.y:
            return True
        else:
            return False

    def _location_against_edge(self, edge: Edge, point: Point):
        a = (point.x - edge.v1.point.x) * (edge.v2.point.y - edge.v1.point.y)
        b = (point.y - edge.v1.point.y) * (edge.v2.point.x - edge.v1.point.x)
        return a - b

    def search_dot(self, point: Point) -> Tuple:
        current_node = self.root
        location = 0
        right_parent = None
        left_parent = None

        while current_node is not None:
            edge = list(
                filter(lambda edge: self._point_in_edge(edge, point), current_node.data)
            )[0]
            location = self._location_against_edge(edge, point)

            if location > 0:
                if current_node.right is not None:
                    current_node = current_node.right
                    left_parent = current_node.parent
                else:
                    return (current_node.data, right_parent.data)

            elif location < 0:
                if current_node.left is not None:
                    current_node = current_node.left
                    right_parent = current_node.parent
                else:
                    return (left_parent.data, current_node.data)
            else:
                return (current_node.data, None)
