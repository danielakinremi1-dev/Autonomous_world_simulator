from world_objects.configs import DEFAULT_MAP_CONFIG
from world_objects.world import World
from world_objects.simulator import Simulator


def main():
    print("Hello from autonomous-world-simulator!")
    world = World(DEFAULT_MAP_CONFIG)
    world.spawn_npc()
    sim = Simulator(world)
    sim.run()


if __name__ == "__main__":
    main()
