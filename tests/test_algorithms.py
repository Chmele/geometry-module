from algo.jarvis import jarvis
import unittest
from models import Point, Vertex, Graph
from algo import stripe_method as s
from algo.jarvis import jarvis

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
        