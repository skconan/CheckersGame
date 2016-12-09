import arcade
import arcade.key
from bot import Bot

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
BLOCK_SIZE = 79
TOP_LEFT = (237, SCREEN_HEIGHT - 75)
BOTTOM_LEFT = (237, 73)


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

    def generate_player(self):
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
                    self.player[self.board[r][c]].player.set_position(
                        TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE)

    def eat(self, r_origin, c_origin, r_current, c_current):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)
        r_white, c_white = r_origin + \
            int(delta_r / 2), c_origin + int(delta_c / 2)
        if delta_r == -2 and abs(delta_c) == 2 and 1 <= self.board[r_white][c_white] <= 8:
            self.board[r_white][c_white] = 0
            return True
        return False

    def walk(self, r_origin, c_origin, r_current, c_current):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)

        if(delta_r == -1 and abs(delta_c) == 1):
            self.board[r_current][c_current] = 0
            return True
        return False

    def select_player(self, r, c):
        if not self.check_select and self.board[r][c] > 8:
            print("select", r, c)
            self.position_select = [r, c]
            self.player_select = self.board[r][c]
            self.board[r][c] = 0
            self.check_select = not self.check_select

        elif (self.check_select and self.board[r][c] == 0
              and (self.eat(self.position_select[0], self.position_select[1], r, c)
                   or self.walk(self.position_select[0], self.position_select[1], r, c))):
            print("release", r, c)
            self.board[r][c] = self.player_select
            self.board = self.bot.play(self.board)
            self.check_select = not self.check_select

        elif self.position_select == [r, c]:
            print("release", r, c)
            self.board[r][c] = self.player_select
            self.check_select = not self.check_select


class Control:

    def __init__(self):
        pass

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
        self.src = {"white_player": "images/player00.fw.png",
                    "white_king": "images/player00-k.fw.png",
                    "red_player": "images/player01.fw.png",
                    "red_king": "images/player01-k.fw.png"}

        if character == 'w':
            self.player = arcade.Sprite(self.src['white_player'])
        elif character == 'W':
            self.player = arcade.Sprite(self.src['white_king'])
        elif character == 'r':
            self.player = arcade.Sprite(self.src['red_player'])
        elif character == 'R':
            self.player = arcade.Sprite(self.src['red_king'])
        self.player.set_position(x, y)
        self.character = character


class World:

    def __init__(self):
        self.control = Control()
        self.map = Map()
        self.map.generate_player()

    def animate(self, delta):
        self.map.animate(delta)

    def click_in_board(self, x, y):
        if 200 < x < 830 and 40 < y < 670:
            return True
        return False

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.click_in_board(x, y):
            r, c = self.control.get_mouse_position_map(x, y)
            self.map.select_player(r, c)
            self.left_down = False


class WorldRenderer:

    def __init__(self, world):
        self.world = world

    def on_draw(self):
        self.world.map.on_draw()
