from models import Node, BinTree


class RegionTree(BinTree):
    def __init__(self, points):
        self.x_ordered = sorted(points, key=lambda u: u.x)
        self.y_key = lambda u: u.y
        interval = [0, len(self.x_ordered) - 1]
        super().__init__(Node([interval, sorted(self.x_ordered, key=self.y_key)]))
        self.__build(self.root)

    def __build(self, node: Node):
        begin, end = node.data[0]
        mid = (end + begin) // 2
        if (end - begin) == 1:
            return
        l_int, r_int = [begin, mid], [mid, end]
        l_list = sorted(self.x_ordered[begin:mid + 1], key=self.y_key)
        r_list = sorted(self.x_ordered[mid:end + 1], key=self.y_key)
        node.left = Node([l_int, l_list])
        node.right = Node([r_int, r_list])
        self.__build(node.left)
        self.__build(node.right)

    def region_search(self, x_range, y_range):
        enum = enumerate(self.x_ordered)
        l_bound = next((x for x, val in enum if val.x >= x_range[0]), None)
        r_bound = next((x for x, val in reversed(list(enum)) if val.x <= x_range[1]), None)
        if l_bound is None or r_bound is None:
            return []
        nodes = RegionTree.primary_search(self.root, [l_bound, r_bound])
        sec_structs = [RegionTree.build_sec_struct(node.data[1]) for node in nodes]
        points = set(RegionTree.secondary_search(tree, y_range) for tree in sec_structs)
        return nodes, sec_structs, points

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
    def build_sec_struct(points):
        if not points:
            return
        mid = (len(points) - 1) // 2
        node = Node(points[mid])
        node.left = RegionTree.build_sec_struct(points[:mid])
        node.right = RegionTree.build_sec_struct(points[mid + 1:])
        return node

    @staticmethod
    def secondary_search(node: Node, interval):
        pass
