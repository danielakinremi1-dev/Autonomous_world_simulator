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
        self.damage = item_configs[item_name]["damage"]
        self.healing = item_configs[item_name]["healing"]
        self.satiation = item_configs[item_name]["healing"]
        self.armor = item_configs[item_name]["armor"]
        self.sell_price = item_configs[item_name]["price"]
        self.recycle_price = self.sell_price // 3 
        self.can_use = False
        

