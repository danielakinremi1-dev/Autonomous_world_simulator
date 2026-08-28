from world_objects.configs import npc_configs
from world_objects.world import World
from world_objects.npc import NPC

class NPC():
    def __init__(self, x: int, y: int, npc: NPC, world: World):
        if npc not in npc_configs:
            raise ValueError("Invalid npc")
        self.x = x
        self.y = y
        self.npc_type = npc
        self.world = world
        self.health = npc_configs[npc]["health"]
        self.emoji = npc_configs[npc]["emoji"]


    def __str__(self):
        return f"A {self.npc_type}"
    

    def get_visual(self) -> str:
         return self.emoji

    def move(self, direction: str):
        new_tile = self.world.move_npc(self, direction)
        self.x = new_tile[1]
        self.y = new_tile[0]
