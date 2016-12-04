import arcade
 
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
bg_src = "images/board.fw.png"
class CheckerGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.bg = arcade.Sprite(bg_src)
        self.bg.set_position(1024/2, 700/2)

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
if __name__ == '__main__':
    window = CheckerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()