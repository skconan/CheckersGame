import arcade
from models import World, WorldRenderer

SCREEN_WIDTH = 1098
SCREEN_HEIGHT = 700


class CheckerGameWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.src = {"bg": "images/board.fw.png"}
        self.bg = arcade.load_texture(self.src['bg'])
        self.world = World()
        self.worldRenderer = WorldRenderer(self.world)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      self.bg.width,
                                      self.bg.height, self.bg, 0)
        self.worldRenderer.on_draw()

    def animate(self, delta):
        self.world.animate(delta)

    def on_mouse_release(self, x, y, button, modifiers):
        self.world.on_mouse_release(x, y, button, modifiers)

if __name__ == '__main__':
    window = CheckerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
