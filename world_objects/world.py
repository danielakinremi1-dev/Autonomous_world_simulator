from world_objects.terrain import Terrain
from world_objects.tile import Tile
from world_objects.npc import NPC
from world_objects.configs import npc_configs
from world_objects.items import Item
import random


class World:
    def __init__(self, map_input: list[list[str]]):
        if len(map_input) <= 1:
            raise ValueError("No proper map input")

        self.grid = []
        self.row_len = len(map_input[0])
        self.rows = len(map_input)
        self.npcs = []
        self.despawned_npc = None
        self.despawn_ticks = 0
        self.despawn_tile = None

        for row in map_input:
            if len(row) != self.row_len:
                raise ValueError("Misshapen map input")

        for y_idx, row in enumerate(map_input):
            new_row = []
            for x_idx, terrain_obj in enumerate(row):
                new_row.append(Tile(x_idx, y_idx, Terrain(terrain_obj)))
            self.grid.append(new_row)

    def __str__(self):
        return f"A {self.row_len} by {self.rows} simulated world!"

    def get_render_data(self):
        visual_grid = []
        for row in self.grid:
            new_visual_row = []
            for tile in row:
                new_visual_row.append(tile.get_visual())
            visual_grid.append(new_visual_row)
        return visual_grid

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

        self.npcs.sort(key=lambda npc: npc.speed, reverse=True)

    def place_npc(self, x: int = 1, y: int = 1, npc_type: str = "villager") -> NPC:

        if (x < 0 or y < 0) or (x >= self.row_len or y >= self.rows):
            raise ValueError("Can't spawn off world map")
        if not self.grid[y][x].can_enter():
            raise ValueError("Can't spawn on blocked tile")

        npc = NPC(x, y, npc_type, self)
        self.grid[y][x].occupant = npc
        self.npcs.append(npc)
        return npc

    def move_npc(self, npc: NPC, requested_coords: tuple[int, int]) -> bool:

        if requested_coords[0] < 0 or requested_coords[1] < 0:
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
        if self.despawn_ticks:
            self.despawn_ticks -= 1
            if self.despawn_ticks == 0:
                if not self.despawn_tile.can_enter():
                    self.despawn_ticks += 1
                    return
                self.despawn_and_respawn(self.despawned_npc, respawn=True)
                self.despawned_npc = None
                self.despawn_tile = None

        for npc in self.npcs:
            if npc != self.despawned_npc:
                npc.observe_and_act()

    # Known locations
    def find_nurse(self):
        for npc in self.npcs:
            if npc.npc_type == "nurse":
                return (npc.x, npc.y)
        raise ValueError("NPC data doesn't exist")

    def find_baker(self):
        for npc in self.npcs:
            if npc.npc_type == "baker":
                return (npc.x, npc.y)
        raise ValueError("NPC data doesn't exist")

    def find_blacksmith(self):
        for npc in self.npcs:
            if npc.npc_type == "blacksmith":
                return (npc.x, npc.y)
        raise ValueError("NPC data doesn't exist")

    def interact_nurse(self):
        for npc in self.npcs:
            if npc.npc_type == "nurse":
                return npc
        raise ValueError("NPC data doesn't exist")

    def interact_baker(self):
        for npc in self.npcs:
            if npc.npc_type == "baker":
                return npc
        raise ValueError("NPC data doesn't exist")

    def interact_blacksmith(self):
        for npc in self.npcs:
            if npc.npc_type == "blacksmith":
                return npc
        raise ValueError("NPC data doesn't exist")

    def npc_worldview(self, npc: NPC) -> dict:
        default_view = npc.view_radius

        world_map = self.grid
        minimap = []

        upper_left = (npc.x - default_view, npc.y - default_view)
        lower_right = (npc.x + default_view, npc.y + default_view)

        if upper_left[0] < 0:
            upper_left = (0, upper_left[1])

        if upper_left[1] < 0:
            upper_left = (upper_left[0], 0)

        if lower_right[0] >= self.row_len:
            lower_right = (self.row_len - 1, lower_right[1])
        if lower_right[1] >= self.rows:
            lower_right = (lower_right[0], self.rows - 1)

        for row in range(upper_left[1], lower_right[1] + 1):
            section = world_map[row][upper_left[0] : lower_right[0] + 1]
            minimap.append(section)
        return {
            "minimap": minimap,
            "upper_left": upper_left,
            "lower_right": lower_right,
        }

    def get_resource(self, npc, tile_coord, target_resource):

        tile = self.grid[tile_coord[1]][tile_coord[0]]
        terrain = tile.terrain

        if target_resource == "Gather wood" and terrain.type == "tree":
            if npc.inventory["axe"] and npc.inventory["axe"].usable:
                npc.inventory["axe"].use()
                npc.inventory["wood"].quantity += 1
                tile.terrain.hp -= 1
                if tile.terrain.hp < 1:
                    tile.terrain = Terrain("ground")

        elif target_resource == "Gather stones" and terrain.type == "rock":
            if npc.inventory["pickaxe"] and npc.inventory["pickaxe"].usable:
                npc.inventory["pickaxe"].use()
                npc.inventory["stone"].quantity += 1
                tile.terrain.hp -= 1
                if tile.terrain.hp < 1:
                    tile.terrain = Terrain("ground")

        elif target_resource == "Gather herbs" and terrain.type == "plant":
            npc.inventory["herbs"].quantity += 1
            tile.terrain.hp -= 1
            if tile.terrain.hp < 1:
                tile.terrain = Terrain("grass")

        elif target_resource == "Gather wheat" and terrain.type == "wheat":
            npc.inventory["wheat"].quantity += 1
            tile.terrain.hp -= 1
            if tile.terrain.hp < 1:
                tile.terrain = Terrain("grass")

        elif target_resource == "Gather water" and terrain.type == "water":
            npc.inventory["water"].quantity += 1

    def world_edges(self):
        world_map = self.grid

        upper_tile = world_map[0][0]
        lower_tile = world_map[self.rows - 1][self.row_len - 1]

        upper_left = (upper_tile.x, upper_tile.y)
        lower_right = (lower_tile.x, lower_tile.y)
        return {
            "world_map": world_map,
            "upper_left": upper_left,
            "lower_left": lower_right,
        }

    def despawn_and_respawn(self, npc, respawn=False):
        if not respawn:
            self.despawned_npc = npc
            self.despawn_tile = self.grid[npc.y][npc.x]
            self.despawn_tile.occupant = None
            self.despawn_ticks = 20
            return

        if not npc.inventory["herbs"]:
            npc.inventory["herbs"] = Item("herbs")
            npc.inventory["herbs"].quantity = 0
        npc.inventory["herbs"].quantity += 3

        if not npc.inventory["stone"]:
            npc.inventory["stone"] = Item("stone")
            npc.inventory["stone"].quantity = 0
        npc.inventory["stone"].quantity += 3

        if not npc.inventory["wheat"]:
            npc.inventory["wheat"] = Item("wheat")
            npc.inventory["wheat"].quantity = 0
        npc.inventory["wheat"].quantity += 3

        if not npc.inventory["water"]:
            npc.inventory["water"] = Item("water")
            npc.inventory["water"].quantity = 0
        npc.inventory["water"].quantity += 3

        if not npc.inventory["wood"]:
            npc.inventory["wood"] = Item("wood")
            npc.inventory["wood"].quantity = 0
        npc.inventory["wood"].quantity += 3

        self.despawn_tile.occupant = npc
