from characters.character import Character


class Spartan(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._health = 100
        self._speed = 1
        self._damage = 4
        self._protection = 1
        self._attack_range = 2
        self._visual_range = 20

    def __str__(self):
        return "\n--Spartan-- \n" + super().__str__()
