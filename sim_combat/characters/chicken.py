from characters.character import Character


class Chicken(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._health = 100
        self._speed = 4
        self._damage = 1
        self._protection = 1
        self._attack_range = 1
        self._visual_range = 10

    def __str__(self):
        return "\n--Chicken-- \n" + super().__str__()
