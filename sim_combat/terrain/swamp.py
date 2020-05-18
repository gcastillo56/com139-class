from terrain.terrain import Terrain


class Swamp(Terrain):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._factor = 0.5

    def __str__(self):
        return "Swamp: " + super().__str__()
