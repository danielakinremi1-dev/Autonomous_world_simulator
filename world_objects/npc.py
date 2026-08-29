from world_objects.configs import npc_configs, direction_configs
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from world_objects.world import World

class NPC():
    def __init__(self, x: int, y: int, npc: str, world: "World") -> None:
        if npc not in npc_configs:
            raise ValueError("Invalid npc")
        self.x = x
        self.y = y
        self.npc_type = npc
        self.world = world
        self.health = npc_configs[npc]["health"]
        self.emoji = npc_configs[npc]["emoji"] 


    def __str__(self) -> str:
        return f"A {self.npc_type}"


    def get_visual(self) -> str:
         return self.emoji


    def wander(self) -> bool:
        direction = random.choice(list(direction_configs))
        return self.move(direction)


    

    def move(self, direction: str) -> bool:
        if direction == "stay":
            return True
        return self.world.move_npc(self, direction)

