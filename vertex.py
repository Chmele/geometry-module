from .point import Point


class Vertex:
    def __init__(self, point: Point):
        self.point = point
        self.id = 0
        self.adjacent = {}
    
    def __str__(self):
        return 'Vertex #' + str(self.id) + ', adjacent: ' + \
            str([x.id for x in self.adjacent])