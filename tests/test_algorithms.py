import unittest
from models import Point, Vertex, Graph, Edge, BinTree, KdTree, Node, OrientedGraph, OrientedEdge, NodeWithParent
from collections import OrderedDict
from algo import stripe_method as s
from algo import kd_tree_method as kd
from algo.jarvis import jarvis
from algo.graham import graham
from algo.quickhull import quickhull
from algo.loci import Loci
from algo.chaine_method import createStructure, balance, create_chains, findDot
import math
import copy


class TestAlgorithms(unittest.TestCase):
    '''Algorithm tests'''
    def test_stripe(self):
        p1 = Vertex(Point(7, 0))
        p2 = Vertex(Point(2, 2.5))
        p3 = Vertex(Point(12, 3))
        p4 = Vertex(Point(8, 5))
        p5 = Vertex(Point(0, 7))
        p6 = Vertex(Point(13, 8))
        p7 = Vertex(Point(6, 11))

        g = Graph()

        g.add_vertex(p1)
        g.add_vertex(p2)
        g.add_vertex(p3)
        g.add_vertex(p4)
        g.add_vertex(p5)
        g.add_vertex(p6)
        g.add_vertex(p7)

        g.add_edge(p1, p2)
        g.add_edge(p1, p3)
        g.add_edge(p2, p3)
        g.add_edge(p7, p6)
        g.add_edge(p3, p6)
        g.add_edge(p4, p6)
        g.add_edge(p4, p5)
        g.add_edge(p4, p7)
        g.add_edge(p5, p7)
        g.add_edge(p2, p5)

        dot = Point(11.5, 5.5)

        ans = list(s.stripe(g, dot))
        self.assertEqual(ans[0], [(-math.inf, 0.0), (0.0, 2.5), (2.5, 3.0), (3.0, 5.0), (5.0, 7.0), (7.0, 8.0), (8.0, 11.0), (11.0, math.inf)])
       
        self.assertTrue(self.fragmentation_eq(ans[1], 
        {
            (-math.inf, 0.0): [], 
            (0.0, 2.5): [Edge(p1, p2), Edge(p1, p3)], 
            (2.5, 3.0): [Edge(p1, p3), Edge(p2, p3), Edge(p2, p5)], 
            (3.0, 5.0): [Edge(p2, p5), Edge(p3, p6)], 
            (5.0, 7.0): [Edge(p2, p5), Edge(p4, p5), Edge(p4, p7), Edge(p4, p6), Edge(p3, p6)], 
            (7.0, 8.0): [Edge(p5, p7), Edge(p4, p7), Edge(p4, p6), Edge(p3, p6)], 
            (8.0, 11.0): [Edge(p5, p7), Edge(p4, p7), Edge(p7, p6)], 
            (11.0, math.inf): []
        }))

        self.assertEqual(ans[2], (5.0, 7.0))
        # self.assertEqual(ans[3], [Edge(p4, p6), Edge(p3, p6)])

    def fragmentation_eq(self, f1, f2):
        for i in f1:
            for item in f1[i]:
                if item not in f2[i]:
                    return False
        for i in f2:
            for item in f2[i]:
                if item not in f1[i]:
                    return False
        return True
        # print(str(ans[1][(5.0, 7.0)][4]))
        print(str(ans[3][0]))

    def test_jarvis1(self):
        pts = [
            Point(1, 4),
            Point(0, 0),
            Point(3, 3),
            Point(3, 1),
            Point(7, 0),
            Point(5, 5),
            Point(5, 2),
            Point(9, 6)
        ]
        hull = [
            Point(0, 0),
            Point(1, 4),
            Point(9, 6),
            Point(7, 0)
        ]
        ans = jarvis(pts)
        self.assertEqual(ans, hull)
    
    def test_jarvis2(self):
        pts = [
            Point(3,3),
            Point(1,1),
            Point(5,0)
        ]
        hull = [
            Point(1,1),
            Point(3,3),
            Point(5,0)
        ]
        ans = jarvis(pts)
        self.assertEqual(ans, hull)
        
    
    def test_kd_tree(self):
        pts = [
            Point(0, 9),
            Point(2, 3),
            Point(3, 6),
            Point(5, 8),
            Point(6, 1),
            Point(8, 13),
            Point(10, 2),
            Point(12, 4),
            Point(14, 11),
            Point(15, 5),
            Point(17, 10)
        ]
        rx = [3, 14]
        ry = [0, 8]
        tree = KdTree(Node(Point(8, 13)), [], [])
        tree.root.left = Node(Point(3, 6))
        tree.root.left.left = Node(Point(6, 1))
        tree.root.left.left.left = Node(Point(2, 3))
        tree.root.left.right = Node(Point(5, 8))
        tree.root.left.right.left = Node(Point(0, 9))
        
        tree.root.right = Node(Point(15, 5))
        tree.root.right.left = Node(Point(12, 4))
        tree.root.right.left.left = Node(Point(10, 2))
        tree.root.right.right = Node(Point(17, 10))
        tree.root.right.right.left = Node(Point(14, 11))

        r_pts = [
            Point(3, 6),
            Point(5, 8),
            Point(6, 1),
            Point(10, 2),
            Point(12, 4),
        ]
        
        ans = kd.kd_tree(pts, rx, ry)
        
        self.assertEqual(sorted(pts), next(ans))
        #self.assertEqual(tree, next(ans))
        #self.assertEqual(r_pts, sorted(next(ans)))

    def test_graham1(self):
        pts = [
            Point(7, 0),
            Point(3, 3),
            Point(0, 0)
        ]
        ordered = [
            Point(0, 0),
            Point(7, 0),
            Point(3, 3)
        ]
        steps = [
            ([0, 1, 2], True, 1),
            ([1, 2, 0], True, 2)
        ]
        hull = [
            Point(0, 0),
            Point(7, 0),
            Point(3, 3)
        ]
        ans = graham(pts)
        self.assertEqual(ordered, next(ans))
        self.assertEqual(steps, next(ans))
        self.assertEqual(hull, next(ans))

    def test_graham2(self):
        pts = [
            Point(3, 10),
            Point(6, 8),
            Point(3, 5),
            Point(2, 8),
            Point(4, 8),
            Point(5, 5),
            Point(3, 3),
            Point(7, 7),
            Point(5, 0),
            Point(0, 0),
            Point(10, 3)
        ]
        ordered = [
            Point(0, 0),
            Point(3, 3),
            Point(5, 0),
            Point(10, 3),
            Point(5, 5),
            Point(7, 7),
            Point(6, 8),
            Point(4, 8),
            Point(3, 10),
            Point(2, 8),
            Point(3, 5)
        ]
        steps = [
            ([0, 1, 2], False, 1),
            ([0, 2, 3], True, 2),
            ([2, 3, 4], True, 3),
            ([3, 4, 5], False, 4),
            ([2, 3, 5], True, 3),
            ([3, 5, 6], True, 5),
            ([5, 6, 7], True, 6),
            ([6, 7, 8], False, 7),
            ([5, 6, 8], True, 6),
            ([6, 8, 9], True, 8),
            ([8, 9, 10], True, 9),
            ([9, 10, 0], False, 10),
            ([8, 9, 0], True, 9)
        ]
        hull = [
            Point(0, 0),
            Point(5, 0),
            Point(10, 3),
            Point(7, 7),
            Point(6, 8),
            Point(3, 10),
            Point(2, 8)
        ]
        ans = graham(pts)
        self.assertEqual(ordered, next(ans))
        self.assertEqual(steps, next(ans))
        self.assertEqual(hull, next(ans))
    
    def test_graham3(self):
        pts = [
            Point(2, 8),
            Point(5, 6),
            Point(7, 8),
            Point(8, 11),
            Point(7, 5),
            Point(10, 7),
            Point(11, 5),
            Point(8, 2),
            Point(1, 3),
            Point(5, 2)
        ]
        ordered = [
            Point(5, 2),
            Point(8, 2),
            Point(7, 5),
            Point(11, 5),
            Point(10, 7),
            Point(8, 11),
            Point(7, 8),
            Point(2, 8),
            Point(5, 6),
            Point(1, 3)
        ]
        steps = [
            ([0, 1, 2], True, 1),
            ([1, 2, 3], False, 2),
            ([0, 1, 3], True, 1),
            ([1, 3, 4], True, 3),
            ([3, 4, 5], False, 4),
            ([1, 3, 5], True, 3),
            ([3, 5, 6], True, 5),
            ([5, 6, 7], False, 6),
            ([3, 5, 7], True, 5),
            ([5, 7, 8], True, 7),
            ([7, 8, 9], False, 8),
            ([5, 7, 9], True, 7),
            ([7, 9, 0], True, 9)
        ]
        hull = [
            Point(5, 2),
            Point(8, 2),
            Point(11, 5),
            Point(8, 11),
            Point(2, 8),
            Point(1, 3)
        ]
        ans = graham(pts)
        self.assertEqual(ordered, next(ans))
        self.assertEqual(steps, next(ans))
        self.assertEqual(hull, next(ans))
    
    def test_quickhull1(self):
        pts = [
            Point(3, 4),
            Point(0, 0),
            Point(7, 2)
        ]
        tree = BinTree(Node([pts[1], pts[0], pts[2]]))
        tree.root.left = Node([pts[1], pts[0], pts[2]])
        tree.root.right = Node([pts[2], pts[1]])
        tree.root.left.left = Node([pts[1], pts[0]])
        tree.root.left.right = Node([pts[0], pts[2]])
        hull = [
            pts[1],
            pts[0],
            pts[2]
        ]

        ans = quickhull(pts)
        self.assertEqual(tree, next(ans))
        self.assertEqual(hull, next(ans))

    def test_quickhull2(self):
        pts = [
            Point(0, 6),
            Point(8, 11),
            Point(10, 4),
            Point(7, 13),
            Point(6, 3),
            Point(3, 0),
            Point(4, 2),
            Point(12, 1),
            Point(14, 10),
            Point(5, 9),
            Point(3, 11),
            Point(1, 4)
        ]
        tree = BinTree(Node([
            pts[0],
            pts[10],
            pts[9],
            pts[3],
            pts[1],
            pts[8],
            pts[7],
            pts[2],
            pts[4],
            pts[6],
            pts[5],
            pts[11]
        ]))

        tree.root.left = Node([pts[0], pts[10], pts[9], pts[3], pts[1], pts[8]])
        tree.root.right = Node([pts[8], pts[7], pts[2], pts[4], pts[6], pts[5], pts[11], pts[0]])
        
        tree.root.left.left = Node([pts[0], pts[10], pts[3]])
        tree.root.left.right = Node([pts[3], pts[8]])
        tree.root.left.left.left = Node([pts[0], pts[10]])
        tree.root.left.left.right = Node([pts[10], pts[3]])
        
        tree.root.right.left = Node([pts[8], pts[7]])
        tree.root.right.right = Node([pts[7], pts[4], pts[6], pts[5], pts[11], pts[0]])
        tree.root.right.right.left = Node([pts[7], pts[5]])
        tree.root.right.right.right = Node([pts[5], pts[0]])

        hull = [pts[0], pts[10], pts[3], pts[8], pts[7], pts[5]]

        ans = quickhull(pts)
        self.assertEqual(tree, next(ans))
        self.assertEqual(hull, next(ans))

    def test_loci(self):
        l = Loci()
        p1 = Point(1, 1)
        p2 = Point(2, 1)
        p3 = Point(2, 3)
        p4 = Point(2, 2)

        l.append_points(p1, p2, p3, p4)
        q = l.query(Point(2.5, 0.5))
        self.assertEqual(q, 0)
        res = l.get_points_in_rect(((1.5, 2.5),(0.5, 3.5)))
        res2 = l.get_points_in_rect(((0.5, 2.5),(0.5, 3.5)))

        self.assertEqual(res, 3)
        self.assertEqual(res2, 4)

        p1 = Point(2, 1)
        p2 = Point(1, 2)
        p3 = Point(0, 3)
        l = Loci()
        l.append_points(p1, p2, p3)
        res = l.get_points_in_rect(((0.5, 2.5), (0.5, 2.5)))
        self.assertEqual(res, 2)

    def test_chain_methode(self):
        graph = OrientedGraph()
        point = Point(4, 5)
        v1 = Vertex(Point(4, 2))
        v2 = Vertex(Point(2, 4))
        v3 = Vertex(Point(6, 5))
        v4 = Vertex(Point(5, 7))
        
        e1 = OrientedEdge(v1, v2, 1)
        e2 = OrientedEdge(v1, v3, 1)
        e3 = OrientedEdge(v2, v3, 1)
        e4 = OrientedEdge(v2, v4, 1)
        e5 = OrientedEdge(v3, v4, 1)

        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)

        graph.add_edge(v1, v2, 1)
        graph.add_edge(v1, v3, 1)
        graph.add_edge(v2, v3, 1)
        graph.add_edge(v2, v4, 1)
        graph.add_edge(v3, v4, 1)

        def test_structure(graph: OrientedGraph):

            weight_table_test = createStructure(graph)

            weight_table = {
                v1: {"VIN": [], "VOUT": [e1, e2], "WIN": 0, "WOUT": 2},
                v2: {"VIN": [e1], "VOUT": [e4, e3], "WIN": 1, "WOUT": 2},
                v3: {"VIN": [e3, e2], "VOUT": [e5], "WIN": 2, "WOUT": 1},
                v4: {"VIN": [e4, e5], "VOUT": [], "WIN": 2, "WOUT": 0}
            }

            weight_table_true = OrderedDict(weight_table)

            self.assertDictEqual(weight_table_test, weight_table_true)

            return weight_table_test

        def test_balancing(weight_table_test: OrderedDict):

            balance(weight_table_test)
            e1_TRUE = copy.deepcopy(e1)
            e1_TRUE.weight = 2
            e5_TRUE = copy.deepcopy(e5)
            e5_TRUE.weight = 2
            weight_table_true = {
                v1: {"VIN": [], "VOUT": [e1_TRUE, e2], "WIN": 0, "WOUT": 3},
                v2: {"VIN": [e1_TRUE], "VOUT": [e4, e3], "WIN": 2, "WOUT": 2},
                v3: {"VIN": [e3, e2], "VOUT": [e5_TRUE], "WIN": 2, "WOUT": 2},
                v4: {"VIN": [e4, e5_TRUE], "VOUT": [], "WIN": 3, "WOUT": 0}
            }

            weight_table_true = OrderedDict(weight_table_true)

            self.assertDictEqual(weight_table_test, weight_table_true)

        def test_creating_chains(weight_table: OrderedDict):
            chain_list_test = list()

            chain_list_test = create_chains(weight_table)
            
            e1_TRUE = copy.deepcopy(e1)
            e1_TRUE.weight = 0
            e2_TRUE = copy.deepcopy(e2)
            e2_TRUE.weight = 0
            e3_TRUE = copy.deepcopy(e3)
            e3_TRUE.weight = 0
            e4_TRUE = copy.deepcopy(e4)
            e4_TRUE.weight = 0
            e5_TRUE = copy.deepcopy(e5)
            e5_TRUE.weight = 0

            chain_list_true = [
                [e1_TRUE, e4_TRUE],
                [e1_TRUE, e3_TRUE, e5_TRUE],
                [e2_TRUE, e5_TRUE]
            ]
            
            self.assertListEqual(chain_list_test, chain_list_true)
            
            return chain_list_test

        def test_find_dot(graph: OrientedGraph, point: Point):

            chain_test = findDot(graph, point)
        
            e1_TRUE = copy.deepcopy(e1)
            e1_TRUE.weight = 0
            e2_TRUE = copy.deepcopy(e2)
            e2_TRUE.weight = 0
            e3_TRUE = copy.deepcopy(e3)
            e3_TRUE.weight = 0
            e4_TRUE = copy.deepcopy(e4)
            e4_TRUE.weight = 0
            e5_TRUE = copy.deepcopy(e5)
            e5_TRUE.weight = 0

            chain_true = (
                [e1_TRUE, e4_TRUE],
                [e1_TRUE, e3_TRUE, e5_TRUE]
            )

            self.assertTupleEqual(chain_true, chain_test)

        weight_table_test = test_structure(graph)
        test_balancing(weight_table_test)
        test_creating_chains(weight_table_test)
        test_find_dot(graph, point)
                