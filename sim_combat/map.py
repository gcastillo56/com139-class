from terrain import Terrain
from terrain_type import TerrainType


class Map:
    # dimensions
    def __init__(self, w: int, h: int):
        self.map[w][h]
        self._ttype = TerrainType.UNDEFINED
        # TODO: read the height map
        # TODO: Assign the type of terrain

    # map.assign_type(TerrainType.ICE)
    def assign_type(self, ttype: TerrainType) -> None:
        self._ttype = ttype
        pass

