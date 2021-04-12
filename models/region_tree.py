from models import Node, BinTree
from itertools import groupby, chain


class RegionTree(BinTree):
    def __init__(self, points):
        self.__y_sort_flat = lambda l: sorted(chain.from_iterable(l), key=lambda u: u.y)
        self.x_ordered = sorted(points)
        self.y_ordered = sorted(self.x_ordered, key=lambda u: u.y)
        self.projections = [list(g) for _, g in groupby(self.x_ordered, key=lambda u: u.x)]
        interval = [1, len(self.projections)]
        super().__init__(Node([interval, self.__y_sort_flat(self.projections)]))
        self.__build(self.root)

    def __build(self, node: Node):
        start, end = node.data[0]
        mid = (end + start) // 2
        if (end - start) == 1:
            return
        l_int, r_int = [start, mid], [mid, end]
        l_list = self.__y_sort_flat(self.projections[start - 1:mid])
        r_list = self.__y_sort_flat(self.projections[mid - 1:end])
        if l_list:
            node.left = Node([l_int, l_list])
            self.__build(node.left)
        if r_list:
            node.right = Node([r_int, r_list])
            self.__build(node.right)

    def region_search(self, x_range, y_range):
        x_norm = self.region_normalization(self.projections, x_range)
        if not x_norm:
            return []
        nodes = RegionTree.primary_search(self.root, x_norm)
        res = set(chain.from_iterable(self.secondary_search(node.data[1], y_range) for node in nodes))
        return res

    @staticmethod
    def region_normalization(projections, x_range):
        enum = list(enumerate([ls[0] for ls in projections]))
        l_bound = next((x for x, val in enum if val.x >= x_range[0]), None)
        r_bound = next((x for x, val in reversed(enum) if val.x <= x_range[1]), None)
        return [l_bound + 1, r_bound + 1] if l_bound is not None and r_bound is not None else []

    @staticmethod
    def primary_search(node: Node, interval):
        begin, end = node.data[0]
        if begin == interval[0] and end == interval[1]:
            return [node]
        mid = (end + begin) // 2
        nodes = []
        if node.left and interval[0] < mid:
            new_interval = [interval[0], mid if interval[1] > mid else interval[1]]
            nodes.extend(RegionTree.primary_search(node.left, new_interval))
        if node.right and interval[1] > mid:
            new_interval = [mid if interval[0] < mid else interval[0], interval[1]]
            nodes.extend(RegionTree.primary_search(node.right, new_interval))
        return nodes

    @staticmethod
    def secondary_search(ls, interval):
        enum = list(enumerate(ls))
        l_bound = next((x for x, val in enum if val.y >= interval[0]), None)
        r_bound = next((x for x, val in reversed(enum) if val.y <= interval[1]), None)
        return ls[l_bound:r_bound + 1] if l_bound is not None and r_bound is not None else []
