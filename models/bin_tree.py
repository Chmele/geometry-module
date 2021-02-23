class BinTree:
    def __init__(self, root: Node):
        self.root = root

    def print_tree(self, root):
        print('data = ' + str(root.data))
        print('left = ' + str(root.left.data)) if root.left else print('left = None')
        print('right = ' + str(root.right.data)) if root.right else print('right = None')
        print('----')

        if root.left:
            self.print_tree(root.left)
        if root.right:
            self.print_tree(root.right)

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

