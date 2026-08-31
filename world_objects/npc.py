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


    def __str__(self) -> str:
        return f"A {self.npc_type}"
    
    def get_visual(self) -> str:
         return self.emoji






    def observe_and_act(self) -> None: 
        if self.hunger <= 250:
            self.handle_hunger()

        elif self.health < npc_configs[self.npc_type]["health"]:
            self.handle_health()

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
            return True

        
        while queue:
            current_coord = queue.pop(0)

            if current_coord[1] != 0:
                up = (current_coord[0], current_coord[1] - 1)
                if up not in visited and tiles[up[1]][up[0]].can_enter():
                    queue.append(up)
                    visited.append(up)
                    path_history[up] = current_coord
                    if up == destination:
                        return self.traceback(up, path_history)

            if current_coord[1] != self.world.rows - 1:
                down = (current_coord[0], current_coord[1] + 1)
                if down not in visited and tiles[down[1]][down[0]].can_enter():
                    queue.append(down)
                    visited.append(down)
                    path_history[down] = current_coord
                    if down == destination:
                        return self.traceback(down, path_history)

            if current_coord[0] != 0:
                left = (current_coord[0] - 1, current_coord[1])
                if left not in visited and tiles[left[1]][left[0]].can_enter():
                    queue.append(left)
                    visited.append(left)
                    path_history[left] = current_coord
                    if left == destination:
                        return self.traceback(left, path_history)

            if current_coord[0] != self.world.row_len - 1:
                right = (current_coord[0] + 1, current_coord[1])
                if right not in visited and tiles[right[1]][right[0]].can_enter():
                    queue.append(right)
                    visited.append(right)
                    path_history[right] = current_coord
                    if right == destination:
                        return self.traceback(right, path_history)

        return False
            
    def traceback(self, destination: tuple[int,int], pathing: dict[tuple[int,int]]) -> None:
        current_coord = destination
        path = []
        while pathing[current_coord] != None:
            path.append(current_coord)
            current_coord = pathing[current_coord]
        self.pathing = path[::-1]
        return True
        
 

    def handle_health(self) -> None:
        if self.inventory["bandages"] != 0:
            self.health = npc_configs[self.npc_type]["health"]
            self.inventory["bandages"] -= 1
        else:
            self.destination = self.world.find_nurse()
            self.pathfind()

    def handle_hunger(self) -> None:
        if self.inventory["food"] != 0:
            self.hunger = 500
            self.inventory["food"] -= 1
        else:
            self.destination = self.world.find_baker()
            self.pathfind()
            #potentially go home too


    def default_action(self) -> None:
        if self.pathing != None: 
            self.move(self.pathing.pop(0))
        else:
            if self.destination != None:
                self.pathfind(self.destination)
                self.move(self.pathing.pop(0))
            else:
                self.wander()


    def wander(self) -> None:
        direction = random.choice(list(direction_configs))
        new_coordinates = (self.x + direction[0], self.y + direction[1])
        self.move(new_coordinates)

    def move(self, coord: tuple[int, int]) -> None:
        self.hunger -= 1
        if coord == (self.x, self.y)
            return
        path_clear = self.world.move_npc(self, coord)
        if not path_clear:
            self.pathing = None