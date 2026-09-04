from world_objects.configs import npc_configs, direction_configs
from typing import TYPE_CHECKING
import random
from collections import deque
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
        self.view_radius = npc_configs[npc_type]["view_radius"]  
        self.hunger = 500
        self.inventory = {"food": 2,"bandages": 2}
        self.destination = None
        self.pathing = None
        self.home = None 
        self.goal = None 
        self.sleep_ticks = 0
        self.sleep = False
        self.alive = True
        
        #Spawn in homes with NPCs and provide visuals for goals later 


    def __str__(self) -> str:
        return f"A {self.npc_type}"
    
    def get_visual(self) -> str:
         return self.emoji



    def observe_and_act(self) -> None: 
        self.hunger -= 1

        if self.sleep == True:
            if self.sleep_ticks == 0:
                self.sleep = False
            else:
                self.sleep_ticks -= 1
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
        self.pathing = path[::-1]
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
            elif self.home != None:
                self.confirm_destination(self.home)
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
            elif self.home != None:
                self.confirm_destination(self.home)
            else:
                self.goal = None
                return
            
        self.travel_to_destination() 


    def default_action(self) -> None:

        if self.npc_type == "villager":
            self.gather_resources()

        if self.npc_type == "blacksmith":
            self.smith_and_craft()

        if self.npc_type == "nurse":
            self.heal_and_bandage()

        if self.npc_type == "baker":
            self.cook_and_bake()

        if self.npc_type == "hunter":
            self.hunt_and_loot()

        


        else:
            self.wander()

    def arrived(self):
        if self.destination == self.home:
            if self.goal == "Eat":
                self.hunger = 500
                self.sleep = True
                self.sleep_ticks = 5
            if self.goal == "Heal":
                self.health = (npc_configs[self.npc_type]["health"])
                self.sleep = True
                self.sleep_ticks = 5

        if self.destination == self.world.find_baker():
            if self.goal == "Eat":
                self.hunger = 500
                self.inventory["food"] = 4

        if self.destination == self.world.find_nurse(): 
            if self.goal == "Heal":
                self.health = (npc_configs[self.npc_type]["health"])
                self.inventory["bandages"] = 4

        self.destination = None
        self.pathing = None
        self.goal = None

    def wander(self) -> None:
        direction = random.choice(direction_configs)
        new_coord = (self.x + direction[0], self.y + direction[1])
        self.move(new_coord)


    def move(self, coord: tuple[int, int]) -> bool:
        move = self.world.move_npc(self, coord)
        if self.destination:
            if abs(self.destination[0] - self.x) <= 1 and  abs(self.destination[1] - self.y) <= 1:
                self.arrived()
        return move

    def travel_to_destination(self):
        if self.is_at_destination():
            self.arrived()
            return

        if self.pathing != None and len(self.pathing) > 0: 
            can_move = self.move(self.pathing.pop(0))
            if not can_move:
                self.pathing = None
            return

        can_find = self.pathfind()
        if can_find:
            can_move = self.move(self.pathing.pop(0))
            if not can_move:
                self.pathing = None

    def confirm_destination(self, new_dest: tuple[int, int]) -> None:
        if self.destination != new_dest:
            self.destination = new_dest
            self.pathing = None

    def is_at_destination(self, checked_tile: tuple[int, int] | None = None) -> bool:
        if checked_tile == None:
            checked_tile = (self.x, self.y)

        if self.destination != None:
            if abs(self.destination[0] - checked_tile[0]) <= 1 and  abs(self.destination[1] - checked_tile[1]) <= 1:
                return True
        return False
 
    def gather_resources(self):
        pass
        #water

        #rock

        #g 






    def smith_and_craft(self):
        pass

    def heal_and_bandage(self):
        pass

    def cook_and_bake(self):
        pass

    def hunt_and_loot(self):
        pass
