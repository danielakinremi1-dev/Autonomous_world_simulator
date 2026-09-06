from collections import defaultdict
from world_objects.items import Items


#Config shows traversability, viusals of terrain types
terrain_configs = {"grass":{"traversable":True, "emoji":"🟩", "hp":None},
           "tree":{"traversable":False, "emoji":"🌳", "hp":10},
           "water":{"traversable":False, "emoji":"🌊", "hp":None},
           "ground":{"traversable":True, "emoji":"🟫", "hp":None},
           "rock":{"traversable":False, "emoji":"🪨", "hp": 100},
           "plant":{"traversable":True, "emoji":"🌾", "hp":3}}

#Setup npc inventory objects 

npc_configs = {"blacksmith":{"health":400, "emoji":"👲", "speed" :80, "job" : "craft", "view_radius" : 6, 
                             "inventory": defaultdict(int, {"money": 300,"food": 3,"bandages": 5, "axe": 1000, "pickaxe": 1000})}, 

               "nurse":{"health":300, "emoji":"👩‍⚕️","speed" :55, "job" : "heal", "view_radius" : 8, 
                        "inventory": defaultdict(int, {"money": 400,"food": 5,"bandages": 15})}, 

               "hunter":{"health":800, "emoji":"🥷","speed" :200, "job" : "hunt", "view_radius" : 12, 
                         "inventory": defaultdict(int, {"money": 500,"food": 5,"bandages": 5, "axe": 200, "pickaxe": 200})}, 

               "baker":{"health":250, "emoji":"🧑‍🍳","speed" :60, "job" : "bake", "view_radius" : 7, 
                        "inventory": defaultdict(int, {"money": 300,"food": 15,"bandages": 3})},

               "villager":{"health":200, "emoji":"👩‍🌾","speed" :50, "job" : "gather", "view_radius" : 8, 
                           "inventory": defaultdict(int, {"money": 150,"food": 2,"bandages": 2, "axe": 200, "pickaxe": 200})}}

direction_configs = ((0, -1), (0, 1), (-1, 0), (1, 0), (0,0))

item_configs = {"axe":{"durability": 30, "damage": 5, "craft time": 14, "price": 30,
                       "craft materials": {"wood": 3, "stone": 3, "water": 2}, 
                       "recycle materials": {"wood": 1, "stone": 1}}, 

                "smithing hammer": {"durability": 60, "damage": 4, "craft time": 10, "price": 400,
                       "craft materials": {"wood":2, "stone": 5, "water": 3}, 
                       "recycle materials": {"wood": 1, "stone": 2, "water": 0}}, 

                "pickaxe": {"durability": 25, "damage": 4, "craft time": 14, "price": 35,
                       "craft materials": {"wood": 5, "stone": 6, "water": 2}, 
                       "recycle materials": {"wood": 2, "stone": 3, "water": 0}}, 

                "sword":{"durability": 50, "damage": 20, "craft time": 22, "price": 100,
                       "craft materials": {"wood": 0, "stone": 6, "water": 3}, 
                       "recycle materials": {"wood": 0, "stone": 3, "water": 0}}, 

                "bow": {"durability": 50, "damage": 15, "craft time": 20, "price": 95,
                       "craft materials": {"wood": 6, "stone": 0, "water": 3}, 
                       "recycle materials": {"wood": 2, "stone": 0, "water": 0}}, 

                "cooking utensils": {"durability": 70, "damage": 1, "craft time": 10, "price": 60,
                       "craft materials": {"wood": 5, "stone": 2, "water": 1}, 
                       "recycle materials": {"wood": 2, "stone": 1, "water": 0}}, 

                "armor": {"durability": 200, "damage": 0, "craft time": 30, "price": 150,
                        "craft materials": {"wood": 2, "stone": 7, "water": 3}, 
                       "recycle materials": {"wood": 1, "stone": 3, "water": 0}},
                
                "medical equipment":{"durability": 70, "damage": 0, "craft time": 25, "price": 70,
                       "craft materials": {"wood": 2, "stone": 3, "water": 1}, 
                       "recycle materials": {"wood": 1, "stone": 1, "water": 0}}}

