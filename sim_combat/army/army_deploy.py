from enum import Enum


class ArmyDeploy(Enum):
    """An enumeration of the types of army deployments"""
    UNDEFINED = 0, 'UNDEFINED type. will do Random distribution'
    HORIZONTAL = 1, 'Horizontal.'
    VERTICAL = 2, 'Vertical.'
    UP_DIAGONAL = 3, 'Upper Diagonal.'
    DOWN_DIAGONAL = 4, 'Down Diagonal.'
    RADIAL = 5, 'Radial.'
    SQUARE = 6, 'Square.'
    TRIANGLE = 7, 'Triangle.'

    def __str__(self):
        return str(self.name)
