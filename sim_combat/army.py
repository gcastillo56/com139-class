from characters.character import Character
from characters.character_type import CharacterType


class Army:

    def __init__(self, army_id: int):
        self._id = army_id
        self._size = 0
        self._army = [0 for x in range(10)]

    def assignArmy(self, size: int, army_type: CharacterType) -> None:
        self._size = size
        if army_type == CharacterType.SOLDIER:
            self._army = [Character() for x in range(size)]

    def getCenter(self) -> (float, float):
        avg_x = 0
        avg_y = 0
        for x in range(self._size):
            avg_x += self._army[x].x
            avg_y += self._army[x].y
        return (avg_x/self._size), (avg_y/self._size)
