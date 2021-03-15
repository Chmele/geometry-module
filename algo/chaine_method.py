from models import Graph, Vertex, Edge, Point, BinTree, Node
from typing import List, Tuple, OrderedDict
from collections import OrderedDict

class NodeWithParent(Node):
    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent

class BinTreeChains(BinTree):
    def __init__(self):
        super().__init__()
    
    def make_tree(self, list: List, node: Node):
        mid = len(list) // 2

        if mid == 0:
            return
        
        list_l = list[:mid]
        list_r = list[-mid:]
        left, right = list_l[mid // 2], list_r[mid // 2]

        node.left = Node(left, node)
        if (node.data != right):
            node.right = Node(right, node)

        self.make_tree(list_l, node.left)
        self.make_tree(list_r, node.right)

    def search_dot(self, point: Point) -> Tuple:
        current_node = self.root 
        while not (current_node.left == None and current_node.right == None):
            edge = list(filter(lambda edge: edge.v1.point.y >= point.y and edge.v2.point.y < point.y, current_node.data))[0]
            location = (point.x - edge.v1.point.x)*(edge.v2.point.y - edge.v1.point.y) - (point.y - edge.v1.point.y)*(edge.v2.point.x - edge.v1.point.x)
            if location > 0:
                
                if current_node.right:
                    current_node = current_node.right
                    left_parent = current_node.parent
                else:
                    return (left_parent, current_node)
            elif location < 0:
                
                if current_node.left:
                    current_node = current_node.left
                    right_parent = current_node.parent
                else:
                    return (current_node, right_parent)
            else:
                return(current_node, None)

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
        
            VIN.sort(key = lambda x: x.v2.point.x, reversed = True) 
            VOUT = sort_VOUT(VOUT)
        
        vertex_data["VIN"] = VIN
        vertex_data["VOUT"] = VOUT
        vertex_date["WIN"] = sum(edge.weight for edge in VIN)
        vertex_data["WOUT"] = sum(edge.weight for edge in VOUT)

        weight_table[vertex] = vertex_data
    return weight_table

        
def sort_VOUT(edges: List[Edge]):
    less_then_origin = list()
    greater_then_origin = list()
    as_origin = None
    sorted_VOUT = list()

    for edge in edges:
        if edge.v2.x > edge.v1.x:
            greater_then_origin.append(edge)
        elif edge.v2.x < edge.v1.x:
            less_then_origin.append(edge)
        else:
            as_origin = edge
    
    less_then_origin.sort(key = lambda x: (x.v2.point.y - x.v1.point.y)/(x.v1.point.x - x.v2.point.x))
    greater_then_origin.sort(key = lambda x: (x.v2.point.y - x.v1.point.y)/(x.v2.point.x - x.v1.point.x))
    less_then_origin.append(as_origin)

    sorted_VOUT.extend(less_then_origin)
    sorted_VOUT.extend(greater_then_origin)

    return sorted_VOUT

def balancingAlgor(weightTable: OrderedDict):
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
    
def creatingChains(weightTable: OrderedDict):

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
        balancingAlgor(weightTable = weightTable)
        chainList = creatingChains(weightTable)

        root = Node(chainList[len(chainList) // 2])
        tree = BinTree(root)
        tree.make_tree(chainList, root)
        yield tree.search_dot(point)
        
    