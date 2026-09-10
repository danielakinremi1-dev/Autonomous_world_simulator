import time
import os
from world_objects.renderer import Renderer


class Simulator:
    def __init__(self, world, fps=1):
        self.world = world
        self.renderer = Renderer(world)
        self.fps = fps

    def tick(self):
        self.world.advance_world()
        print("\033[H", end="")
        self.renderer.render()

    def run(self):
        print("\033[2J\033[H", end="")
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            self.tick()
            time.sleep(1 / self.fps)
