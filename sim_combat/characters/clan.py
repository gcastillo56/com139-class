from enum import Enum


class Clan(Enum):
    """An enumeration of the types of characters"""
    UNDEFINED = 0, 'UNDEFINED type. (Not in use)'
    RED = 1, 'Red'
    BLUE = 2, 'Blue'

    def __str__(self):
        return str(self.name)
