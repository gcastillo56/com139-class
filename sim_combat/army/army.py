from characters.character import Character
from characters.chicken import Chicken
from characters.jedi import Jedi
from characters.soldier import Soldier
from characters.spartan import Spartan
from characters.trex import Trex
from characters.clan import Clan
from characters.character_type import CharacterType
from army.army_deploy import ArmyDeploy
from map.map import Map


class Army:

    def __init__(self, army_clan: Clan) -> None:
        self._clan_id = army_clan
        self._deployment = ArmyDeploy.UNDEFINED
        self._army_type = CharacterType.UNDEFINED
        self._size = 0
        self._army = []

    def __str__(self) -> str:
        str_val = str("(%s) Type: %s\n" % (self._clan_id.name, self._army_type.name))
        str_val += str("Deployment strategy: %s\n" % self._deployment.name)
        str_val += str("Size: %d\n" % self._size)
        str_val += str(self._army)
        return str_val

    @property
    def deploy(self) -> ArmyDeploy:
        return self._deployment

    @deploy.setter
    def deploy(self, value: ArmyDeploy) -> None:
        self._deployment = value

    @property
    def army_type(self) -> CharacterType:
        return self._army_type

    @army_type.setter
    def army_type(self, value: CharacterType) -> None:
        self._army_type = value

    @property
    def army(self):
        return self._army

    def createArmy(self, size: int) -> None:
        self._size = size
        self._army = []
        # TODO: create the mechanism to define the deploy shape of the army
        if self._deployment == ArmyDeploy.HORIZONTAL:
            self._deployHorizontal()
        elif self._deployment == ArmyDeploy.VERTICAL:
            self._deployVertical()
        elif self._deployment == ArmyDeploy.UP_DIAGONAL:
            pass
        elif self._deployment == ArmyDeploy.DOWN_DIAGONAL:
            pass
        elif self._deployment == ArmyDeploy.RADIAL:
            pass
        elif self._deployment == ArmyDeploy.SQUARE:
            pass
        elif self._deployment == ArmyDeploy.TRIANGLE:
            pass
        else:       # Random
            pass
        pass

    def _addElement(self, x: int, y: int) -> None:
        if self._army_type == CharacterType.SOLDIER:
            element = Soldier(x, y)
        elif self._army_type == CharacterType.CHICKEN:
            element = Chicken(x, y)
        elif self._army_type == CharacterType.JEDI_KNIGHT:
            element = Jedi(x, y)
        elif self._army_type == CharacterType.SPARTAN:
            element = Spartan(x, y)
        elif self._army_type == CharacterType.T_REX:
            element = Trex(x, y)
        element.clan = self._clan_id
        self._army.append(element)

    def _boundingBox(self) -> ((float, float), (float, float)):
        get_x = lambda val: val.x
        get_y = lambda val: val.y
        xs = list(map(get_x, self._army))
        ys = list(map(get_y, self._army))
        return (min(xs), min(ys)), (max(xs), max(ys))

    def _deployHorizontal(self):
        min_x = 0
        max_x = Map.getMap().width
        if self._clan_id == Clan.RED:
            min_y = 0
            max_y = Map.getMap().height / 3
        else:
            min_y = (Map.getMap().height / 3) * 2
            max_y = Map.getMap().height
        pos_x = min_x + 1
        pos_y = min_y + 1
        for p in range(self._size):
            self._addElement(pos_x, pos_y)
            pos_x += 1
            if pos_x == max_x - 1:
                pos_x = min_x + 1
                pos_y += 1

    def _deployVertical(self):
        min_y = 0
        max_y = Map.getMap().height
        if self._clan_id == Clan.RED:
            min_x = 0
            max_x = Map.getMap().width / 3
        else:
            min_x = (Map.getMap().width / 3) * 2
            max_x = Map.getMap().width
        pos_x = min_x + 1
        pos_y = min_y + 1
        for p in range(self._size):
            self._addElement(pos_x, pos_y)
            pos_y += 1
            if pos_y == max_y - 1:
                pos_y = min_y + 1
                pos_x += 1

    def getCenter(self) -> (float, float):
        avg_x = 0
        avg_y = 0
        for x in range(self._size):
            avg_x += self._army[x].x
            avg_y += self._army[x].y
        return (avg_x/self._size), (avg_y/self._size)

    def step(self, enemy) -> None:
        center = enemy.getCenter()
        print(center)
        pass

