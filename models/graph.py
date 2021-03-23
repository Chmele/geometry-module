from models import Vertex, Edge, OrientedEdge
from typing import List, Tuple, OrderedDict

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
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(Edge(v1, v2))


class OrientedGraph(Graph):
    def __init__(self):
        super().__init__()
    
    def add_edge(self, v1: Vertex, v2: Vertex, weight: int):
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(OrientedEdge(v1, v2, weight))

    def get_sorted_by_y_verticies(self) -> List:
        return list(sorted(self.vertices, key = lambda x: x.point.y))
    
    def is_regular(self) -> bool:
        y_sorted_verticies = self.get_sorted_by_y_verticies()
        y_sorted_verticies = y_sorted_verticies[1:-1]
        origin_vertecies = [ edge.v1 for edge in self.edges ]
        end_vertecies = [ edge.v2 for edge in self.edges ]
        for vertex in y_sorted_verticies:
            if vertex not in origin_vertecies:
                return False
            if vertex not in end_vertecies:
                return False
        return True
