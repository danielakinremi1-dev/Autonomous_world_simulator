from world_objects.terrain import Terrain

class Tile():
    def __init__(self, terrain: Terrain):
        self.terrain = terrain
        self.occupant = None




    def can_enter(self) -> bool: 
        return self.terrain.traversable and self.occupant == None

    def __str__(self):
        if self.occupant is not None:
            return f"A tile occupied by a{str(self.occupant)}"
        else:
            return f"A tile of {str(self.terrain)}"

    def get_visual(self) -> str:
        if self.occupant is not None:
            return self.occupant.get_visual()
        else:
            return self.terrain.get_visual()