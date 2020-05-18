from ..map import Map


class Character:

    def __init__(self):
        self._x = 0
        self._y = 0
        self._clan = 0
        self._health = 0
        self._visual_range = 0
        self._speed = 0
        self._attack_range = 0
        self._damage = 0
        self._protection = 0

    def __str__(self) -> str:
        str_val = str("Location: (%d, %d)\n" % (self._x, self._y))
        str_val += str("Clan: %d\n" % self._clan)
        str_val += str("Health: %.2f\n" % self._health)
        str_val += str("Speed: %.2f\n" % self._speed)
        str_val += str("Visual Range: %.2f\n" % self._visual_range)
        str_val += str("Attack Range: %.2f\n" % self._attack_range)
        str_val += str("Damage: %.2f\n" % self._damage)
        str_val += str("Protection: %.2f\n" % self._protection)
        return str_val

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def move(self, center_x: float, center_y: float) -> None:
        """This function represents the interaction between my character and the environment.

        Returns
        -------

        """
        map = Map(-1,-1)

        pass

    def battle(self):
        """ This function will represent the interaction between characters, from both sides.

        Returns
        -------

        """
        pass


