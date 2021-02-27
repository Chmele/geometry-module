from geometry.module.models.point import Point
from geometry.module.models.bin_tree_node import Node
from geometry.module.models.bin_tree import BinTree
from algo.kd_tree_method import kd_tree
import unittest
from models import Point, Vertex, Graph
from algo import stripe_method as s


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
        tree.root.left.right = Node(Point(5, 3))
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
        
        ans = kd_tree(pts, rx, ry)

        self.assertEqual(sorted(pts), next(ans))
        self.assertEqual(tree, next(ans))
        self.assertEqual(r_pts, sorted(next(ans)))
