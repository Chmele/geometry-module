from models import Node


class BinTree:
    def __init__(self, root: Node):
        self.root = root

    def __eq__(self, other):
        return self.root == other.root
