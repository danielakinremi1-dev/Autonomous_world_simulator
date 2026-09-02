import pytest

from world_objects.constants import DEFAULT_MAP
from world_objects.world import World
from world_objects.configs import npc_configs


def make_world():
    return World([
        ["ground", "ground", "ground"],
        ["ground", "ground", "tree"],
        ["ground", "ground", "ground"],
    ])


def make_open_world():
    return World([
        ["ground", "ground", "ground"],
        ["ground", "ground", "ground"],
        ["ground", "ground", "ground"],
    ])


# WORLD CREATION





def test_world():
    world = World(DEFAULT_MAP)

    assert world.row_len == 20
    assert world.rows == 15
    assert str(world) == "A 20 by 15 simulated world!"


# NPC SPAWNING


def test_spawn_npc_creates_all_configured_npcs():
    world = make_world()

    world.spawn_npc()

    assert len(world.npcs) == len(npc_configs)


def test_spawned_npcs_are_on_their_tiles():
    world = make_world()

    world.spawn_npc()

    for npc in world.npcs:
        assert world.grid[npc.y][npc.x].occupant is npc


def test_spawned_npcs_have_unique_coordinates():
    world = make_world()

    world.spawn_npc()

    coordinates = [(npc.x, npc.y) for npc in world.npcs]

    assert len(coordinates) == len(set(coordinates))


def test_npcs_only_spawn_on_ground():
    world = make_world()

    world.spawn_npc()

    for npc in world.npcs:
        assert world.grid[npc.y][npc.x].terrain.type == "ground"


def test_spawned_tiles_are_no_longer_enterable():
    world = make_world()

    world.spawn_npc()

    for npc in world.npcs:
        assert world.grid[npc.y][npc.x].can_enter() is False


def test_spawn_npc_raises_when_not_enough_spawn_tiles():
    world = World([
        ["ground"],
    ])

    with pytest.raises(ValueError):
        world.spawn_npc()


# PLACE NPC


def test_place_npc():
    world = make_open_world()

    npc = world.place_npc(1, 1)

    assert npc.x == 1
    assert npc.y == 1
    assert npc.npc_type == "villager"

    assert world.grid[1][1].occupant is npc
    assert npc in world.npcs


@pytest.mark.parametrize(
    "x, y",
    [
        (-1, 1),
        (1, -1),
        (3, 1),
        (1, 3),
    ],
)
def test_place_npc_out_of_bounds(x, y):
    world = make_open_world()

    with pytest.raises(ValueError):
        world.place_npc(x, y)


def test_place_npc_on_blocked_terrain():
    world = make_world()

    with pytest.raises(ValueError):
        world.place_npc(2, 1)


def test_place_npc_on_occupied_tile():
    world = make_open_world()

    world.place_npc(1, 1)

    with pytest.raises(ValueError):
        world.place_npc(1, 1)


# NPC MOVEMENT


def test_move_npc_success():
    world = make_open_world()
    npc = world.place_npc(1, 1)

    result = npc.move((0, 1))

    assert result is True

    assert (npc.x, npc.y) == (0, 1)

    assert world.grid[1][0].occupant is npc
    assert world.grid[1][1].occupant is None


def test_move_npc_into_occupied_tile():
    world = make_open_world()

    npc_one = world.place_npc(1, 1)
    npc_two = world.place_npc(0, 1)

    result = npc_one.move((0, 1))

    assert result is False

    assert (npc_one.x, npc_one.y) == (1, 1)

    assert world.grid[1][1].occupant is npc_one
    assert world.grid[1][0].occupant is npc_two


def test_move_npc_into_untraversable_tile():
    world = make_world()
    npc = world.place_npc(1, 1)

    result = npc.move((2, 1))

    assert result is False

    assert (npc.x, npc.y) == (1, 1)

    assert world.grid[1][1].occupant is npc
    assert world.grid[1][2].occupant is None


@pytest.mark.parametrize(
    "x, y, requested_coord",
    [
        (0, 1, (-1, 1)),
        (2, 1, (3, 1)),
        (1, 0, (1, -1)),
        (1, 2, (1, 3)),
    ],
)
def test_move_npc_out_of_bounds(x, y, requested_coord):
    world = make_open_world()
    npc = world.place_npc(x, y)

    result = npc.move(requested_coord)

    assert result is False
    assert (npc.x, npc.y) == (x, y)
    assert world.grid[y][x].occupant is npc


@pytest.mark.parametrize(
    "requested_coord",
    [
        (2, 2),   # diagonal from (1, 1)
        (0, 0),   # diagonal from (1, 1)
        (1, 3),   # jumps two tiles down
        (3, 1),   # jumps two tiles right
    ],
)
def test_move_npc_rejects_invalid_movement(requested_coord):
    world = World([
        ["ground", "ground", "ground", "ground"],
        ["ground", "ground", "ground", "ground"],
        ["ground", "ground", "ground", "ground"],
        ["ground", "ground", "ground", "ground"],
    ])

    npc = world.place_npc(1, 1)

    with pytest.raises(ValueError):
        npc.move(requested_coord)