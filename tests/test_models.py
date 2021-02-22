import unittest
from models import Point, Vertex, Graph


class TestModels(unittest.TestCase):
    def test_point_creation(self):
        p1 = Point(1, 2)
        self.assertEquals((p1.x, p1.y), (1, 2))