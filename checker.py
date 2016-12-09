import arcade
from models import World, Control, Map, WorldRenderer


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
BOTTOM_LEFT = (237, 73)

src = {"bg": "images/board.fw.png",
       "control": "images/control.fw.png",
       "select": "images/select.fw.png"}


class ModelSprite(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class CheckerGameWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.bg = arcade.Sprite(src['bg'])
        self.bg.set_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.world = World()
        self.worldRenderer = WorldRenderer(self.world)

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self.worldRenderer.on_draw()
 
    def animate(self, delta):
        self.world.animate(delta)

    def on_mouse_release(self, x, y, button, modifiers):
        self.world.on_mouse_release(x, y, button, modifiers)

if __name__ == '__main__':
    window = CheckerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
