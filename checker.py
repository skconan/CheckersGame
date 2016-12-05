import arcade
from models import World, Control, Map


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
        self.world = World(BOTTOM_LEFT)
        self.map = self.world.map
        self.control_sprite = ModelSprite(
            src['control'], model=self.world.control)
       
    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self.control_sprite.draw()
        self.map.draw_player()
    
    def animate(self, delta):
        self.map.animate(delta)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

if __name__ == '__main__':
    window = CheckerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
