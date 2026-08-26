from terrain_configs import configs

class Terrain():
    def __init__(self, type):
        if type not in configs:
            raise ValueError("Invalid terrain type") 
        
        self.type = type
        self.emoji = configs[type]["emoji"]
        self.traversable = configs[type]["traversable"]

    def __str__(self):
            return f"{self.type} block"

    def get_visual(self):
         return self.emoji


