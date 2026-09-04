from world_objects.terrain import Terrain
from world_objects.tile import Tile
import pytest

def test_tiles():
    grassblock = Terrain("grass")
    tileblock = Tile(1, 1, grassblock)
    assert tileblock.can_enter() == True