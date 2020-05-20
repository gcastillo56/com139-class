from characters.character import Character


class Trex(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._health = 100
        self._speed = 4
        self._damage = 8
        self._protection = 2
        self._attack_range = 2
        self._visual_range = 40

    def __str__(self):
        return "\n--T-Rex-- \n" + super().__str__()
