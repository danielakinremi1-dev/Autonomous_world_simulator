from world_objects.configs import terrain_configs

class Terrain():
    def __init__(self, type: str):
        if type not in terrain_configs:
            raise ValueError("Invalid terrain type") 
        
        self.type = type
        self.emoji = terrain_configs[type]["emoji"]
        self.traversable = terrain_configs[type]["traversable"]

    def __str__(self) -> str:
            return f"{self.type} block"

    def get_visual(self) -> str:
         return self.emoji


