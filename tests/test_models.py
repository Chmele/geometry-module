import unittest
from models import Point, Vertex, Graph


class TestModels(unittest.TestCase):
    '''Test class for basic entities'''
    def test_point_creation(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2, 3.6)
        self.assertEqual(p1.coords, (1, 2))
        self.assertEqual(p2.coords, (1, 2, 3.6))

    def test_graph_vertex_add(self):
        g = Graph()
        v1 = Vertex(Point(1, 2))
        v2 = Vertex(Point(2, 1))

        g.add_vertex(v1)
        g.add_vertex(v2)

        g.add_edge(v1, v2)
        g.add_edge(v2, v1)

        self.assertEqual(len(g.edges), 1)

    def test_point_domination(self):
        a = Point(1,2)
        b = Point(3,4)
        c = Point(2,2)
        self.assertTrue(b.dominating(a))
        self.assertTrue(b.dominating(c))
        self.assertFalse(a.dominating(c))