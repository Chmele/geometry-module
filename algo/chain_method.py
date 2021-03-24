from math import pi as pi
from models import Point, NodeWithParent, ChainsBinTree, OrientedGraph
from collections import OrderedDict


def chain_method(graph: OrientedGraph, point: Point):
    if not graph.is_regular():
        return (None, None)
    else:
        yield graph.sorted_vertices(sort_key=lambda v: v.point.y)

        weight_table = make_weight_table(graph)
        yield weight_table

        balance(weight_table)
        yield weight_table

        chains = create_chains(weight_table)
        yield chains

        root = NodeWithParent(data=chains[len(chains) // 2])
        tree = ChainsBinTree(root)
        tree.make_tree(chains, root)
        yield tree

        return tree.search_dot(point)


def make_weight_table(graph: OrientedGraph):
    """
    Make weighted table for graph:
    "vin" - "in" edges of a vertex sorted counterclockwise
    "vout" - "out" edges of a vertex sorted clockwise
    "win" - sum of vin edges' weights
    "wout" - sum of vout edges' weights
    """
    weight_table = OrderedDict()
    for vertex in graph.sorted_vertices(sort_key=lambda v: v.point.y):
        vertex_data = {}
        vin, vout = [], []

        vin.extend(list(filter(lambda e: e.v2 == vertex, graph.edges)))
        vout.extend(list(filter(lambda e: e.v1 == vertex, graph.edges)))

        vin = sort_v_edges(vin, is_out=False)
        vout = sort_v_edges(vout, is_out=True)

        vertex_data["vin"] = vin
        vertex_data["vout"] = vout

        weight_v_edges(vertex_data, vin, "win")
        weight_v_edges(vertex_data, vout, "wout")

        weight_table[vertex] = vertex_data    
    return weight_table


def sort_v_edges(edges, is_out):
    '''Sort vin edges counterclockwise, vout edges clockwise'''
    if not edges:
        return edges

    def v_angle(p1, p2):
        '''Counterclockwise polar angle to sort by starting from pi/2 (noon)'''
        angle = p1.ccw_polar_angle_with(p2)
        return angle if angle >= pi / 2 else 2 * pi + angle

    if is_out:
        sort_key = lambda e: v_angle(e.v1.point, e.v2.point)
    else:
        sort_key = lambda e: v_angle(e.v2.point, e.v1.point)

    return sorted(edges, key=sort_key, reverse=is_out)


def weight_v_edges(vertex_data, edges, edge_type):
    '''Set total weight of either vin or vout edges of the vertex'''
    if not edges:
        vertex_data[edge_type] = 0
    else:
        vertex_data[edge_type] = sum(e.weight for e in edges)


def balance(weight_table: OrderedDict, is_down):
    '''
        Balance weight table by traversing it forwards and backwards
        and reassigning weight values.
    '''
    if is_down:
        v_type, w_type1, w_type2 = "vin", "win", "wout"
        vertex_data = weight_table.values()
    else:
        v_type, w_type1, w_type2 = "vout", "wout", "win"
        vertex_data = reversed(weight_table.values)
    
    update_edge_weights(vertex_data, v_type, w_type1, w_type2)


def update_edge_weights(vertex_data, v_type, w_type1, w_type2):
    for vd in vertex_data:
        if vd[w_type1] > vd[w_type2]:
            edge_to_update = vd[v_type][0]
            old_weight = edge_to_update.weight
            edge_to_update.weight = vd[w_type1] - vd[w_type2] + 1
            delta_weight = edge_to_update.weight - old_weight
            vd[w_type2] += delta_weight
            
            for x in vertex_data:
                for e in x[v_type]:
                    if e == edge_to_update:
                        x[w_type1] += delta_weight


def create_chains(weight_table: OrderedDict):
    '''Create monotone chains from graph's start to its end'''
    chain, chains = [], []
    current = None

    first = list(weight_table.keys())[0]
    last = list(weight_table.keys())[-1]
    while weight_table.get(first)["wout"] != 0:
        current = first

        while current != last:
            edge = weight_table[current]["vout"][0]
            
            if edge.weight == 0:
                weight_table[current]["vout"].pop(0)
                edge = weight_table[current]["vout"][0]
            
            chain.append(edge)
            edge.weight -= 1
            weight_table[current]["wout"] -= 1
            weight_table[edge.v2]["win"] -= 1
            current = edge.v2

        chains.append(chain)
        chain = []
        current = first

    return chains
