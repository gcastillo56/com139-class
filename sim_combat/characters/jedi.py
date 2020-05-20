from characters.character import Character


class Jedi(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._health = 100
        self._speed = 4
        self._damage = 6
        self._protection = 1
        self._attack_range = 3
        self._visual_range = 30

    def __str__(self):
        return "\n--Jedi-- \n" + super().__str__()
