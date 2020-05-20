from map import Map
from characters.clan import Clan


class Character:

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._clan = Clan.UNDEFINED
        self._health = 0
        self._visual_range = 0
        self._speed = 0
        self._attack_range = 0
        self._damage = 0
        self._protection = 0

    def __str__(self) -> str:
        str_val = str("Location: (%d, %d)\n" % (self._x, self._y))
        str_val += str("Clan: %s\n" % self._clan.name)
        str_val += str("Health: %.2f\n" % self._health)
        str_val += str("Speed: %.2f\n" % self._speed)
        str_val += str("Visual Range: %.2f\n" % self._visual_range)
        str_val += str("Attack Range: %.2f\n" % self._attack_range)
        str_val += str("Damage: %.2f\n" % self._damage)
        str_val += str("Protection: %.2f\n" % self._protection)
        return str_val

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def clan(self) -> Clan:
        return self._clan

    @clan.setter
    def clan(self, value: int):
        if value == 1:
            self._clan = Clan.RED
        elif value == 2:
            self._clan = Clan.BLUE

    def move(self, center_x: float, center_y: float) -> None:
        """This function represents the interaction between my character and the environment.

        Returns
        -------

        """
        terrain = Map.getTerrainAt(self._x, self._y)
        print(terrain)
        pass

    def battle(self):
        """ This function will represent the interaction between characters, from both sides.

        Returns
        -------

        """
        pass


