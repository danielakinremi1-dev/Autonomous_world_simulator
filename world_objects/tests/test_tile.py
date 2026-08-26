from terrain import Terrain
from tile import Tile


grassblock = Terrain("grass")
tileblock = Tile(grassblock)
print(tileblock.can_enter())