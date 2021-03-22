from models import Vertex, Edge


class Graph:
    def __init__(self):
        self.vertices, self.edges = set(), set()

    def __str__(self):
        return str(self.edges)

    def get_sorted_vertices(self):
        return list(sorted(map(lambda x: x.point.tuple, self.vertices)))

    def add_vertex(self, v: Vertex):
        self.vertices.add(v)

    def add_edge(self, v1: Vertex, v2: Vertex):
        if v1 in self.vertices and v2 in self.vertices:
            self.edges.add(Edge(v1, v2))
