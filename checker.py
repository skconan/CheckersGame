import arcade
from models import Control


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
BOTTOM_LEFT = (237, 73)

src = {"bg": "images/board.fw.png",
       "control": "images/control.fw.png",
       "select": "images/select.fw.png"}


class CheckerGameWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.bg = arcade.Sprite(src['bg'])
        self.bg.set_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.control = Control(BOTTOM_LEFT[0], BOTTOM_LEFT[1])
        self.control_sprite = arcade.Sprite(src['control'])
        # self.

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self.control_sprite.draw()
                
    def animate(self, delta):
        control = self.control
        control.animate()
        self.control_sprite.set_position(control.r, control.c)


if __name__ == '__main__':
    window = CheckerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
