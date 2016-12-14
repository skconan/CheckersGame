import arcade
from models import World, WorldRenderer


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700


class CheckerGameWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.src = {"bg": "images/board.fw.png"}
        self.bg = arcade.Sprite(self.src['bg'])
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
