import pytest

from world_objects.world import World
from world_objects.npc import NPC
from world_objects.items import Item
from world_objects.configs import npc_configs, item_configs


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


@pytest.mark.parametrize(
    "npc_type, expected_goal, method_name",
    [
        ("villager", "Gather resources", "gather_resources"),
        ("blacksmith", "Manage smithing station", "smith_and_craft"),
        ("nurse", "Manage infirmary", "heal_and_bandage"),
        ("baker", "Manage bakery", "cook_and_bake"),
        ("hunter", "Hunt and gather", "hunt_and_loot"),
    ],
)
def test_default_action_calls_correct_role_behavior(
    npc_type, expected_goal, method_name, monkeypatch
):
    world = make_open_world()
    npc = world.place_npc(2, 2, npc_type)

    calls = []

    def fake_action(*args, **kwargs):
        calls.append(method_name)

    monkeypatch.setattr(npc, method_name, fake_action)

    npc.default_action()

    assert npc.goal == expected_goal
    assert calls == [method_name]


def test_default_action_only_runs_one_role_behavior():
    world = make_open_world()
    npc = world.place_npc(2, 2, "villager")

    calls = []

    npc.gather_resources = lambda: calls.append("gather")
    npc.smith_and_craft = lambda: calls.append("smith")
    npc.heal_and_bandage = lambda: calls.append("heal")
    npc.cook_and_bake = lambda: calls.append("bake")
    npc.hunt_and_loot = lambda: calls.append("hunt")
    npc.wander = lambda: calls.append("wander")

    npc.default_action()

    assert calls == ["gather"]


def test_default_action_falls_back_to_wander():
    world = make_open_world()
    npc = world.place_npc(2, 2, "villager")

    npc.npc_type = "unknown"

    calls = []
    npc.wander = lambda: calls.append("wander")

    npc.default_action()

    assert calls == ["wander"]


def test_same_type_npcs_have_independent_inventories(world):
    npc1 = world.place_npc(1, 1, "villager")
    npc2 = world.place_npc(3, 3, "villager")

    starting_npc2_food = npc2.inventory["food"].quantity

    npc1.inventory["food"].quantity -= 1

    assert npc2.inventory["food"].quantity == starting_npc2_food
    assert npc1.inventory is not npc2.inventory
    assert npc1.inventory["food"] is not npc2.inventory["food"]


def test_item_uses_config_values():
    axe = Item("axe")

    assert axe.item_name == "axe"
    assert axe.durability == item_configs["axe"]["durability"]
    assert axe.craft_time == item_configs["axe"]["craft time"]
    assert axe.craft_materials == item_configs["axe"]["craft materials"]
    assert axe.sell_price == item_configs["axe"]["price"]


def test_item_quantity_is_set():
    food = Item("food", 4)

    assert food.quantity == 4


def test_using_tool_reduces_durability():
    axe = Item("axe")

    starting_durability = axe.durability

    axe.use()

    assert axe.durability == starting_durability - 1


def test_tool_becomes_unusable_when_last_copy_breaks():
    axe = Item("axe", 1)

    axe.durability = 1

    axe.use()

    assert axe.quantity == 0
    assert axe.usable is False


def test_next_tool_becomes_available_when_stack_has_more():
    axe = Item("axe", 2)
    axe.durability = 1

    axe.use()

    assert axe.quantity == 1
    assert axe.usable is True
    assert axe.durability > 0


def test_gather_wood_uses_axe_and_adds_wood(world):
    npc = world.place_npc(2, 2, "villager")

    world.grid[2][3].terrain = world.grid[2][3].terrain.__class__("tree")

    npc.inventory["wood"] = Item("wood", 0)

    starting_durability = npc.inventory["axe"].durability
    starting_hp = world.grid[2][3].terrain.hp

    world.get_resource(npc, (3, 2), "Gather wood")

    assert npc.inventory["wood"].quantity == 1
    assert npc.inventory["axe"].durability == starting_durability - 1
    assert world.grid[2][3].terrain.hp == starting_hp - 1


def test_gather_stone_requires_pickaxe(world):
    npc = world.place_npc(2, 2, "villager")

    from world_objects.terrain import Terrain

    world.grid[2][3].terrain = Terrain("rock")
    npc.inventory["stone"] = Item("stone", 0)

    npc.inventory["pickaxe"].usable = False

    world.get_resource(npc, (3, 2), "Gather stones")

    assert npc.inventory["stone"].quantity == 0


