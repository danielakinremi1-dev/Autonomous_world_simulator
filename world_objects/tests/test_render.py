 
from world_objects.world import World
from world_objects.renderer import Renderer
import pytest

def test_renderer_outputs_multiple_rows(capsys):
    test_map = [
        ["grass", "grass"],
        ["tree", "water"],
    ]
    renderer = Renderer(World(test_map))
    renderer.render()
    captured = capsys.readouterr()
    assert captured.out.strip() == "🟩🟩\n🌳🌊"


from world_objects.world import World
from world_objects.renderer import Renderer 


TEST_MAP = [
    ["ground", "ground", "ground"],
    ["ground", "ground", "ground"],
    ["grass",  "grass",  "grass"],
]


def test_render_data_contains_spawned_npc_visuals():
    world = World(TEST_MAP)
    world.spawn_npc()

    render_data = world.get_render_data()

    rendered_visuals = [
        visual
        for row in render_data
        for visual in row
    ]

    for npc in world.npcs:
        assert npc.get_visual() in rendered_visuals


def test_npc_visual_replaces_terrain_visual():
    world = World(TEST_MAP)
    world.spawn_npc()

    for npc in world.npcs:
        assert world.get_render_data()[npc.y][npc.x] == npc.get_visual()


def test_renderer_prints_npc_visuals(capsys):
    world = World(TEST_MAP)
    world.spawn_npc()

    renderer = Renderer(world)
    renderer.render()

    captured = capsys.readouterr()

    for npc in world.npcs:
        assert npc.get_visual() in captured.out



TEST_MAP = [
    ["ground", "ground", "ground"],
    ["ground", "ground", "ground"],
    ["grass",  "grass",  "grass"],
]


world = World(TEST_MAP)
world.spawn_npc()

renderer = Renderer(world)
renderer.render()