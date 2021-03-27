class Edge:
    def __init__(self, v1, v2, weight=0):
        self.v1, self.v2, self.weight = v1, v2, weight

    def __hash__(self):
        return hash(self.v1) + hash(self.v2)

    def __eq__(self, other):
        return set((self.v1, self.v2)) == set((other.v1, other.v2))

    def __str__(self):
        return '({}, {})'.format(self.v1, self.v2) + f"weight = {repr(self.weight)}"


class OrientedEdge(Edge):
    def __hash__(self):
        return super().__hash__() + hash(self.weight)

    def __eq__(self, other: Edge):
        return (self.v1, self.v2) == (other.v1, other.v2)

    def __repr__(self):
        return f"{repr(self.v1)}->{repr(self.v2)}, weight = {repr(self.weight)}"
