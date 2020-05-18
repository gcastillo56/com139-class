from enum import Enum


class CharacterType(Enum):
    """An enumeration of the types of characters"""
    UNDEFINED = 0, 'UNDEFINED type. (Not in use)'
    SOLDIER = 1, 'Soldier.'

    def __str__(self):
        return str(self.name)
