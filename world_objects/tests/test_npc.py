import pytest
from world_objects.world import World
from world_objects.npc import NPC
from world_objects.configs import npc_configs

def test_npc_creation():
    TEST_MAP = [
    ["ground", "ground", "ground"],
    ["ground", "ground", "ground"],
    ["grass",  "grass",  "grass"],
] 
    world = World(TEST_MAP)    

    npc_type = next(iter(npc_configs))

    npc = NPC(3, 5, npc_type, world)

    assert npc.x == 3
    assert npc.y == 5
    assert npc.npc_type == npc_type
    assert npc.health == npc_configs[npc_type]["health"]
    assert npc.emoji == npc_configs[npc_type]["emoji"]


def test_npc_invalid_type():
    TEST_MAP = [
    ["ground", "ground", "ground"],
    ["ground", "ground", "ground"],
    ["grass",  "grass",  "grass"],
] 
    world = World(TEST_MAP)

    with pytest.raises(ValueError):
        NPC(0, 0, "invalid_npc", world)


def test_npcs_store_independent_positions():
    TEST_MAP = [
    ["ground", "ground", "ground"],
    ["ground", "ground", "ground"],
    ["grass",  "grass",  "grass"],
] 
    world = World(TEST_MAP)
    npc_type = next(iter(npc_configs))

    npc_one = NPC(1, 2, npc_type, world)
    npc_two = NPC(7, 4, npc_type, world)

    assert npc_one.x == 1
    assert npc_one.y == 2
    assert npc_two.x == 7
    assert npc_two.y == 4
