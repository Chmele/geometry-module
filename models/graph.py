from models import Vertex, Edge, OrientedEdge

class Graph:
    edge_class = Edge

    def __init__(self):
        self.vertices, self.edges = set(), set()

    def __str__(self):
        """Return str for edges of graph."""
        return str(self.edges)

    def sorted_vertices(self, sort_key):
        return sorted(self.vertices, key=sort_key)

    def add_vertex(self, v: Vertex):
        self.vertices.add(v)

    def add_edge(self, v1: Vertex, v2: Vertex, weight=0):
        e1 = self.edge_class(v1, v2, weight)
        e2 = self.edge_class(v2, v1)
        if (v1 in self.vertices and v2 in self.vertices
            and e1 not in self.edges and e2 not in self.edges):
            self.edges.add(e1)


class OrientedGraph(Graph):
    edge_class = OrientedEdge

    def add_edge(self, v1: Vertex, v2: Vertex, weight=0):
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(self.edge_class(v1, v2, weight))

    def is_regular(self):
        '''
            Checks whether a graph is regular, i.e. each of its vertices
            has both incoming and outcoming edge(s),
            except for the starting (no incoming) and ending (no outcoming).
        '''
        sorted_vertices = self.sorted_vertices(sort_key=lambda v: v.point.y)[1:-1]
        regular_vertices = [e.v1 for e in self.edges] + [e.v2 for e in self.edges]

        return all(v in regular_vertices for v in sorted_vertices)
