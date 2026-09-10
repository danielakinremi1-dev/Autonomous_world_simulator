from world_objects.configs import npc_configs
from world_objects.helper_item_configs import item_configs
from typing import TYPE_CHECKING
import random
from collections import deque
from world_objects.items import Item

if TYPE_CHECKING:
    from world_objects.world import World


class NPC:
    def __init__(self, x: int, y: int, npc_type: str, world: "World") -> None:
        if npc_type not in npc_configs:
            raise ValueError("Invalid npc")
        self.x = x
        self.y = y
        self.npc_type = npc_type
        self.world = world
        self.speed = npc_configs[npc_type]["speed"]
        self.health = npc_configs[npc_type]["health"]
        self.emoji = npc_configs[npc_type]["emoji"]
        self.job = npc_configs[npc_type]["job"]
        self.personality = "Cooperative"
        self.view_radius = npc_configs[npc_type]["view_radius"]
        self.hunger = 500
        self.inventory = (npc_configs[npc_type]["inventory"]).copy()
        self.destination = None
        self.current_path = None
        self.home = None
        self.goal = None
        self.sub_goal = None
        self.sleep_ticks = 0
        self.sleep = False
        self.busy_ticks = 0
        self.busy = False
        self.alive = True
        self.crafting_queue = None
        self.buy_queue = []
        self.sell_queue = []
        self.coins = 2000

        # Spawn in homes with NPCs and provide visuals for goals later

    def __str__(self) -> str:
        return f"A {self.npc_type}"

    def get_visual(self) -> str:
        return self.emoji

    # Refactor sell and buy queues by order of importance, handle broken and unusable items and consumbles
    def observe_and_act(self) -> None:
        if self.alive:
            self.hunger -= 1

            if self.sleep == True:
                if self.sleep_ticks == 0:
                    self.sleep = False
                else:
                    self.sleep_ticks -= 1
                    return

            if self.busy == True:
                if self.busy_ticks == 0:
                    self.can_craft(status="Done")
                    self.busy = False
                else:
                    self.busy_ticks -= 1
                    self.hunger -= 2
                    return

            if self.health < ((npc_configs[self.npc_type]["health"]) * 0.7):
                self.handle_health()
            elif self.hunger <= 100:
                self.handle_hunger()

            elif self.destination != None and self.goal != None:
                self.travel_to_destination()

            elif self.health < ((npc_configs[self.npc_type]["health"]) * 0.9):
                self.handle_health()
            elif self.hunger <= 250:
                self.handle_hunger()

            else:
                self.default_action()

    def pathfind(self) -> bool:
        if self.destination == None:
            return False
        # could also update to only check static objects for blockage
        destination = self.destination
        start_coord = (self.x, self.y)
        visited = {start_coord}
        queue = deque([start_coord])
        path_history = {}
        tiles = self.world.grid

        path_history[start_coord] = None

        if destination == start_coord:
            self.arrived()
            return False

        while queue:
            current_coord = queue.popleft()
            valid_directions = []

            if current_coord[1] != 0:
                up = (current_coord[0], current_coord[1] - 1)
                if up not in visited and tiles[up[1]][up[0]].can_enter():
                    valid_directions.append(up)

            if current_coord[1] != self.world.rows - 1:
                down = (current_coord[0], current_coord[1] + 1)
                if down not in visited and tiles[down[1]][down[0]].can_enter():
                    valid_directions.append(down)

            if current_coord[0] != 0:
                left = (current_coord[0] - 1, current_coord[1])
                if left not in visited and tiles[left[1]][left[0]].can_enter():
                    valid_directions.append(left)

            if current_coord[0] != self.world.row_len - 1:
                right = (current_coord[0] + 1, current_coord[1])
                if right not in visited and tiles[right[1]][right[0]].can_enter():
                    valid_directions.append(right)

            for direction in valid_directions:
                queue.append(direction)
                visited.add(direction)
                path_history[direction] = current_coord
                if self.is_at_destination(direction):
                    return self.traceback(direction, path_history)
        return False

    def traceback(
        self, destination: tuple[int, int], pathing: dict[tuple[int, int]]
    ) -> bool:
        current_coord = destination
        path = []
        while pathing[current_coord] != None:
            path.append(current_coord)
            current_coord = pathing[current_coord]
        self.current_path = path[::-1]
        return True

    def handle_health(self) -> None:
        if self.inventory["bandages"] and self.inventory["bandages"].quantity > 0:
            self.health = npc_configs[self.npc_type]["health"]
            self.inventory["bandages"].quantity -= 1
            return

        if self.goal != "Heal":
            self.goal = "Heal"

            if self.world.find_nurse() != None:
                self.confirm_destination(self.world.find_nurse())
                self.sub_goal = "Find nurse"
                self.buy_queue.append(Item("bandages"))
                self.buy_queue.append(Item("bandages"))
            elif self.home != None:
                self.confirm_destination(self.home)
                self.sub_goal = "Get home"
            else:
                self.goal = None
                return

        self.travel_to_destination()

    def handle_hunger(self) -> None:
        if self.inventory["food"] and self.inventory["food"].quantity > 0:
            self.hunger = 500
            self.inventory["food"].quantity -= 1
            return

        if self.goal != "Eat":
            self.goal = "Eat"

            if self.world.find_baker() != None:
                self.confirm_destination(self.world.find_baker())
                self.sub_goal = "Find baker"
                self.buy_queue.append(Item("food"))
                self.buy_queue.append(Item("food"))
            elif self.home != None:
                self.confirm_destination(self.home)
                self.sub_goal = "Get home"
            else:
                self.goal = None
                return

        self.travel_to_destination()

    def default_action(self) -> None:

        if self.npc_type == "villager":
            self.goal = "Gather resources"
            self.gather_resources()

        elif self.npc_type == "blacksmith":
            self.goal = "Manage smithing station"
            self.smith_and_craft()

        elif self.npc_type == "nurse":
            self.goal = "Manage infirmary"
            self.heal_and_bandage()

        elif self.npc_type == "baker":
            self.goal = "Manage bakery"
            self.cook_and_bake()

        elif self.npc_type == "hunter":
            self.goal = "Hunt and gather"
            self.hunt_and_loot()

        else:
            self.wander()

    def gather_resources(self):
        self.hunger -= 1
        map_data = self.world.npc_worldview(self)
        visible_tiles = map_data["minimap"]
        target_terrain = None

        target_tiles = []
        routes = []
        final_route = None

        # Can check if resource low first with helper method, otherwise skip
        if not self.inventory["wood"] or self.inventory["wood"].quantity < 3:
            target_terrain = "tree"
            self.sub_goal = "Gather wood"
        elif not self.inventory["herbs"] or self.inventory["herbs"].quantity < 3:
            target_terrain = "plant"
            self.sub_goal = "Gather herbs"
        elif not self.inventory["water"] or self.inventory["water"].quantity < 3:
            target_terrain = "water"
            self.sub_goal = "Gather water"
        elif not self.inventory["stone"] or self.inventory["stone"].quantity < 3:
            target_terrain = "rock"
            self.sub_goal = "Gather stones"
        elif not self.inventory["wheat"] or self.inventory["wheat"].quantity < 3:
            target_terrain = "wheat"
            self.sub_goal = "Gather wheat"
        else:
            trading_items = [
                self.inventory["wood"],
                self.inventory["herbs"],
                self.inventory["water"],
                self.inventory["stone"],
                self.inventory["wheat"],
            ]
            self.sell_queue.extend(trading_items)
            self.trade_and_sell()
            return

        for row in visible_tiles:
            for tile in row:
                if tile.terrain.type == target_terrain:
                    target_tiles.append(tile)

        for tile in target_tiles:
            self.confirm_destination((tile.x, tile.y))
            if self.pathfind():
                routes.append(self.current_path)

        if routes:
            final_route = routes[0]
            for route in routes:
                if len(route) < len(final_route):
                    final_route = route

        if final_route == None:
            self.wander()
        else:
            self.current_path = final_route
            self.destination = final_route[-1]
            self.move(self.current_path.pop(0))

    # Ensure homes spawn in and blacksmith has default start mats, method for checking inventory and resources
    def smith_and_craft(self, request=None):
        self.confirm_destination(self.home)
        if not self.is_at_destination():
            self.travel_to_destination()
            return

        if (
            not self.inventory["smithing hammer"]
            or self.inventory["smithing hammer"].quantity < 2
        ):
            self.can_craft("smithing hammer")
        elif request:
            self.can_craft(request)

        elif not self.inventory["pickaxe"] or self.inventory["pickaxe"].quantity < 2:
            self.can_craft("pickaxe")
        elif not self.inventory["axe"] or self.inventory["axe"].quantity < 2:
            self.can_craft("axe")

        elif (
            not self.inventory["medical equipment"]
            or self.inventory["medical equipment"] < 1
        ):
            self.can_craft("medical equipment")
        elif (
            not self.inventory["cooking utensils"]
            or self.inventory["cooking utensils"].quantity < 1
        ):
            self.self.can_craft("cooking utensils")

        elif not self.inventory["bow"] or self.inventory["bow"] < 2:
            self.can_craft("bow")
        elif not self.inventory["sword"] or self.inventory["sword"] < 2:
            self.can_craft("sword")
        elif not self.inventory["armor"] or self.inventory["armor"] < 2:
            self.can_craft("armor")

        else:
            raise ValueError("Invalid crafting input")

    def heal_and_bandage(self):

        if (
            not self.inventory["medical equipment"]
            or not self.inventory["medical equipment"].usable
        ):
            self.goal = "Repair items at blacksmith"
            self.sub_goal = "Replace broken medical equipment"
            self.confirm_destination(self.world.find_blacksmith())
            if not self.is_at_destination():
                self.travel_to_destination()

        self.confirm_destination(self.home)
        if not self.is_at_destination():
            self.travel_to_destination()
            return

        elif not self.inventory["bandages"] or self.inventory["bandages"].quantity < 4:
            can_craft = self.can_craft("bandages")
            if not can_craft:
                self.wait_for_resources()

    def cook_and_bake(self):
        if (
            not self.inventory["cooking utensils"]
            or not self.inventory["cooking utensils"].usable
        ):
            self.goal = "Repair items at blacksmith"
            self.sub_goal = "Replace broken cooking utensils"
            self.confirm_destination(self.world.find_blacksmith())
            if not self.is_at_destination():
                self.travel_to_destination()
                return

        self.confirm_destination(self.home)
        if not self.is_at_destination():
            self.travel_to_destination()
            return

        if self.inventory["food"].quantity < 2:
            can_craft = self.can_craft("food")
            if not can_craft:
                self.wait_for_resources()

    def hunt_and_loot(self):
        if self.inventory["herbs"] and self.inventory["herbs"].quantity > 5:
            self.sell_queue.append(self.inventory["herbs"])
        if self.inventory["water"] and self.inventory["water"].quantity > 5:
            self.sell_queue.append(self.inventory["water"])
        if self.inventory["stone"] and self.inventory["stone"].quantity > 5:
            self.sell_queue.append(self.inventory["stone"])
        if self.inventory["wheat"] and self.inventory["wheat"].quantity > 5:
            self.sell_queue.append(self.inventory["wheat"])
        if self.inventory["wood"] and self.inventory["wood"].quantity > 5:
            self.sell_queue.append(self.inventory["wood"])
        if self.sell_queue:
            self.trade_and_sell()
            return

        if self.sub_goal != "Leaving village":
            self.sub_goal = "Leaving village"
            self.hunger -= 1
            map_data = self.world.world_edges()
            minimap = map_data["world_map"]
            upper_left = map_data["upper_left"]
            lower_right = map_data["lower_right"]
            outer_tiles_coord = []
            hunting_paths = []

            for row in minimap:
                for tile in row:
                    if (
                        tile.x == (upper_left[0])
                        or tile.x == lower_right[0]
                        or tile.y == (upper_left[1])
                        or tile.y == lower_right[1]
                    ) and (tile.can_enter()):
                        outer_tiles_coord.append((tile.x, tile.y))

            for outer_tile in outer_tiles_coord:
                self.confirm_destination(outer_tile)
                if self.pathfind():
                    hunting_paths.append(self.current_path)

            if hunting_paths:
                final_route = random.choice(hunting_paths)
                self.destination = final_route[-1]
                self.current_path = final_route
                self.move(self.current_path.pop(0))
        if self.is_at_destination():
            self.world.despawn_and_respawn(self)

    # Sort by importance of items
    def buy_and_sell(self):
        go_home_after = False

        if self.buy_queue:
            item = self.buy_queue[0]
            match item.item_type:
                case (
                    "medical equipment"
                    | "armor"
                    | "damage"
                    | "mining"
                    | "logging"
                    | "cooking equipment"
                ):
                    target = self.world.interact_blacksmith()
                    self.confirm_destination(self.world.find_blacksmith())
                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return
                case "satiation":
                    target = self.world.interact_baker()
                    self.confirm_destination(self.world.find_baker())
                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return

                case "healing":
                    target = self.world.interact_nurse()
                    self.confirm_destination(self.world.find_nurse())
                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return
                case _:
                    raise ValueError("Invalid item type")

            self.trade(target, "Buy")
            if self.buy_queue:
                go_home_after = True

        if self.sell_queue:
            item = self.sell_queue[0]
            match item.item_type:
                case (
                    "medical equipment"
                    | "armor"
                    | "damage"
                    | "mining"
                    | "logging"
                    | "cooking equipment"
                    | "stone"
                ):
                    target = self.world.interact_blacksmith()
                    self.confirm_destination(self.world.find_blacksmith())
                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return
                case "wood" | "water":
                    potential_targets = [
                        (
                            self.world.interact_blacksmith(),
                            self.world.find_blacksmith(),
                        ),
                        (self.world.interact_baker(), self.world.find_baker()),
                        (self.world.interact_nurse(), self.world.find_nurse()),
                    ]
                    target_details = random.choice(potential_targets)
                    target = target_details[0]
                    self.confirm_destination(target_details[1])

                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return
                case "herbs":
                    target = self.world.interact_nurse()
                    self.confirm_destination(self.world.find_nurse())
                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return
                case "wheat":
                    target = self.world.interact_baker()
                    self.confirm_destination(self.world.find_baker())
                    if not self.is_at_destination():
                        self.travel_to_destination()
                        return
                case _:
                    raise ValueError("Invalid item type")

            self.trade(target, "Sell")
            if self.sell_queue:
                go_home_after = True

        if go_home_after:
            self.goal = "Rest"
            self.confirm_destination(self.home)

    def trade(self, target_npc, action):
        if action == "Buy":
            bought = []
            for item in self.buy_queue:
                target_item = target_npc.inventory[item.item_name]
                if target_item and target_item.quantity > 0:
                    price = target_item.sell_price
                    if self.coins >= price:
                        if self.inventory[item.item_name]:
                            if target_npc.inventory[item.item_name].quantity == 1:
                                new_item = target_npc.inventory.pop(item.item_name)
                            else:
                                target_npc.inventory[item.item_name].quantity -= 1
                                new_item = Item(item.item_name)
                            previous_quanity = self.inventory[item.item_name].quantity
                            new_item.quantity += previous_quanity
                            self.inventory[item.item_name] = new_item
                        else:
                            if target_npc.inventory[item.item_name].quantity == 1:
                                new_item = target_npc.inventory.pop(item.item_name)
                            else:
                                target_npc.inventory[item.item_name].quantity -= 1
                                new_item = Item(item.item_name)
                            self.inventory[item.item_name] = new_item

                        target_npc.coins += price
                        self.coins -= price
                        bought.append(item)
            for item in bought:
                self.buy_queue.remove(item)

        elif action == "Sell":
            sold = []
            for item in self.sell_queue:
                target_item = self.inventory[item.item_name]
                if target_item and target_item.quantity > 0:
                    price = target_item.sell_price
                    if not target_item.usable or (
                        target_item.durability
                        < item_configs[target_item.item_name]["durability"]
                    ):
                        price = price // 3
                        target_npc.busy_ticks += 20
                        target_npc.busy = True
                    if target_npc.coins >= price:
                        if target_npc.inventory[item.item_name]:
                            new_item = self.inventory.pop(item.item_name)
                            previous_quanity = target_npc.inventory[
                                item.item_name
                            ].quantity
                            new_item.quantity += previous_quanity
                            target_npc.inventory[item.item_name] = new_item
                        else:
                            target_npc.inventory[item.item_name] = self.inventory.pop(
                                item.item_name
                            )

                        target_npc.coins -= price
                        self.coins += price
                        sold.append(item)
            for item in sold:
                self.sell_queue.remove(item)
        else:
            raise ValueError("Invalid trading action")

    def can_craft(self, item_name=None, status="Start"):
        if status == "Start" and item_name:
            self.crafting_queue = Item(item_name)

            materials_used = self.crafting_queue.craft_materials
            for key, value in materials_used.items():
                material_cost = value
                current_amount = self.inventory[key].quantity
                if current_amount - material_cost < 0:
                    self.crafting_queue = None
                    return False

            for key, value in materials_used.items():
                self.inventory[key].quantity -= value

            self.sub_goal = f"Crafting {item_name}"
            self.busy = True
            self.busy_ticks = self.crafting_queue.craft_time

            if self.npc_type == "blacksmith":
                self.inventory["smithing hammer"].use()

            if self.npc_type == "baker":
                self.inventory["cooking utensils"].use()

            if self.npc_type == "nurse":
                self.inventory["medical equipment"].use()

            return True

        elif status == "Done":
            self.add_to_inventory(self, self.crafting_queue)
            self.crafting_queue = []

    def wait_for_resources(self):
        pass

    # Ensure all inventory slots have proper item class allocation to avoid quantity access error
    def add_to_inventory(self, npc, item):
        if npc.inventory[item.item_name]:
            npc.inventory[item.item_name].quantity += 1
            return
        npc.inventory[item.item_name] = item

    # maybe a lesser hunt for villagers, wander and hunt use similar logic for edges

    def arrived(self):
        if self.destination == self.home:
            # could add helper methods for eat and heal with optional arguments of sleep and inventory, rename heal
            if self.goal == "Eat":
                self.hunger = 500 * 0.85
                self.sleep = True
                self.sleep_ticks = 15
            if self.goal == "Heal":
                self.health = (npc_configs[self.npc_type]["health"]) * 0.85
                self.sleep = True
                self.sleep_ticks = 15
            if self.goal == "Rest":
                self.sleep = True
                self.sleep_ticks = 12
            if self.goal == "Manage smithing station":
                self.smith_and_craft()
            if self.goal == "Manage infirmary":
                self.heal_and_bandage()
            if self.goal == "Manage bakery":
                self.cook_and_bake()

        if self.destination == self.world.find_baker():
            self.buy_and_sell()

        if self.destination == self.world.find_nurse():
            self.buy_and_sell()

        if self.destination == self.world.find_blacksmith():
            self.buy_and_sell()

        if self.goal == "Gather resources":
            self.world.get_resource(self, self.destination, self.sub_goal)

        self.destination = None
        self.current_path = None
        self.goal = None
        self.sub_goal = None

    def wander(self) -> None:
        minimap_data = self.world.npc_worldview(self)
        minimap = minimap_data["minimap"]
        upper_left = minimap_data["upper_left"]
        lower_right = minimap_data["lower_right"]
        outer_tiles_coord = []
        wandering_paths = []

        for row in minimap:
            for tile in row:
                if (
                    tile.x == (upper_left[0])
                    or tile.x == lower_right[0]
                    or tile.y == (upper_left[1])
                    or tile.y == lower_right[1]
                ) and (tile.can_enter()):
                    outer_tiles_coord.append((tile.x, tile.y))

        for outer_tile in outer_tiles_coord:
            self.confirm_destination(outer_tile)
            if self.pathfind():
                wandering_paths.append(self.current_path)

        if wandering_paths:
            final_route = random.choice(wandering_paths)
            self.destination = final_route[-1]
            self.current_path = final_route
            self.move(self.current_path.pop(0))

    def move(self, coord: tuple[int, int]) -> bool:
        self.hunger -= 2
        move = self.world.move_npc(self, coord)
        if self.destination and self.is_at_destination():
            self.arrived()
        return move

    def travel_to_destination(self):
        if self.is_at_destination():
            self.arrived()
            return

        if self.current_path != None and len(self.current_path) > 0:
            can_move = self.move(self.current_path.pop(0))
            if not can_move:
                self.current_path = None
            return

        can_find = self.pathfind()
        if can_find:
            can_move = self.move(self.current_path.pop(0))
            if not can_move:
                self.current_path = None

    def confirm_destination(self, new_dest: tuple[int, int]) -> None:
        if self.destination != new_dest:
            self.destination = new_dest
            self.current_path = None

    def is_at_destination(self, checked_tile: tuple[int, int] | None = None) -> bool:
        if checked_tile == None:
            checked_tile = (self.x, self.y)

        if self.destination != None:
            if (
                abs(self.destination[0] - checked_tile[0]) <= 1
                and abs(self.destination[1] - checked_tile[1]) <= 1
            ):
                return True
        return False

    def get_hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.emoji = "❌"
