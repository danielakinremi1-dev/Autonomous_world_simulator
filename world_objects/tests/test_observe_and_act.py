import pytest

from world_objects.world import World
from world_objects.configs import npc_configs
from world_objects.items import Item


def make_open_world():
    return World(
        [
            ["ground", "ground", "ground", "ground", "ground"],
            ["ground", "ground", "ground", "ground", "ground"],
            ["ground", "ground", "ground", "ground", "ground"],
            ["ground", "ground", "ground", "ground", "ground"],
            ["ground", "ground", "ground", "ground", "ground"],
        ]
    )


def make_wall_world():
    return World(
        [
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "ground", "ground", "ground"],
            ["ground", "ground", "ground", "ground", "ground"],
        ]
    )


def set_item_quantity(npc, item_name, quantity):
    if not npc.inventory[item_name]:
        npc.inventory[item_name] = Item(item_name, quantity)
    else:
        npc.inventory[item_name].quantity = quantity


def test_pathfind_shortest_route_around_wall():
    world = make_wall_world()
    npc = world.place_npc(0, 0)

    npc.destination = (4, 0)
    npc.goal = "Test"

    result = npc.pathfind()

    assert result is True
    assert npc.current_path is not None

    previous = (npc.x, npc.y)

    for coord in npc.current_path:
        distance = abs(coord[0] - previous[0]) + abs(coord[1] - previous[1])

        assert distance == 1
        assert world.grid[coord[1]][coord[0]].terrain.type != "tree"

        previous = coord

    assert npc.is_at_destination(npc.current_path[-1]) is True


def test_npc_arrives_at_destination():
    world = make_wall_world()
    npc = world.place_npc(0, 0)

    npc.destination = (4, 0)
    npc.goal = "Test"

    for _ in range(20):
        if npc.destination is None:
            break

        npc.observe_and_act()

    assert npc.destination is None
    assert npc.goal is None
    assert npc.current_path is None


def test_npc_knows_when_destination_unreachable():
    world = World(
        [
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
        ]
    )

    npc = world.place_npc(0, 2)

    npc.destination = (4, 2)
    npc.goal = "Test"

    starting_position = (npc.x, npc.y)

    result = npc.pathfind()

    assert result is False
    assert (npc.x, npc.y) == starting_position
    assert npc.current_path is None


def test_auto_travel_fails_without_path():
    world = World(
        [
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
            ["ground", "ground", "tree", "ground", "ground"],
        ]
    )

    npc = world.place_npc(0, 2)

    npc.destination = (4, 2)
    npc.goal = "Test"

    npc.travel_to_destination()

    assert (npc.x, npc.y) == (0, 2)


def test_injured_npc_goes_to_nurse_and_buys_bandages():
    world = make_open_world()

    villager = world.place_npc(0, 2, "villager")
    nurse = world.place_npc(4, 2, "nurse")

    villager.health = npc_configs["villager"]["health"] * 0.5
    set_item_quantity(villager, "bandages", 0)

    for _ in range(20):
        villager.observe_and_act()

        if (
            villager.health == npc_configs["villager"]["health"]
            and villager.inventory["bandages"].quantity == 1
        ):
            break

    assert villager.health == npc_configs["villager"]["health"]

    assert villager.inventory["bandages"].quantity == 1

    assert villager.goal is None
    assert villager.destination is None
    assert villager.current_path is None

    assert abs(villager.x - nurse.x) <= 1
    assert abs(villager.y - nurse.y) <= 1


def test_npcs_use_bandages_before_seeking_nurse():
    world = make_open_world()

    villager = world.place_npc(0, 2, "villager")
    world.place_npc(4, 2, "nurse")

    villager.health = npc_configs["villager"]["health"] * 0.5
    set_item_quantity(villager, "bandages", 2)

    villager.observe_and_act()

    assert villager.health == npc_configs["villager"]["health"]
    assert villager.inventory["bandages"].quantity == 1

    assert villager.goal is None
    assert villager.destination is None
    assert villager.buy_queue == []


def test_hungry_npc_goes_to_baker_and_buys_food():
    world = make_open_world()

    villager = world.place_npc(0, 2, "villager")
    baker = world.place_npc(4, 2, "baker")

    villager.hunger = 50
    set_item_quantity(villager, "food", 0)

    for _ in range(20):
        villager.observe_and_act()

        if villager.hunger == 500 and villager.inventory["food"].quantity == 1:
            break

    assert villager.hunger == 500

    # Bought 2, then ate 1.
    assert villager.inventory["food"].quantity == 1

    assert villager.goal is None
    assert villager.destination is None
    assert villager.current_path is None

    assert abs(villager.x - baker.x) <= 1
    assert abs(villager.y - baker.y) <= 1


def test_npcs_use_food_before_seeking_baker():
    world = make_open_world()

    villager = world.place_npc(0, 2, "villager")
    world.place_npc(4, 2, "baker")

    villager.hunger = 50
    set_item_quantity(villager, "food", 2)

    villager.observe_and_act()

    assert villager.hunger == 500
    assert villager.inventory["food"].quantity == 1

    assert villager.goal is None
    assert villager.destination is None
    assert villager.buy_queue == []


def test_npcs_prioritize_critical_health_over_critical_hunger():
    world = make_open_world()

    villager = world.place_npc(0, 2, "villager")
    nurse = world.place_npc(4, 2, "nurse")
    world.place_npc(4, 4, "baker")

    villager.health = npc_configs["villager"]["health"] * 0.5
    villager.hunger = 50

    set_item_quantity(villager, "bandages", 0)
    set_item_quantity(villager, "food", 0)

    villager.observe_and_act()

    assert villager.goal == "Heal"
    assert villager.destination == (nurse.x, nurse.y)

    assert len(villager.buy_queue) == 2
    assert all(item.item_name == "bandages" for item in villager.buy_queue)


def test_arrival_clears_pathfinding():
    world = make_open_world()

    villager = world.place_npc(1, 1, "villager")
    baker = world.place_npc(2, 1, "baker")

    villager.goal = "Test"
    villager.destination = (baker.x, baker.y)
    villager.current_path = [(1, 2), (2, 2)]

    villager.travel_to_destination()

    assert villager.goal is None
    assert villager.destination is None
    assert villager.current_path is None


def test_sleeping_npc_does_not_move():
    world = make_open_world()
    npc = world.place_npc(2, 2)

    npc.sleep = True
    npc.sleep_ticks = 3

    starting_position = (npc.x, npc.y)

    npc.observe_and_act()

    assert (npc.x, npc.y) == starting_position
    assert npc.sleep_ticks == 2
    assert npc.sleep is True


def test_npc_wakes_when_sleep_clears():
    world = make_open_world()
    npc = world.place_npc(2, 2)

    npc.sleep = True
    npc.sleep_ticks = 0

    npc.observe_and_act()

    assert npc.sleep is False


def test_blocked_pathing_is_cleared():
    world = make_open_world()

    traveler = world.place_npc(0, 2)
    blocker = world.place_npc(1, 2)

    traveler.destination = (4, 2)
    traveler.goal = "Test"
    traveler.current_path = [(1, 2), (2, 2), (3, 2)]

    traveler.travel_to_destination()

    assert (traveler.x, traveler.y) == (0, 2)
    assert traveler.current_path is None

    assert world.grid[2][1].occupant is blocker
