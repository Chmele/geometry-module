from models import Node


class BinTree:
    def __init__(self, root: Node, x_range, y_range):
        self.root = root
        self.x_range = x_range
        self.y_range = y_range

    def make_tree(self, list, node: Node, vertical=True):
        med = len(list) // 2
        if med == 0:
            return

        if vertical:
            sort_key = lambda p: p.y
        else:
            sort_key = lambda p: p.x

        list_l = sorted(list[:med], key=sort_key)
        list_r = sorted(list[-med:], key=sort_key)
        left, right = list_l[med // 2], list_r[med // 2]
    
        node.left = Node(left)
        if (node.data != right):
            node.right = Node(right)

        self.make_tree(list_l, node.left, not vertical)
        self.make_tree(list_r, node.right, not vertical)

    def region_search(self, node: Node, vertical=True):
        if vertical:
            left, right, coord = self.x_range[0], self.x_range[1], node.data.x
        else:
            left, right, coord = self.y_range[0], self.y_range[1], node.data.y
        
        dots = []
        if self.dot_in_region(node.data):
            dots.append(node.data)

        if node.left and left < coord:
            dots.extend(self.region_search(node.left, not vertical))
        if node.right and coord < right:
            dots.extend(self.region_search(node.right, not vertical))

        return dots

    def dot_in_region(self, dot):
        return (
            self.x_range[0] <= dot.x and dot.x <= self.x_range[1] and
            self.y_range[0] <= dot.y and dot.y <= self.y_range[1]
        )

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