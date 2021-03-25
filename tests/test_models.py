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

    def test_vectors(self):
        a = Vector([1, 1])
        b = Vector([0, 12])
        self.assertAlmostEqual(a.angle(b), math.pi / 4)

    def test_polygon_in(self):
        p1 = Point(1, 1)
        p2 = Point(1, -1)
        p3 = Point(-1, -1)
        p4 = Point(-1, 1)
        p = Polygon([p1, p2, p3, p4])

        p0 = Point(0, 0)
        pn = Point(1.1, 1)
        self.assertEqual(p.contains_point(p0), True)
        self.assertNotEqual(p.contains_point(pn), True)

    def test_point_centroid(self):
        p1 = Point(1, 2, 3)
        p2 = Point(1, 5, 6)
        p3 = Point(1, 2, 3)
        self.assertEqual(Point.centroid((p1, p2, p3)), Point(1, 3, 4))

        p1 = Point(1, 2, 3)
        p2 = Point(1, 5, 6)
        p3 = Point(1, 2, 3)
        p4 = Point(1, 2, 3)
        self.assertEqual(Point.centroid((p1, p2, p3, p4)), Point(1, 2.75, 3.75))

    def test_triangle_area(self):
        p1 = Point(0, 1)
        p2 = Point(0, 0)
        p3 = Point(1, 0)
        t = Triangle(p1, p2, p3)
        self.assertAlmostEqual(t.area, 0.5)

        p1 = Point(-100, 0)
        p2 = Point(0, 100)
        p3 = Point(100, 0)
        t = Triangle(p1, p2, p3)
        self.assertAlmostEqual(t.area, 10000)

    def test_polygon_area(self):
        p1 = Point(0, 0)
        p2 = Point(0, 100)
        p3 = Point(100, 100)
        p4 = Point(100, 0)
        p = Polygon((p1, p2, p3, p4))
        self.assertAlmostEqual(p.area, 10000)

    def test_hull_sum(self):
        p1 = Point(2, 2)
        p2 = Point(2, -2)
        p3 = Point(-2, -2)
        p4 = Point(-2, 2)
        r1 = Polygon((p1, p2, p3, p4))
        p1 = Point(3, 0)
        p2 = Point(0, -3)
        p3 = Point(-3, 0)
        p4 = Point(0, 3)
        r2 = Polygon((p1, p2, p3, p4))

        h = Hull(r1) + Hull(r2)
        self.assertEqual(
            h,
            [
                Point(0.0, -3.0),
                Point(2.0, -2.0),
                Point(3.0, 0.0),
                Point(2.0, 2.0),
                Point(0.0, 3.0),
                Point(-2.0, 2.0),
                Point(-3.0, 0.0),
                Point(-2.0, -2.0),
            ],
        )

        p1 = Point(2, 2)
        p2 = Point(2, 0)
        p3 = Point(0, 0)
        p4 = Point(0, 2)
        r1 = Polygon((p1, p2, p3, p4))
        p1 = Point(-2, -2)
        p2 = Point(-2, 0)
        p3 = Point(0, -1)
        p4 = Point(0, -2)
        r2 = Polygon((p1, p2, p3, p4))

        h = Hull(r1) + Hull(r2)
        self.assertEqual(
            h,
            [
                Point(-2.0, -2.0),
                Point(0.0, -2.0),
                Point(2.0, 0.0),
                Point(2.0, 2.0),
                Point(0.0, 2.0),
                Point(-2.0, 0.0),
            ],
        )


    def test_point_belonging_to_triangle(self):
        # one side of the triangle is parallel to one of the coordinate axes
        tr1 = Triangle(Point(-1, -1), Point(1, -1), Point(0, 1))
        tp1 = Point(2, 2)  # point lies outside the triangle
        tp2 = Point(0, 0)  # point lies inside the triangle
        tp3 = Point(0, 1)  # point coincides with the apex of the triangle
        tp4 = Point(0.5, 0)  # point lies on one of the sides of the triangle
        tp5 = Point(1, 3)  # point lies on the extension of one of the sides of the triangle
        self.assertFalse(tr1.point_belonging(tp1))
        self.assertTrue(tr1.point_belonging(tp2))
        self.assertTrue(tr1.point_belonging(tp3))
        self.assertTrue(tr1.point_belonging(tp4))
        self.assertFalse(tr1.point_belonging(tp5))

        # two sides of the triangle are parallel to the coordinate axes
        tr2 = Triangle(Point(0, 0), Point(2, 0), Point(0, 2))
        tp6, tp7 = Point(1, 1), Point(5, 5)
        self.assertTrue(tr2.point_belonging(tp6))
        self.assertFalse(tr2.point_belonging(tp7))

        tr3 = Triangle(Point(3, 4), Point(4, 6), Point(6, 8))
        tp8 = Point(5, 7.01)
        self.assertFalse(tr3.point_belonging(tp8))
