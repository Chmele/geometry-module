class Node:
    def __init__(self, data):
        """By default Node has no children."""
        self.data = data
        self.left = None
        self.right = None

    def __eq__(self, other):
        """Recursive equality."""
        return (
            self.data == other.data
            and self.left == other.left
            and self.right == other.right
        )
