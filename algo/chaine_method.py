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
    
    for vertex in graph.get_sorted_by_y_verticies():

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

        VIN = sort_VIN(VIN) 
        VOUT = sort_VOUT(VOUT)
        
        vertex_data["VIN"] = VIN
        vertex_data["VOUT"] = VOUT
        if not VIN:
            vertex_data["WIN"] = 0
        else:
            vertex_data["WIN"] = sum(edge.weight for edge in VIN)
        
        if not VOUT:
            vertex_data["WOUT"] = 0 
        else:
            vertex_data["WOUT"] = sum(edge.weight for edge in VOUT)

        weight_table[vertex] = vertex_data
    return weight_table

        
def sort_VIN(edges: List[Edge]):
    """Sorting "in" edges of the vertex clockwise"""
    if not edges:
        return edges
    
    less_then_end = list()
    greater_then_end = list()
    as_origin = None
    sorted_VIN = list()

    for edge in edges:
        if edge.v1.point.x > edge.v2.point.x:
            greater_then_end.append(edge)
        elif edge.v1.point.x < edge.v2.point.x:
            less_then_end.append(edge)
        else:
            as_origin = edge
    
    less_then_end.sort(key = lambda edge: (edge.v2.point.y - edge.v1.point.y)/(edge.v2.point.x - edge.v1.point.x))
    greater_then_end.sort(key = lambda edge: (edge.v2.point.y - edge.v1.point.y)/(edge.v1.point.x - edge.v2.point.x), reverse = True)

    if as_origin != None:
        less_then_end.append(as_origin)
    
    sorted_VIN.extend(less_then_end)
    sorted_VIN.extend(greater_then_end)

    return sorted_VIN

def sort_VOUT(edges: List[Edge]):
    """Sorting "out" edges of the vertex clockwise"""
    
    if not edges:
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
    
    less_then_origin.sort(key = lambda edge: (edge.v2.point.y - edge.v1.point.y)/(edge.v1.point.x - edge.v2.point.x))
    greater_then_origin.sort(key = lambda edge: (edge.v2.point.y - edge.v1.point.y)/(edge.v2.point.x - edge.v1.point.x), reverse = True)

    if as_origin != None:
        less_then_origin.append(as_origin)
    
    sorted_VOUT.extend(less_then_origin)
    sorted_VOUT.extend(greater_then_origin)

    return sorted_VOUT

def balance(weightTable: OrderedDict):
    """balancing weight table"""
    counter = 0
    dict_length = len(weightTable) - 1
    for vertex, vertex_data in weightTable.items():

        if counter == dict_length:
            break

        if vertex_data["WIN"] > vertex_data["WOUT"]:
            edge_to_update = vertex_data["VOUT"][0]
            old_weight = edge_to_update.weight
            edge_to_update.weight = vertex_data["WIN"] - vertex_data["WOUT"] + 1
            delta_weight = edge_to_update.weight - old_weight
            vertex_data["WOUT"] += delta_weight

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
            edge_to_update.weight = vertex_data["WOUT"] - vertex_data["WIN"] + 1
            delta_weight = edge_to_update.weight - old_weight
            vertex_data["WIN"] += delta_weight

            for vertex_data in weightTable.values():
                for edge in vertex_data["VOUT"]:
                    if edge == edge_to_update:
                        vertex_data["WOUT"] += delta_weight

        counter += 1
    
def create_chains(weightTable: OrderedDict):
    """Creating chainse from the start of the graph to the end point of the graph"""

    chainList = list()
    chain = list()
    current = None

    first = list(weightTable.keys())[0]
    last = list(weightTable.keys())[-1]
    current = first
    while weightTable.get(first)["WOUT"] != 0:
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
        chain = list()
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
        return tree.search_dot(point)
