
#Config shows traversability, viusals of terrain types
terrain_configs = {"grass":{"traversable":True, "emoji":"🟩"},
           "tree":{"traversable":False, "emoji":"🌳"},
           "water":{"traversable":False, "emoji":"🌊"},
           "ground":{"traversable":True, "emoji":"🟫"},
           "rock":{"traversable":False, "emoji":"🪨"},
           "plant":{"traversable":True, "emoji":"🌾"}}


npc_configs = {"blacksmith":{"health":600, "emoji":"👲", "speed" :80, "job" : "craft"}, 
               "nurse":{"health":200, "emoji":"👩‍⚕️","speed" :55, "job" : "heal"}, 
               "hunter":{"health":800, "emoji":"🥷","speed" :200, "job" : "hunt"}, 
               "baker":{"health":200, "emoji":"🧑‍🍳","speed" :60, "job" : "bake"},
               "villager":{"health":200, "emoji":"👩‍🌾","speed" :50, "job" : "gather"}}

direction_configs = ((0, -1), (0, 1), (-1, 0), (1, 0), (0,0))

