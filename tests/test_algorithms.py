import unittest
from models import Point, Vertex, Graph, Edge
from algo import stripe_method as s
import math
import functools as f


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
        self.assertEqual(ans[3], [Edge(p4, p6), Edge(p3, p6)])

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