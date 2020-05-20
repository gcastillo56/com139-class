from characters.character import Character


class Soldier(Character):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._health = 100
        self._speed = 1
        self._damage = 4
        self._protection = 2
        self._attack_range = 6
        self._visual_range = 20

    def __str__(self):
        return "\n--Soldier-- \n" + super().__str__()
