from algo.jarvis import jarvis
import unittest
from models import Point, Vertex, Graph, Edge, BinTree, Node
from algo import stripe_method as s
from algo.jarvis import jarvis
import math
import functools as f
from algo import kd_tree_method as kd


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
        tree = BinTree(Node(Point(8, 13)), [], [])
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
        self.assertEqual(tree, next(ans))
        self.assertEqual(r_pts, sorted(next(ans)))
