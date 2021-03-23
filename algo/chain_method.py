from models import Edge, Point, NodeWithParent, ChainsBinTree, OrientedGraph
from typing import List, Tuple, OrderedDict
from collections import OrderedDict


def create_structure(graph: OrientedGraph) -> OrderedDict:
    """
    Creating weighted table for graph
    "vin" - "in" edges of a vertex sorted counterclockwise
    "vout" - "out" edges of a vertex sorted clockwise
    "win" - sum of vin weights
    "wout" - sum of vout weights
    {
        vertex : {
            "vin": [e1, e2 ...],
            "vout": [e5, e9 ...],
            "wout": 4,
            "win": 5
            }
    }
    """
    weight_table: OrderedDict = OrderedDict()

    for vertex in graph.get_sorted_by_y_verticies():

        vertex_data = dict()
        vin = list()
        vout = list()

        for edge in graph.edges:
            start = edge.v1
            end = edge.v2
            if vertex == start:
                vout.append(edge)
            if vertex == end:
                vin.append(edge)

        vin = sort_vin(vin)
        vout = sort_vout(vout)

        vertex_data["vin"] = vin
        vertex_data["vout"] = vout

        if not vin:
            vertex_data["win"] = 0
        else:
            vertex_data["win"] = sum(edge.weight for edge in vin)

        if not vout:
            vertex_data["wout"] = 0
        else:
            vertex_data["wout"] = sum(edge.weight for edge in vout)

        weight_table[vertex] = vertex_data
    return weight_table


def sort_vin(edges: List[Edge]):
    """Sorting "in" edges of the vertex clockwise"""
    if not edges:
        return edges

    less_then_end = list()
    greater_then_end = list()
    as_origin = None
    sorted_vin = list()

    for edge in edges:
        if edge.v1.point.x > edge.v2.point.x:
            greater_then_end.append(edge)
        elif edge.v1.point.x < edge.v2.point.x:
            less_then_end.append(edge)
        else:
            as_origin = edge

    less_then_end.sort(
        key=lambda edge: (edge.v2.point.y - edge.v1.point.y)
        / (edge.v2.point.x - edge.v1.point.x)
    )

    greater_then_end.sort(
        key=lambda edge: (edge.v2.point.y - edge.v1.point.y)
        / (edge.v1.point.x - edge.v2.point.x),
        reverse=True,
    )

    if as_origin is not None:
        less_then_end.append(as_origin)

    sorted_vin.extend(less_then_end)
    sorted_vin.extend(greater_then_end)

    return sorted_vin


def sort_vout(edges: List[Edge]):
    """Sorting "out" edges of the vertex clockwise"""

    if not edges:
        return edges

    less_then_origin = list()
    greater_then_origin = list()
    as_origin = None
    sorted_vout = list()

    for edge in edges:
        if edge.v2.point.x > edge.v1.point.x:
            greater_then_origin.append(edge)
        elif edge.v2.point.x < edge.v1.point.x:
            less_then_origin.append(edge)
        else:
            as_origin = edge

    less_then_origin.sort(
        key=lambda edge: (edge.v2.point.y - edge.v1.point.y)
        / (edge.v1.point.x - edge.v2.point.x)
    )
    greater_then_origin.sort(
        key=lambda edge: (edge.v2.point.y - edge.v1.point.y)
        / (edge.v2.point.x - edge.v1.point.x),
        reverse=True,
    )

    if as_origin is not None:
        less_then_origin.append(as_origin)

    sorted_vout.extend(less_then_origin)
    sorted_vout.extend(greater_then_origin)

    return sorted_vout


def balance(weight_table: OrderedDict):
    """balancing weight table"""
    counter = 0
    dict_length = len(weight_table) - 1
    for vertex, vertex_data in weight_table.items():

        if counter == dict_length:
            break

        if vertex_data["win"] > vertex_data["wout"]:
            edge_to_update = vertex_data["vout"][0]
            old_weight = edge_to_update.weight
            edge_to_update.weight = vertex_data["win"] - vertex_data["wout"] + 1
            delta_weight = edge_to_update.weight - old_weight
            vertex_data["wout"] += delta_weight

            for vertex_data in weight_table.values():
                for edge in vertex_data["vin"]:
                    if edge == edge_to_update:
                        vertex_data["win"] += delta_weight

        counter += 1

    counter = 0
    for vertex, vertex_data in reversed(weight_table.items()):

        if counter == dict_length:
            break

        if vertex_data["win"] < vertex_data["wout"]:
            edge_to_update = vertex_data["vin"][0]
            old_weight = edge_to_update.weight
            edge_to_update.weight = vertex_data["wout"] - vertex_data["win"] + 1
            delta_weight = edge_to_update.weight - old_weight
            vertex_data["win"] += delta_weight

            for vertex_data in weight_table.values():
                for edge in vertex_data["vout"]:
                    if edge == edge_to_update:
                        vertex_data["wout"] += delta_weight

        counter += 1


def create_chains(weight_table: OrderedDict):
    """
    Creating chains from the start of
    the graph to the end point of the graph
    """

    chains = list()
    chain = list()
    current = None

    first = list(weight_table.keys())[0]
    last = list(weight_table.keys())[-1]
    current = first
    while weight_table.get(first)["wout"] != 0:
        while current != last:
            edge = weight_table[current]["vout"][0]
            if edge.weight == 0:
                weight_table[current]["vout"].pop(0)
                edge = weight_table[current]["vout"][0]
                chain.append(edge)
                edge.weight -= 1
                weight_table[current]["wout"] -= 1
                weight_table[edge.v2]["win"] -= 1
            else:
                chain.append(edge)
                edge.weight -= 1
                weight_table[current]["wout"] -= 1
                weight_table[edge.v2]["win"] -= 1

            current = edge.v2

        chains.append(chain)
        chain = list()
        current = first

    return chains


def find_dot(graph: OrientedGraph, point: Point) -> Tuple:
    if not graph.is_regular():
        return (None, None)
    else:
        weight_table = create_structure(graph)
        balance(weight_table=weight_table)
        chains = create_chains(weight_table)

        root = NodeWithParent(data=chains[len(chains) // 2])
        tree = BinTreeChains(root)
        tree.make_tree(chains, root)
        return tree.search_dot(point)
