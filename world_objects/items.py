from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world_objects.configs import item_configs

class Item():

    def __init__(self, item_name):
        self.item_name = item_name
        self.durability = item_configs[item_name]["durability"]
        self.craft_time = item_configs[item_name]["craft time"]
        self.craft_materials = item_configs[item_name]["craft materials"]
        self.recycle_materials = item_configs[item_name]["recycle materials"]
        self.item_type = item_configs[item_name]["item_type"]
        self.stat_bonus = item_configs[item_name]["stat bonus"]
        self.quantity = item_configs[item_name]["quantity"]
        self.consumable = item_configs[item_name]["stat bonus"]
        self.sell_price = item_configs[item_name]["price"]
        self.recycle_price = self.sell_price // 3 
        self.usable = True
        self.broken = 0

        

    def use(self, item):
        if item.durability <= 0:
            self.broken += 1
            self.quantity -= 1
            if self.quantity >= 1:
                self.durability = item_configs[self.item_name]["durability"] - 1
                return self.stat_bonus
            else:
                self.usable = False
                return 0
        

