class Terrain:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._factor = 1

    def __str__(self) -> str:
        return "(%d, %d) - %.2f" % (self._x, self._y, self._factor)

    def cross(self) -> float:
        return self._factor

