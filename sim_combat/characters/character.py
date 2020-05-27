from map.map import Map
from characters.clan import Clan
from typing import Union


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

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, value: float) -> None:
        self._health = value

    @property
    def range(self) -> float:
        return self._attack_range

    @property
    def range(self) -> float:
        return self._attack_range

    @property
    def clan(self) -> Clan:
        return self._clan

    @clan.setter
    def clan(self, value: Union[int, Clan]) -> None:
        if isinstance(value, Clan):
            self._clan = value
        else:
            if value == 1:
                self._clan = Clan.RED
            elif value == 2:
                self._clan = Clan.BLUE

    def move(self, move_vector: (float, float)) -> bool:
        """This function represents the interaction between my character and the environment.

        The speed and terrain part that follows could be simplified in our current case, since all the terrain is
        the same and the speed of our army elements is all equal. But in a more complex situation, where the terrain
        is heterogeneous and we have a mixed army, this code would be able to handle properly the movement in such
        cases

        Returns
        -------

        """
        factor = Map.getTerrainAt(int(self._x), int(self._y)).cross() * self._speed
        m_x = move_vector[0] * factor
        m_y = move_vector[1] * factor
        new_x = self._x + m_x
        new_y = self._y + m_y
        if Map.getMap().width >= new_x >= 0:
            self._x = new_x
        elif Map.getMap().width < new_x:
            self._x = Map.getMap().width
        else:
            self._x = 0
        if Map.getMap().height >= new_y >= 0:
            self._y = new_y
        elif Map.getMap().height < new_y:
            self._y = Map.getMap().height
        else:
            self._y = 0
        return True

    def battle(self):
        """ This function will represent the interaction between characters, from both sides.

        Returns
        -------

        """
        pass


