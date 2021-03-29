from models import Point, RegionTree


def region_tree_method(points, x_range, y_range):
    reg_tree = RegionTree(points)
    nodes, sec_structs, points = reg_tree.region_search(x_range, y_range)