def test_gather_herbs_does_not_require_tool(world):
    npc = world.place_npc(2, 2, "villager")

    from world_objects.terrain import Terrain

    world.grid[2][3].terrain = Terrain("plant")
    npc.inventory["herbs"] = Item("herbs", 0)

    world.get_resource(npc, (3, 2), "Gather herbs")

    assert npc.inventory["herbs"].quantity == 1


def test_depleted_plant_becomes_grass(world):
    npc = world.place_npc(2, 2, "villager")

    from world_objects.terrain import Terrain

    world.grid[2][3].terrain = Terrain("plant")
    world.grid[2][3].terrain.hp = 1

    npc.inventory["herbs"] = Item("herbs", 0)

    world.get_resource(npc, (3, 2), "Gather herbs")

    assert world.grid[2][3].terrain.type == "grass"


def test_depleted_tree_becomes_ground(world):
    npc = world.place_npc(2, 2, "villager")

    from world_objects.terrain import Terrain

    world.grid[2][3].terrain = Terrain("tree")
    world.grid[2][3].terrain.hp = 1

    npc.inventory["wood"] = Item("wood", 0)

    world.get_resource(npc, (3, 2), "Gather wood")

    assert world.grid[2][3].terrain.type == "ground"


def give_crafting_resources(npc, amount=100):
    for resource in ["wood", "stone", "water", "herbs", "wheat"]:
        npc.inventory[resource] = Item(resource, amount)


def test_can_craft_starts_crafting(world):
    blacksmith = world.place_npc(2, 2, "blacksmith")

    give_crafting_resources(blacksmith)

    result = blacksmith.can_craft("axe")

    assert result is True
    assert blacksmith.busy is True
    assert blacksmith.crafting_queue is not None
    assert blacksmith.crafting_queue.item_name == "axe"
    assert blacksmith.busy_ticks == item_configs["axe"]["craft time"]


def test_crafting_deducts_correct_materials(world):
    blacksmith = world.place_npc(2, 2, "blacksmith")

    give_crafting_resources(blacksmith)

    wood_before = blacksmith.inventory["wood"].quantity
    stone_before = blacksmith.inventory["stone"].quantity
    water_before = blacksmith.inventory["water"].quantity

    blacksmith.can_craft("axe")

    recipe = item_configs["axe"]["craft materials"]

    assert blacksmith.inventory["wood"].quantity == wood_before - recipe["wood"]
    assert blacksmith.inventory["stone"].quantity == stone_before - recipe["stone"]
    assert blacksmith.inventory["water"].quantity == water_before - recipe["water"]


def test_failed_craft_does_not_consume_any_materials(world):
    blacksmith = world.place_npc(2, 2, "blacksmith")

    blacksmith.inventory["wood"] = Item("wood", 100)
    blacksmith.inventory["stone"] = Item("stone", 100)
    blacksmith.inventory["water"] = Item("water", 0)

    wood_before = blacksmith.inventory["wood"].quantity
    stone_before = blacksmith.inventory["stone"].quantity

    result = blacksmith.can_craft("axe")

    assert result is False

    assert blacksmith.inventory["wood"].quantity == wood_before
    assert blacksmith.inventory["stone"].quantity == stone_before

    assert blacksmith.busy is False
    assert blacksmith.crafting_queue is None


def test_finished_craft_enters_inventory(world):
    blacksmith = world.place_npc(2, 2, "blacksmith")

    give_crafting_resources(blacksmith)

    blacksmith.can_craft("axe")

    previous_quantity = blacksmith.inventory["axe"].quantity

    blacksmith.can_craft(status="Done")

    assert blacksmith.inventory["axe"].quantity == previous_quantity + 1


def test_hungry_npc_eats_carried_food(world):
    npc = world.place_npc(2, 2, "villager")

    npc.hunger = 50
    npc.inventory["food"].quantity = 2

    npc.handle_hunger()

    assert npc.hunger == 500
    assert npc.inventory["food"].quantity == 1


def test_injured_npc_uses_bandage(world):
    npc = world.place_npc(2, 2, "villager")

    npc.health = 25
    npc.inventory["bandages"].quantity = 2

    npc.handle_health()

    assert npc.health == npc_configs["villager"]["health"]
    assert npc.inventory["bandages"].quantity == 1


