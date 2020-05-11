from enum import Enum


class TerrainType(Enum):
    """An enumeration of the types of terrain"""
    UNDEFINED = 0, 'UNDEFINED state. (Not in use)'
    ICE = 1, 'ICE terrain.'
    SWAMP = 2, 'SWAMP terrain.'
    FOREST = 3, 'FOREST terrain'
    SAND = 4, 'SAND terrain'
    SHALLOWS = 5, 'SHALLOWS terrain'
    ROCKS = 6, 'ROCKS terrain'
    PLAIN = 7, 'PLAINS terrain'

    def __str__(self):
        return str(self.name)
