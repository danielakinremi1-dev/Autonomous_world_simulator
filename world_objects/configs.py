
#Config shows traversability, viusals of terrain types
terrain_configs = {"grass":{"traversable":True, "emoji":"🟩"},
           "tree":{"traversable":False, "emoji":"🌳"},
           "water":{"traversable":False, "emoji":"🌊"},
           "ground":{"traversable":True, "emoji":"🟫"}}


npc_configs = {"blacksmith":{"health":60, "emoji":"👲"}, 
               "nurse":{"health":20, "emoji":"👩‍⚕️"}, 
               "hunter":{"health":80, "emoji":"🥷"}, 
               "baker":{"health":20, "emoji":"🧑‍🍳"},
               "villager":{"health":20, "emoji":"👩‍🌾"}}

direction_configs = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "stay" : (0,0)
}
