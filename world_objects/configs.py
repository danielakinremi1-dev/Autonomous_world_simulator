from collections import defaultdict
from world_objects.helper_item_configs import item_configs
from world_objects.items import Item


# Config shows traversability, viusals of terrain types
terrain_configs = {
    "grass": {
        "traversable": True,
        "emoji": "🟩",
        "hp": None,
    },
    "tree": {"traversable": False, "emoji": "🌳", "hp": 10},
    "water": {"traversable": False, "emoji": "🌊", "hp": None},
    "ground": {"traversable": True, "emoji": "🟫", "hp": None},
    "rock": {"traversable": False, "emoji": "🪨", "hp": 100},
    "plant": {"traversable": True, "emoji": "🌿", "hp": 3},
    "wheat": {"traversable": True, "emoji": "🌾", "hp": 3},
}

resource_configs = ["herbs", "stone", "wood", "water", "wheat"]

# Setup npc inventory objects and refactor for dictionary searches

npc_configs = {
    "blacksmith": {
        "health": 400,
        "emoji": "👲",
        "speed": 80,
        "job": "craft",
        "view_radius": 6,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 4),
                "bandages": Item("bandages", 5),
                "axe": Item("axe", 2),
                "pickaxe": Item("pickaxe", 2),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
    "nurse": {
        "health": 300,
        "emoji": "👩‍⚕️",
        "speed": 55,
        "job": "heal",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 4),
                "bandages": Item("bandages", 10),
                "medical equipment": Item("medical equipment"),
            },
        ),
    },
    "hunter": {
        "health": 800,
        "emoji": "🥷",
        "speed": 200,
        "job": "hunt",
        "view_radius": 50,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 6),
                "bandages": Item("bandages", 6),
                "sword": Item("sword"),
                "armor": Item("armor"),
            },
        ),
    },
    "baker": {
        "health": 250,
        "emoji": "🧑‍🍳",
        "speed": 60,
        "job": "bake",
        "view_radius": 7,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 10),
                "bandages": Item("bandages", 4),
                "cooking utensils": Item("cooking utensils"),
            },
        ),
    },
    "villager": {
        "health": 200,
        "emoji": "👩‍🌾",
        "speed": 50,
        "job": "gather",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 3),
                "bandages": Item("bandages", 3),
                "axe": Item("axe", 1),
                "pickaxe": Item("pickaxe", 1),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
    "villager2": {
        "health": 200,
        "emoji": "👩‍🚒",
        "speed": 50,
        "job": "gather",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 3),
                "bandages": Item("bandages", 3),
                "axe": Item("axe", 1),
                "pickaxe": Item("pickaxe", 1),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
    "villager3": {
        "health": 200,
        "emoji": "👩‍🎤",
        "speed": 50,
        "job": "gather",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 3),
                "bandages": Item("bandages", 3),
                "axe": Item("axe", 1),
                "pickaxe": Item("pickaxe", 1),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
    "villager4": {
        "health": 200,
        "emoji": "🧝",
        "speed": 50,
        "job": "gather",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 3),
                "bandages": Item("bandages", 3),
                "axe": Item("axe", 1),
                "pickaxe": Item("pickaxe", 1),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
    "villager5": {
        "health": 200,
        "emoji": "👨‍🔧",
        "speed": 50,
        "job": "gather",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 3),
                "bandages": Item("bandages", 3),
                "axe": Item("axe", 1),
                "pickaxe": Item("pickaxe", 1),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
    "villager6": {
        "health": 200,
        "emoji": "🧕",
        "speed": 50,
        "job": "gather",
        "view_radius": 8,
        "inventory": defaultdict(
            int,
            {
                "food": Item("food", 3),
                "bandages": Item("bandages", 3),
                "axe": Item("axe", 1),
                "pickaxe": Item("pickaxe", 1),
                "smithing hammer": Item("smithing hammer"),
            },
        ),
    },
}

direction_configs = ((0, -1), (0, 1), (-1, 0), (1, 0), (0, 0))

TERRAIN_KEY = {
    "g": "grass",
    ".": "ground",
    "T": "tree",
    "W": "water",
    "R": "rock",
    "P": "plant",
    "H": "wheat",
}


DEFAULT_MAP_LAYOUT = [
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
    "Tggggggggggggggggggggggg..gggggggggggggggggggggggT",
    "Tggggggggggggggggggggggg..gggggggggggggggggggggggT",
    "TgggggggggTTTggggggggggg..gggggTTggggggggggggggggT",
    "TggTTTggggggggTTgggggggg..ggggggTggggggggggggggggT",
    "TggTgggggggggggggggggggg..gggggggggWWWWWgggggggTgT",
    "TgggggTggggggggggggggggg..ggggggggWWWWWWWWWggggTggT",
    "Tggggggg.ggggggggggggggg..gggggggWWWWWWWWWWWgggTggT",
    "Tggggggg..................ggggggggWWWWWWWWWWWggggggT",
    "Tggggggg.ggggggggggggggg..gggPPgggWWWWWWWWWgggggggT",
    "TgggggPggggggggggggggggg..gggPPggggWWWWWWWggggggggT",
    "TggggPgg.gggPPgggggggggg..ggggPgggggWWWgggggggggggT",
    "TggggggP.gggggPggggggggg..gggPggggggggggggggggggggT",
    "Tggggggg.gggPggPgggggggg..ggggggggggggggggggggggggT",
    "Tggggggg.gggggggg..............ggggggggggggRRggggggT",
    "TggTTggg.gggggggg..............ggggggggggggRgggggggT",
    "TgggTTTg.gHHHggggg..............ggggggggggggRRggggggT",
    "Tggggggg.gHHHggggg..............ggPPggggggggggggggggT",
    "Tggggggg.ggggggggg..............gggPggggggggggggggggT",
    "T................................................T",
    "T................................................T",
    "Tggggggg.gggggHHH..............ggggggggggggg.ggggggT",
    "Tggggggg.gggggHHH..............ggggggggggggg.ggggggT",
    "Tggggggg.gPPgggggg..............ggggggggggggg.ggggggT",
    "Tggggggg.gggPggggg..............ggggggggggggg.ggggggT",
    "Tggggggg.ggggggggg..............ggggggggggggg.ggggggT",
    "Tggggggg.ggggggggggggggg..gggggRRRgggggggggg.ggggggT",
    "Tggggggg.gggTTgggggggggg..gggggRRgRggggggggg.ggggggT",
    "Tggggggg.ggggTgggggggggg..ggggRRgRRggggggggg.ggggggT",
    "TggTTggg.gggggTgggggggggg..ggHHHgggggggggggg.ggggggT",
    "TgggTTgg.ggggggTggggggggg..ggHHHgggggggggggg.ggggggT",
    "TgggTggg.gggggggggggggggg..ggggggggggggggggg.ggggggT",
    "Tggggggg.gggggggggggggggg..................gg.ggggggT",
    "Tggggggg.ggggggPPPggggggg..gggggggggggggggTTTggggggT",
    "Tggggggg.ggggggggPPgggggg..gggggggggggggggggTTgggggT",
    "Tggggggg.gggggggggPgggggg..gggggggggggggggTggggggggT",
    "Tggggggg.gggggggggggggggg..ggggggggggggggggggggggggT",
    "Tgggggggggggggggggggggggg..gggggggggggggggggggggggT",
    "Tgggggggggggggggggggggggg..gggggggggggggggggggggggT",
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
]


DEFAULT_MAP_CONFIG = [
    [TERRAIN_KEY[symbol] for symbol in row] for row in DEFAULT_MAP_LAYOUT
]