def test_critical_health_has_priority_over_hunger(world, monkeypatch):
    npc = world.place_npc(2, 2, "villager")

    npc.health = 10
    npc.hunger = 10

    calls = []

    monkeypatch.setattr(
        npc,
        "handle_health",
        lambda: calls.append("health"),
    )

    monkeypatch.setattr(
        npc,
        "handle_hunger",
        lambda: calls.append("hunger"),
    )

    npc.observe_and_act()

    assert calls == ["health"]


def test_buying_item_transfers_coins_and_quantity(world):
    buyer = world.place_npc(1, 1, "villager")
    seller = world.place_npc(3, 3, "baker")

    buyer.inventory["food"] = Item("food", 0)
    seller.inventory["food"] = Item("food", 5)

    buyer.buy_queue.append(Item("food"))

    buyer_coins_before = buyer.coins
    seller_coins_before = seller.coins
    price = seller.inventory["food"].sell_price

    buyer.trade(seller, "Buy")

    assert buyer.inventory["food"].quantity == 1
    assert seller.inventory["food"].quantity == 4

    assert buyer.coins == buyer_coins_before - price
    assert seller.coins == seller_coins_before + price

    assert buyer.buy_queue == []


def test_selling_item_transfers_coins_and_inventory(world):
    seller = world.place_npc(1, 1, "villager")
    buyer = world.place_npc(3, 3, "blacksmith")

    seller.inventory["wood"] = Item("wood", 1)
    buyer.inventory["wood"] = Item("wood", 0)

    seller.sell_queue.append(seller.inventory["wood"])

    seller_coins_before = seller.coins
    buyer_coins_before = buyer.coins
    price = seller.inventory["wood"].sell_price

    seller.trade(buyer, "Sell")

    assert buyer.inventory["wood"].quantity == 1

    assert seller.coins == seller_coins_before + price
    assert buyer.coins == buyer_coins_before - price

    assert seller.sell_queue == []


def test_cannot_buy_without_enough_money(world):
    buyer = world.place_npc(1, 1, "villager")
    seller = world.place_npc(3, 3, "baker")

    seller.inventory["food"] = Item("food", 5)

    buyer.coins = 0
    buyer.buy_queue.append(Item("food"))

    seller_quantity_before = seller.inventory["food"].quantity

    buyer.trade(seller, "Buy")

    assert seller.inventory["food"].quantity == seller_quantity_before
    assert buyer.coins == 0


def test_worldview_contains_npc_tile(world):
    npc = world.place_npc(2, 2, "villager")

    view = world.npc_worldview(npc)
    minimap = view["minimap"]

    coords = {(tile.x, tile.y) for row in minimap for tile in row}

    assert (npc.x, npc.y) in coords


def test_worldview_is_clipped_at_world_edge(world):
    npc = world.place_npc(0, 0, "villager")

    view = world.npc_worldview(npc)

    assert view["upper_left"] == (0, 0)


def test_move_updates_both_npc_and_tiles(world):
    npc = world.place_npc(2, 2, "villager")

    result = world.move_npc(npc, (3, 2))

    assert result is True

    assert (npc.x, npc.y) == (3, 2)

    assert world.grid[2][3].occupant is npc
    assert world.grid[2][2].occupant is None


def test_despawn_removes_npc_from_tile(world):
    npc = world.place_npc(2, 2, "hunter")

    tile = world.grid[2][2]

    world.despawn_and_respawn(npc)

    assert tile.occupant is None
    assert world.despawned_npc is npc
    assert world.despawn_ticks == 20


def test_respawn_restores_npc_to_tile(world):
    npc = world.place_npc(2, 2, "hunter")

    world.despawn_and_respawn(npc)

    world.despawn_and_respawn(npc, respawn=True)

    assert world.grid[2][2].occupant is npc


def test_villager_can_gather_resource_then_sell_it(world):
    from world_objects.terrain import Terrain

    villager = world.place_npc(1, 2, "villager")
    blacksmith = world.place_npc(3, 2, "blacksmith")

    villager.inventory["wood"] = Item("wood", 0)

    world.grid[2][2].terrain = Terrain("tree")
    world.grid[2][2].terrain.hp = 1

    world.get_resource(
        villager,
        (2, 2),
        "Gather wood",
    )

    assert villager.inventory["wood"].quantity == 1

    villager.sell_queue.append(villager.inventory["wood"])

    villager.trade(
        blacksmith,
        "Sell",
    )

    assert blacksmith.inventory["wood"].quantity >= 1
    assert villager.sell_queue == []
