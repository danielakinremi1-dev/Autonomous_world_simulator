from world_objects.constants import DEFAULT_MAP
from world_objects.world import World
from world_objects.renderer import Renderer

def main():
    print("Hello from autonomous-world-simulator!")
    world = World(DEFAULT_MAP)

    world.spawn_npc()

    renderer = Renderer(world)
    renderer.render()

if __name__ == "__main__":
    main()
