import time
from world_objects.renderer import Renderer

class Simulator():
    def __init__(self, world):
        self.world = world
        self.renderer = Renderer(world)


    def run(self):
        while True:
            self.world.advance_world()
            self.renderer.render()
            time.sleep(1)


