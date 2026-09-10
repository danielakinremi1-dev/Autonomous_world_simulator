from world_objects.helper_item_configs import item_configs


class Item:
    def __init__(self, item_name, quantity=1):
        self.item_name = item_name
        self.durability = item_configs[item_name]["durability"]
        self.craft_time = item_configs[item_name]["craft time"]
        self.craft_materials = item_configs[item_name]["craft materials"]
        self.recycle_materials = item_configs[item_name]["recycle materials"]
        self.item_type = item_configs[item_name]["item type"]
        self.stat_bonus = item_configs[item_name]["stat bonus"]
        self.quantity = quantity
        self.consumable = item_configs[item_name]["consumable"]
        self.sell_price = item_configs[item_name]["price"]
        self.recycle_price = self.sell_price // 3
        self.usable = True
        self.broken = 0

    def use(self):
        if self.usable:
            self.durability -= 1
            if self.durability <= 0:
                self.broken += 1
                self.quantity -= 1
                if self.quantity >= 1:
                    self.durability = item_configs[self.item_name]["durability"]
                    return self.stat_bonus
            return self.stat_bonus
        return 0
