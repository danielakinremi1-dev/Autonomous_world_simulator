
from world_objects.terrain import Terrain
from world_objects.tile import Tile 
from world_objects.npc import NPC
from world_objects.configs import npc_configs, direction_configs
import random

class World():
    def __init__(self, map_input: list[list[str]]):
        self.grid = []
        self.row_len = len(map_input[0])
        self.rows = len(map_input)
        self.npcs = []
        for row in map_input:
            if len(row) != self.row_len:
                raise ValueError("Misshapen map input")


        for row in map_input:
            new_row = []
            for terrain_obj in row:
                new_row.append(Tile(Terrain(terrain_obj)))
            self.grid.append(new_row)

    def __str__(self):
        return f"A {self.row_len} by {self.rows} simulated world!"


    def spawn_npc(self):

        spawn_locations = []
        
        for y_idx, row in enumerate(self.grid):
            for x_idx, tile in enumerate(row):
                if tile.can_enter() and tile.terrain.type == "ground":
                    spawn_locations.append((x_idx, y_idx))

        for npc in npc_configs.keys():
            if spawn_locations:
                spawn_coord = random.choice(spawn_locations)
                spawn_locations.remove(spawn_coord)
                new_npc = NPC(spawn_coord[0], spawn_coord[1], npc, self)
                self.grid[spawn_coord[1]][spawn_coord[0]].occupant = new_npc
                self.npcs.append(new_npc)
            else:
                raise ValueError("Not enough spawn tiles for all NPCs")

    def place_npc(self, x: int= 1, y:int = 1 , npc_type: str = "villager") -> NPC:
    
        if (x < 0 or y < 0) or (x >= self.row_len or y >= self.rows):
            raise ValueError("Can't spawn off world map") 
        if not self.grid[y][x].can_enter():
            raise ValueError("Can't spawn on blocked tile")
        
        npc = NPC(x, y, npc_type, self)
        self.grid[y][x].occupant = npc
        self.npcs.append(npc)
        return npc

        
    def move_npc(self, npc: NPC, requested_coords: tuple[int, int]) -> bool:

        if (requested_coords[0] < 0 or requested_coords[1] < 0):
            return False
        if requested_coords[0] >= self.row_len or requested_coords[1] >= self.rows:
            return False

        if requested_coords[0] == npc.x and requested_coords[1] == npc.y:
            return True     
        
        if abs(requested_coords[0] - npc.x) + abs(requested_coords[1] - npc.y) != 1:
            raise ValueError("Invalid directional movement requested")

        
        requested_tile = self.grid[requested_coords[1]][requested_coords[0]]
        previous_tile = self.grid[npc.y][npc.x]
        if requested_tile.can_enter():
            requested_tile.occupant = npc
            npc.x, npc.y = requested_coords[0], requested_coords[1]
            previous_tile.occupant = None
            return True
        else:
            return False

    def advance_world(self) -> None:
        #sorted(self.npcs, self.npcs.speed)
        for npc in self.npcs:
            npc.observe_and_act()

    
    def find_nurse(self):
        for npc in self.npcs:
            if npc.npc_type == "nurse":
                return (npc.x, npc.y)
        return None
            
    def find_baker(self):
        for npc in self.npcs:
            if npc.npc_type == "baker":
                return (npc.x, npc.y)
        return None
            
    def get_render_data(self):
        visual_grid = []
        for row in self.grid:
            new_visual_row = []
            for tile in row:
                new_visual_row.append(tile.get_visual())
            visual_grid.append(new_visual_row)
        return visual_grid



 