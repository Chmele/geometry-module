class Edge:
    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2

    def __hash__(self):
        return hash(self.v1) + hash(self.v2)

    def __eq__(self, other):
        return set((self.v1, self.v2)) == set((other.v1, other.v2))

    def __str__(self):
        return '({}, {})'.format(self.v1, self.v2)
