from point import Point


class Vertex:
    def __init__(self, point: Point, id):
        self.point = point
        self.id = id
    
    def __str__(self):
        return 'Vertex #' + str(self.id)