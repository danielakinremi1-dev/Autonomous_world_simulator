from collections import defaultdict
from world_objects.items import Item


#Config shows traversability, viusals of terrain types
terrain_configs = {"grass":{"traversable":True, "emoji":"🟩", "hp":None},
           "tree":{"traversable":False, "emoji":"🌳", "hp":10},
           "water":{"traversable":False, "emoji":"🌊", "hp":None},
           "ground":{"traversable":True, "emoji":"🟫", "hp":None},
           "rock":{"traversable":False, "emoji":"🪨", "hp": 100},
           "plant":{"traversable":True, "emoji":"🌾", "hp":3}}

#Setup npc inventory objects and refactor for dictionary searches

npc_configs = {"blacksmith":{"health":400, "emoji":"👲", "speed" :80, "job" : "craft", "view_radius" : 6, 
                            "inventory": defaultdict(int, {"money": 300,"food": 3,"bandages": 5, 
                            "equipment": [Item("axe"), Item("pickaxe"), Item("smithing hammer")]})}, 

               "nurse":{"health":300, "emoji":"👩‍⚕️","speed" :55, "job" : "heal", "view_radius" : 8, 
                        "inventory": defaultdict(int, {"money": 400,"food": 5,"bandages": 15, 
                        "equipment": [Item("bandages"), Item("bandages"), Item("medical equipment")]})}, 

               "hunter":{"health":800, "emoji":"🥷","speed" :200, "job" : "hunt", "view_radius" : 12, 
                        "inventory": defaultdict(int, {"money": 500,"food": 5,"bandages": 5, 
                        "equipment": [Item("sword"), Item("bow"), Item("arrows")]})}, 

               "baker":{"health":250, "emoji":"🧑‍🍳","speed" :60, "job" : "bake", "view_radius" : 7, 
                        "inventory": defaultdict(int, {"money": 300,"food": 15,"bandages": 3, 
                        "equipment": [Item("food"), Item("food"), Item("cooking utensils")]})},

               "villager":{"health":200, "emoji":"👩‍🌾","speed" :50, "job" : "gather", "view_radius" : 8, 
                           "inventory": defaultdict(int, {"money": 150,"food": 2,"bandages": 2, 
                            "equipment": [Item("axe"), Item("pickaxe")]})}}

direction_configs = ((0, -1), (0, 1), (-1, 0), (1, 0), (0,0))

item_configs = {"axe":{"durability": 30, "craft time": 14, "consumable" : False, 
                       "price": 30, "item type": "logging", "stat bonus": 10, "quantity": 1,
                       "craft materials": {"wood": 3, "stone": 3, "water": 2}, 
                       "recycle materials": {"wood": 1, "stone": 1}}, 

                "smithing hammer": {"durability": 60, "craft time": 28, "consumable" : False, 
                     "price": 400, "item type": "smithing", "stat bonus": 10, "quantity": 1,
                       "craft materials": {"wood":1, "stone": 2, "water": 3}, 
                       "recycle materials": {"wood": 1, "stone": 2, "water": 0}}, 

                "pickaxe": {"durability": 25, "craft time": 14, "consumable" : False,  
                            "price": 35, "item type": "mining", "stat bonus": 10, "quantity": 1,
                       "craft materials": {"wood": 5, "stone": 6, "water": 2}, 
                       "recycle materials": {"wood": 2, "stone": 3, "water": 0}}, 

                "sword":{"durability": 50, "craft time": 22, "consumable" : False, 
                         "price": 100, "item type": "damage", "stat bonus": 20, "quantity": 1,
                       "craft materials": {"wood": 0, "stone": 6, "water": 3}, 
                       "recycle materials": {"wood": 0, "stone": 3, "water": 0}}, 

                "bow": {"durability": 50, "craft time": 20, "consumable" : False, 
                        "price": 95, "item type": "damage", "stat bonus": 15, "quantity": 1,
                       "craft materials": {"wood": 6, "stone": 0, "water": 3}, 
                       "recycle materials": {"wood": 2, "stone": 0, "water": 0}}, 

                "arrows": {"durability": 1,"craft time": 5, "consumable" : True, 
                     "price": 60, "item type": "damage", "stat bonus": 5, "quantity": 10,
                       "craft materials": {"wood": 5, "stone": 2, "water": 1}, 
                       "recycle materials": {"wood": 2, "stone": 1, "water": 0}},  

                "cooking utensils": {"durability": 70, "craft time": 10, "consumable" : False, 
                     "price": 60, "item type": "cooking equipment", "stat bonus": 10, "quantity": 1,
                       "craft materials": {"wood": 5, "stone": 2, "water": 1}, 
                       "recycle materials": {"wood": 2, "stone": 1, "water": 0}}, 

                "armor": {"durability": 200, "craft time": 30, "consumable" : False, 
                          "price": 150, "item type": "armor", "stat bonus":  50, "quantity": 1,
                        "craft materials": {"wood": 2, "stone": 7, "water": 3}, 
                       "recycle materials": {"wood": 1, "stone": 3, "water": 0}},
                
                "medical equipment":{"durability": 70, "craft time": 25, "consumable" : False, 
                     "price": 70, "item type": "healing equipment", "stat bonus": 10, "quantity": 1,
                       "craft materials": {"wood": 2, "stone": 5, "water": 1}, 
                       "recycle materials": {"wood": 1, "stone": 1, "water": 0}},
                
                "bandages":{"durability": 1,"craft time": 20, "consumable" : True, 
                     "price": 35, "item type": "healing", "stat bonus": 100, "quantity": 2,
                       "craft materials": {"wood": 1, "herbs": 3, "water": 1}, 
                       "recycle materials": {"wood": 1, "stone": 1, "water": 0}},
                
                "food":{"durability": 1, "craft time": 15, "consumable" : True, 
                     "price": 25, "item type": "satiation", "stat bonus": 100, "quantity": 1,
                       "craft materials": {"wood": 1, "wheat": 3, "water": 1}, 
                       "recycle materials": {"wood": 1, "stone": 1, "water": 0}}}

