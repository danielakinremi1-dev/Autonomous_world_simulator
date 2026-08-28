import pytest
from world_objects.terrain import Terrain

def test_Terrain():
    new = Terrain("grass")
    print(new.type)
    new2 = Terrain("ground")
    print(new2.emoji) 

    assert "grass" == new.type
    assert "ground" == new2.type
        
def test_invalid_terrain():
    with pytest.raises(ValueError):
        new3 = Terrain("banana")
