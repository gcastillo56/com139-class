from terrain.terrain_type import *
from characters.character import *
from map import Map


m = Map(4,4)
print(m.instance)
m.assign_type(TerrainType.FOREST)
print(m)
m1 = Map(1,1)
m1.assign_type(TerrainType.ICE)
print (m1)

m2 = Map(10,10)
m2.assign_type(TerrainType.SWAMP)
print(m2)

m3 = Map(-1,-1)
print(m3)

print("terrain at")
print(m3.getTerrainAt(1, 1))

ch = Character()
print(ch)
