from characters.character import Character
from characters.chicken import Chicken
from characters.jedi import Jedi
from characters.soldier import Soldier
from characters.spartan import Spartan
from characters.trex import Trex
from characters.character_type import CharacterType
from army.army_deploy import ArmyDeploy


class Army:

    def __init__(self, army_id: int) -> None:
        self._id = army_id
        self._deployment = ArmyDeploy.UNDEFINED
        self._army_type = CharacterType.UNDEFINED
        self._size = 0
        self._army = []

    def __str__(self) -> str:
        str_val = str("(%d) Type: %s\n" % (self._id, self._army_type.name))
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

    def createArmy(self, size: int) -> None:
        self._size = size
        self._army = []
        # TODO: create the mechanism to define the deploy shape of the army
        if self._army_type == ArmyDeploy.HORIZONTAL:
            pass
        elif self._army_type == ArmyDeploy.VERTICAL:
            pass
        elif self._army_type == ArmyDeploy.UP_DIAGONAL:
            pass
        elif self._army_type == ArmyDeploy.DOWN_DIAGONAL:
            pass
        elif self._army_type == ArmyDeploy.RADIAL:
            pass
        elif self._army_type == ArmyDeploy.SQUARE:
            pass
        elif self._army_type == ArmyDeploy.TRIANGLE:
            pass
        else:       # Random
            pass
        pass

    def _addElement(self, x: int, y: int) -> None:
        if self._army_type == CharacterType.SOLDIER:
            self._army.append(Soldier(x, y))
        elif self._army_type == CharacterType.CHICKEN:
            self._army.append(Chicken(x, y))
        elif self._army_type == CharacterType.JEDI:
            self._army.append(Jedi(x, y))
        elif self._army_type == CharacterType.SPARTAN:
            self._army.append(Spartan(x, y))
        elif self._army_type == CharacterType.TREX:
            self._army.append(Trex(x, y))

    def _boundingBox(self) -> ((float, float), (float, float)):
        get_x = lambda val: val.x
        get_y = lambda val: val.y
        xs = list(map(get_x, self._army))
        ys = list(map(get_y, self._army))
        return (min(xs), min(ys)), (max(xs), max(ys))

    def getCenter(self) -> (float, float):
        avg_x = 0
        avg_y = 0
        for x in range(self._size):
            avg_x += self._army[x].x
            avg_y += self._army[x].y
        return (avg_x/self._size), (avg_y/self._size)
