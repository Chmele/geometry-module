class Edge:
    def __init__(self, v1, v2):
        self.v1, self.v2 = v1, v2

    def __hash__(self):
        return hash(self.v1) + hash(self.v2)

    def __eq__(self, other):
        return set((self.v1, self.v2)) == set((other.v1, other.v2))

    def __str__(self):
        return '({}, {})'.format(self.v1, self.v2)

class OrientedEdge(Edge):
    def __init__(self, v1, v2, weight: int):
        self.weight = weight
        super().__init__(v1, v2)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: Edge):
        return (self.v1, self.v2) == (other.v1, other.v2)

    def __repr__(self):
        return f"OrEdge(weight={repr(self.weight)}, v1={repr(self.v1)}, v2={repr(self.v2)})"
    
