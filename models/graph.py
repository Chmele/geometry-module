from models import Point, Vertex


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
    
    def __str__(self):
        return str(self.edges)

    def add_vertex(self, v: Vertex):
        self.vertices.append(v)

    def add_edge(self, v1: Vertex, v2: Vertex, weight = 0):
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.append((v1.id, v2.id, weight))