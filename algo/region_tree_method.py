from models import Point, RegionTree


def region_tree_method(points, x_range, y_range):
    reg_tree = RegionTree(points)
    yield reg_tree.x_ordered, reg_tree.y_ordered
    yield reg_tree.projections
    yield reg_tree.root
    x_norm = RegionTree.region_normalization(reg_tree.projections, x_range)
    yield x_norm
    nodes = RegionTree.primary_search(reg_tree.root, x_norm) if x_norm else None
    yield nodes
    yield [RegionTree.secondary_search(node.data[1], y_range) for node in nodes]
