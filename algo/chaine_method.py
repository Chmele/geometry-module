from models import Graph, Vertex, Edge

class OrientedEdge(Edge):
    def __init__(self, weight: int):
        super().__init__()
        self.weight = weight

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: Edge):
        return (self.v1, self.v2) == (other.v1, other.v2)
    
class OrientedGraph(Graph):
    def __init__(self,):
        super().__init__()
        self.directions = dict()

    def add_edge(self, v1: Vertex, v2: Vertex, weight: int):
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(OrientedEdge(v1, v2, weight))

    def isRegularGraph(self) -> bool:
        pass

def findDot(graph: OrientedGraph) -> bool:
    if not graph.isRegularGraph():
        return False 
    
        
        
