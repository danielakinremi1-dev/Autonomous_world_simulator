from terrain_configs import configs

class Terrain():
    def __init__(self, type):
        self.type = type
        self.emoji = ""
        self.traversable = True

        if self.type not in configs:
            raise ValueError("Invalid terrain type")
        self.emoji = configs[type]["traversable"]
        self.traversable = configs[type]["emoji"]




