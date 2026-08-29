from world_objects.world import World 

class Renderer():
    def __init__(self, world_obj: World) -> None:
        self.world_obj = world_obj

    def render(self) -> None:
        render_data = self.world_obj.get_render_data()
        final_obj = ""
        for row in render_data:
            row = "".join(row)
            final_obj += f"{row}\n"
        print(final_obj) 

