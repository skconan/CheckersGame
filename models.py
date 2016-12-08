import arcade
import arcade.key
from bot import Bot

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
BLOCK_SIZE = 79
TOP_LEFT = (237, SCREEN_HEIGHT - 75)
BOTTOM_LEFT = (237, 73)

src = {"white_player": "images/player00.fw.png",
       "white_king": "images/player00-k.fw.png",
       "red_player": "images/player01.fw.png",
       "red_king": "images/player01-k.fw.png"}


class Map:

    def __init__(self):
        self.check_select = False
        self.position_select = [-1, -1]
        self.player = []
        self.player_select = 0
        self.bot = Bot()
        self.board = [[-1, 1, -1, 2, -1, 3, -1, 4],
                      [5, -1, 6, -1, 7, -1, 8, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 9, -1, 10, -1, 11, -1, 12],
                      [13, -1, 14, -1, 15, -1, 16, -1]]

        for r in range(0, 8):
            print(self.board[r])

    def animate(self, delta):
        self.update_player()

    def on_draw(self):
        self.draw_player()

    def new_player(self):
        self.player.append(0)
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 8:
                    self.player.append(
                        Player(TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE, 'w'))
                elif 8 < self.board[r][c] <= 16:
                    self.player.append(
                        Player(TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE, 'r'))

    def draw_player(self):
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 16:
                    self.player[self.board[r][c]].player.draw()
    
    def update_player(self):
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 16:
                    self.player[self.board[r][c]].player.set_position(TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE)


    def select_player(self, r, c):
        if not self.check_select and self.board[r][c] > 8:
            print("select", r, c)
            self.position_select = [r, c]
            self.player_select = self.board[r][c]
            self.board[r][c] = 0
            self.check_select = not self.check_select
        elif (self.check_select and 0 <= self.board[r][c] <= 8
              and self.position_select[0] - 1 <= r <= self.position_select[0]
              and self.position_select[1] - 1 <= c <= self.position_select[1] + 1):
            print("release", r, c)
            self.board[r][c] = self.player_select
            self.check_select = not self.check_select
            self.board = self.bot.play(self.board)


class Control:
    DIR_DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_map = 0
        self.y_map = 7

    def get_mouse_position_map(self, x, y):
        r, c = -1, -1
        for i in range(0, 8):
            for j in range(0, 8):
                if (x - (TOP_LEFT[0] + j * BLOCK_SIZE))**2 + (y - (TOP_LEFT[1] - i * BLOCK_SIZE))**2 <= (BLOCK_SIZE / 2 - 1)**2:
                    r, c = i, j
                    print(r, c)
        return r, c


class Player():

    def __init__(self, x, y, character):
        if character == 'w':
            self.player = arcade.Sprite(src['white_player'])
        elif character == 'W':
            self.player = arcade.Sprite(src['white_king'])
        elif character == 'r':
            self.player = arcade.Sprite(src['red_player'])
        elif character == 'R':
            self.player = arcade.Sprite(src['red_king'])
        self.player.set_position(x, y)
        self.character = character


class World:

    def __init__(self, BOTTOM_LEFT):
        self.control = Control(BOTTOM_LEFT[0], BOTTOM_LEFT[1])
        self.map = Map()
        self.map.new_player()

    def animate(self, delta):
        self.map.animate(delta)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and 200 < x < 830 and 40 < y < 670:
            self.left_down = False
            r, c = self.control.get_mouse_position_map(x, y)
            self.map.select_player(r, c)


class WorldRenderer:

    def __init__(self, world):
        self.world = world

    def on_draw(self):
        self.world.map.on_draw()
