from world_objects.configs import item_configs


class Item():

    def __init__(self, item_name):
        self.item_name = item_name
        self.durability = item_configs[item_name]["durability"]
        self.craft_time = item_configs[item_name]["craft time"]
        self.craft_materials = item_configs[item_name]["craft materials"]
        self.recycle_materials = item_configs[item_name]["recycle materials"]
        self.damage = item_configs[item_name]["damage"]
        self.sell_price = item_configs[item_name]["price"]
        self.recycle_price = self.sell_price // 3      
        self.broken = False

    def use(self):
        if self.durability == 0 or self.broken:
            return False

        self.durability -= 1
        if self.durability == 0:
            self.broken = True
        return True