from terrain.terrain_type import TerrainType
from terrain.terrain import Terrain
from terrain.ice import Ice
from terrain.swamp import Swamp
from terrain.forest import Forest


class Map:
    instance = None

    def __init__(self,  w: int, h: int):
        if not Map.instance:
            Map.instance = Map.__Map(w, h)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self) -> str:
        if not Map.instance:
            return "No map"
        return str(Map.instance)

    @staticmethod
    def getTerrainAt(x: int, y: int) -> Terrain:
        if not Map.instance:
            return None
        return Map.instance.__getTerrainAt(x, y)

    @staticmethod
    def getMap():
        if not Map.instance:
            return None
        return Map.instance

    class __Map:
        # dimensions
        def __init__(self, w: int, h: int):
            self._width = w
            self._height = h
            self._map = [[0 for x in range(w)] for y in range(h)]
            self._ttype = TerrainType.UNDEFINED
            # TODO: read the height map

        def __str__(self) -> str:
            str_val = "["
            for x in range(self._width):
                str_val += "["
                for y in range(self._height):
                    str_val += str(self._map[x][y])
                    str_val += " | "
                str_val += "]\n"
            str_val += "]\n"
            return str_val

        @property
        def width(self) -> int:
            return self._width

        @property
        def height(self) -> int:
            return self._height

        # map.assign_type(TerrainType.ICE)
        def assign_type(self, ttype: TerrainType) -> None:
            self._ttype = ttype
            if ttype == TerrainType.ICE:
                self._map = [[Ice(x, y) for x in range(self._width)] for y in range(self._height)]
            elif ttype == TerrainType.SWAMP:
                self._map = [[Swamp(x, y) for x in range(self._width)] for y in range(self._height)]
            elif ttype == TerrainType.FOREST:
                self._map = [[Forest(x, y) for x in range(self._width)] for y in range(self._height)]
            pass

        def __getTerrainAt(self, x: int, y: int) -> Terrain:
            return self._map[x][y]


