from world_objects.constants import DEFAULT_MAP
from world_objects.world import World
from world_objects.renderer import Renderer
from world_objects.simulator import Simulator

def main():
    print("Hello from autonomous-world-simulator!")
    world = World(DEFAULT_MAP) 
    world.spawn_npc() 
    sim = Simulator(world)
    sim.run()

if __name__ == "__main__":
    main()
