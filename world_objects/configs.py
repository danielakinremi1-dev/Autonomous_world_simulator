
#Config shows traversability, viusals of terrain types
terrain_configs = {"grass":{"traversable":True, "emoji":"🟩"},
           "tree":{"traversable":False, "emoji":"🌳"},
           "water":{"traversable":False, "emoji":"🌊"},
           "ground":{"traversable":True, "emoji":"🟫"}}


npc_configs = {"blacksmith":{"health":600, "emoji":"👲", "speed" :80}, 
               "nurse":{"health":200, "emoji":"👩‍⚕️","speed" :55}, 
               "hunter":{"health":800, "emoji":"🥷","speed" :200}, 
               "baker":{"health":200, "emoji":"🧑‍🍳","speed" :60},
               "villager":{"health":200, "emoji":"👩‍🌾","speed" :50}}

direction_configs = ((0, -1), (0, 1), (-1, 0), (1, 0), (0,0))

