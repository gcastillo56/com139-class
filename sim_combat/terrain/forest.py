from terrain.terrain import Terrain


class Forest(Terrain):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._factor = 0.9

    def __str__(self):
        return "Forest: " + super().__str__()
