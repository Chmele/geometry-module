from models import Graph, Vertex, Edge
from typing import List

class OrientedEdge(Edge):
    def __init__(self, weight: int):
        super().__init__()
        self.weight = weight

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other: Edge):
        return (self.v1, self.v2) == (other.v1, other.v2)
    
class OrientedGraph(Graph):
    def __init__(self):
        super().__init__()
    
    def add_edge(self, v1: Vertex, v2: Vertex, weight: int):
        if (v1 in self.vertices and v2 in self.vertices):
            self.edges.add(OrientedEdge(v1, v2, weight))

    def graph_as_dict(self) -> dict:
        return { edge.v1 : (edge.v2, edge.weight) for edge in self.edges}

    def _get_sorted_by_y_verticies(self) -> List:
        return list(sorted(self.vertices, key = lambda x: x.point.y))
    
    def isRegularGraph(self) -> bool:
        y_sorted_verticies = self._get_sorted_by_y_verticies()
        y_sorted_verticies = y_sorted_verticies[1:len(y_sorted_verticies) - 2]
        directions = self._graph_as_dict()
        for vertex in y_sorted_verticies:
            if vertex not in directions.keys():
                return False
            if vertex not in [vertex for vertex, weight in list(directions.values())]:
                return False
        return True

def findDot(graph: OrientedGraph) -> bool:
    if not graph.isRegularGraph():
        return False
    
def createStructure(graph: OrientedGraph):
    weight_table = dict()
    directions = graph.graph_as_dict()
    
    for vertex in graph.vertices:
        vertex_data = dict()
        VIN = list()
        VOUT = list()
        for edge in graph.edges:
            start = edge.v1
            end = edge.v2
            if vertex == start:
                VOUT.append(edge)
            if vertex == end:
                VIN.append(edge)
        # відсортувати VIN VOUT
        # Додати в словник разом із їх сумою ваг
        # для кожноъ вершини(ну ми ж в циклі да?) 
        