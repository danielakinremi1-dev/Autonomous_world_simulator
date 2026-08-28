from world_objects.constants import DEFAULT_MAP
from world_objects.world import World
from world_objects.configs import npc_configs
import pytest



def test_world():
    new_world = World(DEFAULT_MAP)
    placeholder = [['🟩', '🟩', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🌊', '🌊', '🌊', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🌊', '🌊', '🌊', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌊', '🌊', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🌊', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🌳', '🌳'], ['🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩'], ['🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🌳', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩']]
    assert new_world.get_render_data() == placeholder
    assert str(new_world) == "A 20 by 15 simulated world!" 




TEST_MAP = [
    ["ground", "ground", "ground"],
    ["ground", "ground", "ground"],
    ["grass",  "grass",  "grass"],
]

def test_spawn_npc_creates_all_configured_npcs():
    world = World(TEST_MAP)
    world.spawn_npc()
    assert len(world.npcs) == len(npc_configs)


def test_spawned_npcs_are_on_their_tiles():
    world = World(TEST_MAP)
    world.spawn_npc()
    for npc in world.npcs:
        tile = world.grid[npc.y][npc.x]
        assert tile.occupant is npc


def test_spawned_npcs_have_unique_coordinates():
    world = World(TEST_MAP)
    world.spawn_npc()
    coordinates = [(npc.x, npc.y) for npc in world.npcs]
    assert len(coordinates) == len(set(coordinates))


def test_npcs_only_spawn_on_ground():
    world = World(TEST_MAP)
    world.spawn_npc()
    for npc in world.npcs:
        tile = world.grid[npc.y][npc.x]
        assert tile.terrain.type == "ground"


def test_spawned_tiles_are_no_longer_enterable():
    world = World(TEST_MAP)
    world.spawn_npc()
    for npc in world.npcs:
        tile = world.grid[npc.y][npc.x]
        assert tile.can_enter() is False


def test_spawn_npc_raises_when_not_enough_spawn_tiles():
    too_small_map = [
        ["ground"],
    ]
    world = World(too_small_map)

    with pytest.raises(ValueError):
        world.spawn_npc()
