class Terrain:

    # features
    # - kind of terrain
    # - height will affect movement based on direction of neighbors
    # -- higher ground increase visual range
    # -- lower ground reduce visual range
    # MIXED
    # [ [x, y, [swamp]], [x, y, [rocks]],
    #   [x, y, [ice]], [x, y, [sand]]
    # ]
    # [ [x, y, [ice]], [x, y, [ice]],
    #   [x, y, [ice]], [x, y, [ice]]
    # ]

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._factor = 1

    def __str__(self) -> str:
        return "(%d, %d) - %f" % (self._x, self._y, self._factor)

    def cross(self) -> float:
        return self._factor

