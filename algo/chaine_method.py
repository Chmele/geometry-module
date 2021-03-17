from models import Graph, Vertex, Edge, Point, BinTree, Node, NodeWithParent, BinTreeChains, OrientedEdge, OrientedGraph
from typing import List, Tuple, OrderedDict
from collections import OrderedDict


def createStructure(graph: OrientedGraph) -> OrderedDict:
    """
    Creating weighted table for graph
    "VIN" - "in" edges of a vertex sorted counterclockwise
    "VOUT" - "out" edges of a vertex sorted clockwise
    "WIN" - sum of VIN weights
    "WOUT" - sum of VOUT weights
    {vertex : {"VIN": [e1, e2 ...], "VOUT": [e5, e9 ...], "WOUT": 4, "WIN": 5 }}
    """
    weight_table: OrderedDict = OrderedDict()
    
    for vertex in graph._get_sorted_by_y_verticies():

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
        
            VIN.sort(key = lambda x: x.v2.point.x, reverse = True) 
            VOUT = sort_VOUT(VOUT)
        
        vertex_data["VIN"] = VIN
        vertex_data["VOUT"] = VOUT
        vertex_data["WIN"] = sum(edge.weight for edge in VIN)
        vertex_data["WOUT"] = sum(edge.weight for edge in VOUT)

        weight_table[vertex] = vertex_data
    return weight_table

        
def sort_VOUT(edges: List[Edge]):
    if len(edges) < 2:
        return edges
    
    less_then_origin = list()
    greater_then_origin = list()
    as_origin = None
    sorted_VOUT = list()

    for edge in edges:
        if edge.v2.point.x > edge.v1.point.x:
            greater_then_origin.append(edge)
        elif edge.v2.point.x < edge.v1.point.x:
            less_then_origin.append(edge)
        else:
            as_origin = edge
    
    less_then_origin.sort(key = lambda x: (x.v2.point.y - x.v1.point.y)/(x.v1.point.x - x.v2.point.x))
    greater_then_origin.sort(key = lambda x: (x.v2.point.y - x.v1.point.y)/(x.v2.point.x - x.v1.point.x))
    less_then_origin.append(as_origin)

    sorted_VOUT.extend(less_then_origin)
    sorted_VOUT.extend(greater_then_origin)

    return sorted_VOUT

def balance(weightTable: OrderedDict):
    counter = 0
    dict_length = len(weightTable) - 1
    for vertex, vertex_data in weightTable.items():

        if counter == dict_length:
            break

        if vertex_data["WIN"] > vertex_data["WOUT"]:
            edge_to_update = vertex_data["VOUT"][0]
            old_weight = edge_to_update.weight
            edge.weight = vertex_data["WIN"] - vertex_data["WOUT"] + 1
            delta_weight = edge_to_update.weight - old_weight

            for vertex_data in weightTable.values():
                for edge in vertex_data["VIN"]:
                    if edge == edge_to_update:
                        vertex_data["WIN"] += delta_weight
        
        counter += 1

    counter = 0
    for vertex, vertex_data in reversed(weightTable.items()):
        
        if counter == dict_length:
            break

        if vertex_data["WIN"] < vertex_data["WOUT"]:
            edge_to_update = vertex_data["VIN"][0]
            old_weight = edge_to_update.weight
            edge.weight = vertex_data["WOUT"] - vertex_data["WIN"] + 1
            delta_weight = edge_to_update.weight - old_weight

            for vertex_data in weightTable.values():
                for edge in vertex_data["VOUT"]:
                    if edge == edge_to_update:
                        vertex_data["WOUT"] += delta_weight

        counter += 1
    
def create_chains(weightTable: OrderedDict):

    chainList = list()
    chain = list()
    current = None

    first = weightTable.keys()[0]
    last = weightTable.keys()[-1]
    current = first
    while weightTable.get(first)["WOU"] != 0:
        while current != last:
            edge = weightTable[current]["VOUT"][0]
            if edge.weight == 0:
                weightTable[current]["VOUT"].pop(0)
                edge = weightTable[current]["VOUT"][0]
                chain.append(edge)
                edge.weight -= 1  
                weightTable[current]["WOUT"] -= 1
                weightTable[edge.v2]["WIN"] -= 1
            else:
                chain.append(edge)
                edge.weight -= 1
                weightTable[current]["WOUT"] -= 1
                weightTable[edge.v2]["WIN"] -= 1

            current = edge.v2

        chainList.append(chain)
        current = first

    return chainList
                        
def findDot(graph: OrientedGraph, point: Point) -> Tuple:
    if not graph.isRegularGraph():
        return (None, None)
    else:
        weightTable = createStructure(graph)
        balance(weightTable = weightTable)
        chainList = create_chains(weightTable)

        root = NodeWithParent(data = chainList[len(chainList) // 2])
        tree = BinTreeChains(root)
        tree.make_tree(chainList, root)
        yield tree.search_dot(point)
        
if __name__ == "__main__":
    dot = Point(4, 3)
    graph = OrientedGraph()

    v1 = Vertex(Point(4, 2))
    v2 = Vertex(Point(2, 4))
    v3 = Vertex(Point(6, 5))
    v4 = Vertex(Point(5, 7))
    
    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_vertex(v3)
    graph.add_vertex(v4)

    e1 = OrientedEdge(v1, v2, 1)
    e2 = OrientedEdge(v1, v3, 1)
    e3 = OrientedEdge(v2, v3, 1)
    e4 = OrientedEdge(v2, v4, 1)
    e5 = OrientedEdge(v3, v4, 1)

    graph.add_edge(v1, v2, 1)
    graph.add_edge(v1, v3, 1)
    graph.add_edge(v2, v3, 1)
    graph.add_edge(v2, v4, 1)
    graph.add_edge(v3, v4, 1)
    
    def test_create_sctructure(graph: chaine_method.OrientedGraph):
        ans = createStructure(graph)
        true_structre ={
            v1:{"VIN": [], "VOUT": [e1, e2], "WIN": 0, "WOUT": 2}, 
            v2:{"VIN": [e1], "VOUT": [e4, e3], "WIN": 1, "WOUT": 2}, 
            v3:{"VIN": [e3, e2], "VOUT": [e5], "WIN": 2, "WOUT": 1}, 
            v4:{"VIN": [e4, e5], "VOUT": [], "WIN": 0, "WOUT": 2}, 
        }
        if true_structre == ans:
            return True
    
    print(test_create_sctructure(graph))