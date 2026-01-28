from enum import Enum


class Status(Enum):
    """An enumeration of the gen_customer states"""
    UNDEFINED = 0, 'UNDEFINED state. (Not in use)'
    SUCCESS = 1, 'SUCCESS state.'
    WAIT = 2, 'WAITING state.'
    RENEGED = 3, 'RENEGED state. Used when the gen_customer is tired of waiting'

    def __str__(self):
        return str(self.name)

