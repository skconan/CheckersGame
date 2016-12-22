import arcade
import constants as const
from models import World, WorldRenderer


class CheckerGameWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.src = ["images/start.fw.png","images/board.fw.png"]
        self.texture = []
        for src in self.src:
            self.texture.append(arcade.load_texture(src))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT // 2,
                                      self.texture[const.GAME_STATE].width,
                                      self.texture[const.GAME_STATE].height, self.texture[const.GAME_STATE], 0)
        if const.GAME_STATE == 1:
            self.worldRenderer.on_draw()

    def animate(self, delta):
        if const.GAME_STATE == 1:
            self.world.animate(delta)

    def on_mouse_release(self, x, y, button, modifiers):
        if const.GAME_STATE == 0:
            self.world = World()
            self.worldRenderer = WorldRenderer(self.world)
            const.GAME_STATE = 1
        else :
            self.world.on_mouse_release(x, y, button, modifiers)
        
if __name__ == '__main__':
    window = CheckerGameWindow(const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
    arcade.run()
