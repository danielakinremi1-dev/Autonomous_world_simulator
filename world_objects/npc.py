from world_objects.configs import npc_configs, direction_configs
from typing import TYPE_CHECKING
import random

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
        self.hunger = 500
        self.inventory = {"food": 2,"bandages": 2}
        self.destination = None
        self.pathing = None
        self.home = None 
        self.goal = None
        self.was_stopped = False
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

       
        elif self.destination != None:
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

        elif self.health < ((npc_configs[self.npc_type]["health"]) * 0.9):
            self.handle_health()
        elif self.hunger <= 250:
            self.handle_hunger()

        else:
            self.default_action()

    def pathfind(self)-> bool: 
        #could also update to only check static objects for blockage
        destination = self.destination
        start_coord = (self.x, self.y)
        visited = [start_coord]
        queue = [start_coord]
        path_history = {}
        tiles = self.world.grid

        path_history[start_coord] = None
        if destination == start_coord:
            self.arrived()
            return False

        
        while queue:
            current_coord = queue.pop(0)
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
                visited.append(direction)
                path_history[direction] = current_coord
                if direction == destination:
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
        else:
            if self.destination != self.world.find_nurse() and self.destination != self.home:
                self.destination = self.world.find_nurse()
                if self.destination == None:
                    if self.home != None:
                        self.destination = self.home
                    else:
                        return

                can_move = self.pathfind()
                if can_move:
                    self.move(self.pathing.pop(0))

    def handle_hunger(self) -> None:
        if self.inventory["food"] > 0:
            self.hunger = 500
            self.inventory["food"] -= 1
            return

        if self.world.find_baker() != None:
            if self.destination != self.world.find_baker()
                self.destination = self.world.find_baker()

        elif self.home != None:
            if self.destination != self.home:
                self.destination = self.home
        else:
            return
        if self.pathing == None or self.pathing == []:
            can_find = self.pathfind()
            if not can_find:
                return

        can_move = self.move(self.pathing.pop(0))
        if not can_move:
            self.pathing = None
        #reset pathing in move when called


    def default_action(self) -> None:
        self.wander()

    def arrived(self):
        if self.destination == self.home:
            self.health = (npc_configs[self.npc_type]["health"])
            self.hunger = 500
            self.sleep = True
            self.sleep_ticks = 5

        if self.destination == self.world.find_baker():
            self.hunger = 500
            self.inventory["food"] = 4

        if self.destination == self.world.find_nurse():
            self.health = (npc_configs[self.npc_type]["health"])
            self.inventory["bandages"] = 4

        self.destination = None
        self.pathing = None

    def wander(self) -> None:
        direction = random.choice(list(direction_configs))
        new_coord = (self.x + direction[0], self.y + direction[1])
        self.move(new_coord)


    def move(self, coord: tuple[int, int]) -> bool:
        if coord == (self.x, self.y):
            self.arrived()
            return True
        move = self.world.move_npc(self, coord)
        if self.destination:
            if abs(self.destination[0] - self.x) <= 1 and  abs(self.destination[1] - self.y) <= 1:
                self.arrived()

        return move