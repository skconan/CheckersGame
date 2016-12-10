import arcade
import arcade.key
from bot import Bot

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
BLOCK_SIZE = 79
TOP_LEFT = (237, SCREEN_HEIGHT - 75)
BOTTOM_LEFT = (237, 73)


class Map:

    def __init__(self):
        self.player = []
        self.check_select = False
        self.r_select = -1
        self.c_select = -1
        self.player_select = 0
        self.bot = Bot()
        self.status = 'Player'
        self.board = [[-1, 1, -1, 2, -1, 3, -1, 4],
                      [5, -1, 6, -1, 7, -1, 8, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 9, -1, 10, -1, 11, -1, 12],
                      [13, -1, 14, -1, 15, -1, 16, -1]]

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

    def update_king(self, r, c):
        if 1 <= self.board[r][c] <= 8 and r == 7:
            self.player[self.board[r][c]].character = 'W'
            self.player[self.board[r][c]].update_img()
        elif 9 <= self.board[r][c] <= 16 and r == 0:
            self.player[self.board[r][c]].character = 'R'
            self.player[self.board[r][c]].update_img()

    def update_player(self):
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 16:
                    self.update_king(r, c)
                    self.player[self.board[r][c]].player.set_position(
                        TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE)

    def out_of_range(self, r, c):
        if 0 <= r <= 7 and 0 <= c <= 7:
            return False
        return True

    def it_is_bot(self, r, c):
        if self.out_of_range(r, c):
            return False
        elif 1 <= self.board[r][c] <= 8:
            return True
        return False

    def it_is_player(self, r, c):
        if self.out_of_range(r, c):
            return False
        elif 9 <= self.board[r][c] <= 16:
            return True
        return False

    def it_is_blank(self, r, c):
        if self.out_of_range(r, c):
            return False
        elif self.board[r][c] == 0:
            return True
        return False

    def basic_cannot_move(self, dr, dc):
        if (dr == 0 or dc == 0 or abs(dr) != abs(dc)):
            return True
        return False

    def eat(self, r_origin, c_origin, r_current, c_current):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)

        if self.basic_cannot_move(delta_r, delta_c):
            return False

        if self.player[self.player_select].character == 'r' and delta_r == -2 and abs(delta_c) == 2:
            r_white = r_origin + int(delta_r / 2)
            c_white = c_origin + int(delta_c / 2)
            if self.it_is_bot(r_white, c_white):
                self.board[r_white][c_white] = 0
                return True

        elif self.player[self.player_select].character == 'R':
            print('R eat')
            eat_list = []
            c_step = int(delta_c / abs(delta_c))
            c_start = c_origin + c_step
            c_stop = c_current

            r_step = int(delta_r / abs(delta_r))
            r_start = r_origin + r_step
            r_stop = r_current

            check_close = False

            if not self.it_is_bot(r_stop - r_step, c_stop - c_step):
                return False
            for r, c in zip(range(r_start, r_stop, r_step), range(c_start, c_stop, c_step)):
                print("R eat", r, c)
                if self.it_is_bot(r, c):
                    if check_close == False:
                        eat_list.append([r, c])
                        check_close = True
                    else:
                        return False
                elif self.it_is_player(r, c):
                    return False
                elif self.it_is_blank(r, c):
                    check_close = False
                print(check_close)
            if len(eat_list) > 0:
                print("R eatttt")
                for r, c in eat_list:
                    self.board[r][c] = 0
                return True
        return False

    def walk(self, r_origin, c_origin, r_current, c_current):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)

        if self.basic_cannot_move(delta_r, delta_c):
            return False

        if self.player[self.player_select].character == 'r' and delta_r == -1 and abs(delta_c) == 1:
            print("r walk")
            self.board[r_current][c_current] = 0
            return True
        elif self.player[self.player_select].character == 'R':
            print("R walk")
            c_step = int(delta_c / abs(delta_c))
            c_start = c_origin + c_step
            c_stop = c_current

            r_step = int(delta_r / abs(delta_r))
            r_start = r_origin + r_step
            r_stop = r_current

            for r, c in zip(range(r_start, r_stop, r_step), range(c_start, c_stop, c_step)):

                print("R walk", r, c)
                if not self.it_is_blank(r, c):
                    return False

            self.board[r_current][c_current] = 0
            print("R walkkkk")
            return True
        return False

    def can_eat(self, r, c):
        print("can eat", r, c)
        if self.it_is_bot(r - 1, c + 1) and self.it_is_blank(r - 2, c + 2):
            print("c+2", r, c)
            return True
        elif self.it_is_bot(r - 1, c - 1) and self.it_is_blank(r - 2, c - 2):
            print("c-2", r, c)
            return True
        return False

    def select_player(self, r, c):
        if self.status == "Bot":
            pass
        if not self.check_select and self.board[r][c] > 8:
            print("select", r, c)
            self.r_select = r
            self.c_select = c
            self.player_select = self.board[r][c]
            self.board[r][c] = 0
            self.check_select = not self.check_select

        elif self.check_select and [self.r_select, self.c_select] == [r, c]:
            print("release current position : ", r, c)
            self.board[r][c] = self.player_select
            self.check_select = not self.check_select

        elif self.check_select and self.it_is_blank(r, c):
            if self.walk(self.r_select, self.c_select, r, c) and not self.can_eat(self.r_select, self.c_select):
                print("release", r, c)
                self.board[r][c] = self.player_select
                self.check_select = not self.check_select
                self.status = "Bot"
            elif self.eat(self.r_select, self.c_select, r, c):
                print("release", r, c)
                self.board[r][c] = self.player_select
                self.check_select = not self.check_select
                if not self.can_eat(r, c):
                    self.status = "Bot"

        if(self.status == "Bot"):
            self.board = self.bot.play(self.board)
            self.status = "Player"


class Control:

    def __init__(self):
        pass

    def get_mouse_position_map(self, x, y):
        r, c = -1, -1
        for i in range(0, 8):
            for j in range(0, 8):
                if (x - (TOP_LEFT[0] + j * BLOCK_SIZE))**2 + (y - (TOP_LEFT[1] - i * BLOCK_SIZE))**2 <= (BLOCK_SIZE / 2 - 1)**2:
                    r, c = i, j
                    # print(r, c)
        return r, c


class Player():

    def __init__(self, x, y, character):
        self.src = {"white_player": "images/player00.fw.png",
                    "white_king": "images/player00-k.fw.png",
                    "red_player": "images/player01.fw.png",
                    "red_king": "images/player01-k.fw.png"}
        self.character = character
        self.update_img()
        self.player.set_position(x, y)
        self.king = False

    def update_img(self):
        if self.character == 'w':
            self.player = arcade.Sprite(self.src['white_player'])
        elif self.character == 'W' and self.king == False:
            self.player = arcade.Sprite(self.src['white_king'])
            self.king = True
        elif self.character == 'r':
            self.player = arcade.Sprite(self.src['red_player'])
        elif self.character == 'R' and self.king == False:
            self.player = arcade.Sprite(self.src['red_king'])
            self.king = True


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
