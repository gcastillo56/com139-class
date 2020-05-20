
from terrain.terrain_type import *
from characters.soldier import Soldier
from characters.jedi import Jedi
from characters.clan import Clan
from army.army import Army
from map import Map
from characters.character_type import CharacterType

m = Map(4, 4)
print(m.instance)
m.assign_type(TerrainType.FOREST)
print(m)

m3 = Map(-1, -1)
print(m3)

print("terrain at")
print(m3.getTerrainAt(1, 1))

ch = Soldier(4, 7)
ch.clan = 1
print(ch)

ch = Jedi(4, 7)
ch.clan = 7
print(ch)

a = Army(1)
a.army_type = CharacterType.SOLDIER
a.createArmy(50)
print(a)

mp = Map.getMap()
print(mp)


