from world_objects.configs import npc_configs, direction_configs
from typing import TYPE_CHECKING
import random
from collections import deque
from items import Item
if TYPE_CHECKING:
    from world_objects.world import World

class NPC():
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
        self.inventory = npc_configs[npc_type]["inventory"]
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
        
        #Spawn in homes with NPCs and provide visuals for goals later 


    def __str__(self) -> str:
        return f"A {self.npc_type}"
    
    def get_visual(self) -> str:
         return self.emoji


#Refactor order by importance, handle broken items
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
                    self.can_craft(status = "Done")
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

    def pathfind(self)-> bool: 
        if self.destination == None:
            return False
        #could also update to only check static objects for blockage
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
    
            
    def traceback(self, destination: tuple[int,int], pathing: dict[tuple[int,int]]) -> bool:
        current_coord = destination
        path = []
        while pathing[current_coord] != None:
            path.append(current_coord)
            current_coord = pathing[current_coord]
        self.current_path = path[::-1]
        return True
        
 


    def handle_health(self) -> None:
        if self.inventory["bandages"] > 0:
            self.health = npc_configs[self.npc_type]["health"]
            self.inventory["bandages"] -= 1
            return
        
        if self.goal != "Heal":
            self.goal = "Heal"

            if self.world.find_nurse() != None:
                self.confirm_destination(self.world.find_nurse())
                self.sub_goal = "Find nurse"
            elif self.home != None:
                self.confirm_destination(self.home)
                self.sub_goal = "Get home"
            else:
                self.goal = None
                return
            
        self.travel_to_destination() 



    def handle_hunger(self) -> None:
        if self.inventory["food"] > 0:
            self.hunger = 500
            self.inventory["food"] -= 1
            return
        
        if self.goal != "Eat":
            self.goal = "Eat"

            if self.world.find_baker() != None:
                self.confirm_destination(self.world.find_baker())
                self.sub_goal = "Find baker"
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
            self.goal = "Craft items"
            self.smith_and_craft()

        elif self.npc_type == "nurse":
            self.goal = "Manage infirmary"
            self.heal_and_bandage()

        elif self.npc_type == "baker":
            self.goal = "Make food"
            self.cook_and_bake()

        elif self.npc_type == "hunter":
            self.goal = "Hunt"
            self.hunt_and_loot()

        else:
            self.wander()










    
 
    def gather_resources(self):
        self.hunger -= 1
        visible_tiles = self.world.npc_worldview(self)
        target_terrain = None
        
        target_tiles = []
        routes = []
        final_route = None

        #Can check if resource low first with helper method, otherwise skip
        if self.inventory["wood"]< 3: 
            target_terrain = "tree"
            self.sub_goal = "Gather wood"
        elif self.inventory["herbs"] < 3: 
            target_terrain = "plant"
            self.sub_goal = "Gather herbs"
        elif self.inventory["water"] < 3: 
            target_terrain = "water"
            self.sub_goal = "Gather water"
        elif self.inventory["stone"] < 3: 
            target_terrain = "rock"
            self.sub_goal = "Gather stones"
        else:
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



 #Ensure homes spawn in and blacksmith has default start mats, 
    def smith_and_craft(self, request = None):
        self.goal = "Craft"
        self.confirm_destination(self.home)
        if not self.is_at_destination():
            self.travel_to_destination()
            return

        elif not self.inventory["equipment"]["smithing hammer"].can_use:
            self.can_craft("smithing hammer")
        elif request:
            self.can_craft(request)

        elif self.inventory["pickaxe"] < 2:
            self.can_craft("pickaxe")
        elif self.inventory["axe"] < 2:
            self.can_craft("axe")
        
        elif self.inventory["medical equipment"] < 1:
            if not self.can_craft("medical equipment")
        elif self.inventory["cooking equipment"] < 1:
            self.can_craft("cooking equipment")

        
        elif self.inventory["bow"] < 2:
            self.can_craft("bow")
        elif self.inventory["sword"] < 2:
            self.can_craft("sword")
        elif self.inventory["armor"] < 2:
            self.can_craft("armor")







        else:
            raise ValueError("Invalid crafting input")
        

    def heal_and_bandage(self):
        self.goal = "Heal"
        self.confirm_destination(self.home)
        if not self.is_at_destination():
            self.travel_to_destination()
            return

        elif not self.inventory["equipment"]["medical equipment"].can_use:
            self.find_blacksmith() 

        elif self.inventory["equipment"]["bandages"] < 2:
            self.can_craft("bandages") 
         

    def cook_and_bake(self):
        self.goal = "Cook"
        self.confirm_destination(self.home)
        if not self.is_at_destination():
            self.travel_to_destination()
            return

        elif not self.inventory["equipment"]["cooking utensils"].can_use:
            self.find_blacksmith() 

        elif self.inventory["equipment"]["food"] < 2:
            self.can_craft("food") 

    def hunt_and_loot(self):
        self.hunger -= 1
        pass

    def buy_and_sell(self, buyer, seller):
       
        pass
 


    def recycle(self):
        pass





    def can_craft(self, item_name = None, status = "Start"):
        if status == "Start" and item_name: 

            self.crafting_queue = Item(item_name)

            materials_used = self.crafting_queue.craft_materials
            for key, value in materials_used.items():
                material_cost = value
                current_amount = self.inventory[key]
                if current_amount - material_cost < 0:
                    self.crafting_queue = None
                    return False
                self.inventory[key] -= material_cost

            self.sub_goal = f"Crafting {item_name}"
            self.busy = True
            self.busy_ticks = self.crafting_queue.craft_time

            if self.type == "blacksmith":
                self.inventory["equipment"]["smithing hammer"].use()

            if self.type == "baker":
                self.inventory["equipment"]["cooking utensils"].use()

            if self.type == "nurse":
                self.inventory["equipment"]["medical equipment"].use()

            return True

        elif status == "Done":
            self.inventory["equipment"].append(self.crafting_queue)

    def wait_for_resources(self):
        pass

        
    #maybe a lesser hunt for villagers, wander and hunt use similar logic for edges








    def use(self, item):
        if item.durability == 0 or item.broken:
            return False

        item.durability -= 1
        if item.durability == 0:
            item.can_use = True

        if item.damage:
            pass

        if item.healing:
            pass

        if item.satiation:
            pass

        return True
















    def arrived(self):
        if self.destination == self.home:
            #could add helper methods for eat and heal with optional arguments of sleep and inventory
            if self.goal == "Eat":
                self.hunger = 500
                self.sleep = True
                self.sleep_ticks = 5
            if self.goal == "Heal":
                self.health = (npc_configs[self.npc_type]["health"])
                self.sleep = True
                self.sleep_ticks = 5
            if self.goal == "Craft":
                self.smith_and_craft()

        if self.destination == self.world.find_baker():
            if self.goal == "Eat":
                self.hunger = 500
                self.inventory["food"] = 4
            if self.goal == "Sell items":
                pass

        if self.destination == self.world.find_nurse(): 
            if self.goal == "Heal" :
                self.health = (npc_configs[self.npc_type]["health"])
                self.inventory["bandages"] = 4
            if self.goal == "Sell items":
                pass

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
                if ((tile.x == (upper_left[0]) or tile.x == lower_right[0] 
                or tile.y == (upper_left[1]) or tile.y == lower_right[1]) 
                and (tile.can_enter())):
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
        if self.destination:
            if self.is_at_destination():
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
            if abs(self.destination[0] - checked_tile[0]) <= 1 and  abs(self.destination[1] - checked_tile[1]) <= 1:
                return True
        return False






    def get_hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.emoji = "❌"
        
