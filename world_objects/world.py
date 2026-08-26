
from terrain import Terrain
from tile import Tile
from constants import DEFAULT_MAP

class World():
    def __init__(self, map_input):
        self.grid = []
        self.map_input = map_input
        self.row_len = len(map_input[0])
        self.rows = len(map_input)
        for row in map_input:
            if len(row) != self.row_len:
                raise ValueError("Misshapen map input")


        for row in map_input:
            new_row = []
            for terrain_obj in row:
                new_row.append(Tile(Terrain(terrain_obj)))
            self.grid.append(new_row)

    def __repr__(self):
        return f"A {self.row_len} by {self.rows} simulated world!"

    def get_render_data(self):
        visual_grid = []
        for row in self.grid:
            new_visual_row = []
            for tile in row:
                new_visual_row.append(tile.get_visual())
            visual_grid.append(new_visual_row)
        return visual_grid


new_world = World(DEFAULT_MAP)
print(new_world.grid)
print(new_world)
print(new_world.get_render_data())