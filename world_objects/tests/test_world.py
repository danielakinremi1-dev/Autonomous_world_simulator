from world_objects.constants import DEFAULT_MAP
from world_objects.world import World
from world_objects.npc import NPC
from world_objects.configs import npc_configs
import pytest



def test_world():
    new_world = World(DEFAULT_MAP)
    placeholder = [['🟩', '🟩', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🌊', '🌊', '🌊', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🌊', '🌊', '🌊', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌊', '🌊', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🌊', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🌳', '🌳'], ['🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩'], ['🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩'], ['🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟫', '🟫', '🟫', '🟫', '🟫', '🟫', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🌳', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🌳', '🟩', '🟩'], ['🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩', '🌳', '🟩', '🟩', '🟩', '🟩', '🟩', '🟩']]
    assert new_world.get_render_data() == placeholder
    assert str(new_world) == "A 20 by 15 simulated world!" 




def make_world():
    return World([
        ["ground", "ground", "ground"],
        ["ground", "ground", "tree"],
        ["ground", "ground", "ground"],
    ])


def test_spawn_npc_creates_all_configured_npcs():
    world = make_world()
    world.spawn_npc()
    assert len(world.npcs) == len(npc_configs)


def test_spawned_npcs_are_on_their_tiles():
    world = make_world()
    world.spawn_npc()
    for npc in world.npcs:
        tile = world.grid[npc.y][npc.x]
        assert tile.occupant is npc


def test_spawned_npcs_have_unique_coordinates():
    world = make_world()
    world.spawn_npc()
    coordinates = [(npc.x, npc.y) for npc in world.npcs]
    assert len(coordinates) == len(set(coordinates))


def test_npcs_only_spawn_on_ground():
    world = make_world()
    world.spawn_npc()
    for npc in world.npcs:
        tile = world.grid[npc.y][npc.x]
        assert tile.terrain.type == "ground"


def test_spawned_tiles_are_no_longer_enterable():
    world = make_world()
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




#NPC movement

def place_npc(world, x=1, y=1):
    npc = NPC(x, y, "villager", world)
    world.grid[y][x].occupant = npc
    world.npcs.append(npc)
    return npc


def test_move_npc_success():
    world = make_world()
    npc = place_npc(world, 1, 1)

    result = npc.move("left")

    assert result is True

    assert npc.x == 0
    assert npc.y == 1

    assert world.grid[1][0].occupant is npc
    assert world.grid[1][1].occupant is None


def test_move_npc_invalid_direction():
    world = make_world()
    npc = place_npc(world)

    with pytest.raises(ValueError):
        npc.move("diagonal")


def test_move_npc_into_occupied_tile():
    world = make_world()

    npc_one = place_npc(world, 1, 1)
    npc_two = place_npc(world, 0, 1)

    result = npc_one.move("left")

    assert result is False

    assert npc_one.x == 1
    assert npc_one.y == 1

    assert world.grid[1][1].occupant is npc_one
    assert world.grid[1][0].occupant is npc_two


def test_move_npc_into_untraversable_tile():
    world = make_world()
    npc = place_npc(world, 1, 1)

    result = npc.move("right")

    assert result is False

    assert npc.x == 1
    assert npc.y == 1

    assert world.grid[1][1].occupant is npc
    assert world.grid[1][2].occupant is None


@pytest.mark.parametrize(
    "x, y, direction",
    [
        (0, 1, "left"),
        (2, 1, "right"),
        (1, 0, "up"),
        (1, 2, "down"),
    ],
)
def test_move_npc_out_of_bounds(x, y, direction):
    world = World([
        ["ground", "ground", "ground"],
        ["ground", "ground", "ground"],
        ["ground", "ground", "ground"],
    ])

    npc = place_npc(world, x, y)

    result = npc.move(direction)

    assert result is False

    assert npc.x == x
    assert npc.y == y
    assert world.grid[y][x].occupant is npc