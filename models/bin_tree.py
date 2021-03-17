from models import Node


class BinTree:
    def __init__(self, root: Node):
        self.root = root

    def __eq__(self, other):
        return self.root == other.root

    def print_tree(self, root):
        print('data = ' + str(root.data))
        print('left = ' + str(root.left.data)) if root.left else print('left = None')
        print('right = ' + str(root.right.data)) if root.right else print('right = None')
        print('----')

        if root.left:
            self.print_tree(root.left)
        if root.right:
            self.print_tree(root.right)

class BinTreeChains(BinTree):
    def __init__(self, root: Node, x_range, y_range):
        super().__init__(root, x_range, y_range)
    
    def make_tree(self, list: List, node: Node):
        mid = len(list) // 2

        if mid == 0:
            return

        list_l = list[:mid]
        list_r = list[-mid:]
        left, right = list_l[mid // 2], list_r[mid // 2]

        node.left = Node(left, node)
        if (node.data != right):
            node.right = Node(right, node)

        self.make_tree(list_l, node.left)
        self.make_tree(list_r, node.right)

    def search_dot(self, point: Point) -> Tuple:
        current_node = self.root 
        while not (current_node.left == None and current_node.right == None):
            edge = list(filter(lambda edge: edge.v1.point.y >= point.y and edge.v2.point.y < point.y, current_node.data))[0]
            location = (point.x - edge.v1.point.x)*(edge.v2.point.y - edge.v1.point.y) - (point.y - edge.v1.point.y)*(edge.v2.point.x - edge.v1.point.x)
            if location > 0:
                
                if current_node.right:
                    current_node = current_node.right
                    left_parent = current_node.parent
                else:
                    return (left_parent, current_node)
            elif location < 0:
                
                if current_node.left:
                    current_node = current_node.left
                    right_parent = current_node.parent
                else:
                    return (current_node, right_parent)
            else:
                return(current_node, None)