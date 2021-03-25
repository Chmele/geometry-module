from models import Vertex, Edge, OrientedEdge

class Graph:
    def __init__(self):
        self.vertices, self.edges = set(), set()

    def __str__(self):
        """Return str for edges of graph."""
        return str(self.edges)

    def sorted_vertices(self, sort_key):
        return sorted(self.vertices, key=sort_key)

    def add_vertex(self, v: Vertex):
        self.vertices.add(v)

    def add_edge(self, v1: Vertex, v2: Vertex):
        edge = Edge(v1, v2)
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(Edge(v1, v2))


class OrientedGraph(Graph):
    def add_edge(self, v1: Vertex, v2: Vertex, weight: int):
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(OrientedEdge(v1, v2, weight))
    
    def is_regular(self):
        '''
            Checks whether a graph is regular, i.e. each of its vertices
            has both incoming and outcoming edge(s),
            except for the starting (no incoming) and ending (no outcoming). 
        '''
        sorted_vertices = self.sorted_vertices(sort_key=lambda v: v.point.y)[1:-1]
        regular_vertices = [e.v1 for e in self.edges] + [e.v2 for e in self.edges]

        return all(v in regular_vertices for v in sorted_vertices)
