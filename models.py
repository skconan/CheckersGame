import arcade
import arcade.key

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
BLOCK_SIZE = 79
TOP_LEFT = (237, SCREEN_HEIGHT - 75)
BOTTOM_LEFT = (237, 73)

src = {"white_player": "images/player00.fw.png",
       "red_player": "images/player01.fw.png"}


class Map:

    def __init__(self):
        self.check_select = False
        self.position_select = [-1, -1]
        self.board = []
        self.player = []
        self.player_select = 0
        self.board_str = [
            '.w.w.w.w',
            'w.w.w.w.',
            '.-.-.-.-',
            '-.-.-.-.',
            '.-.-.-.-',
            '-.-.-.-.',
            '.r.r.r.r',
            'r.r.r.r.',
        ]
        count = 1
        for r in range(0, 8):
            self.board.append([])
            for c in range(0, 8):
                if self.board_str[r][c] == "w":
                    self.board[r].append(count)
                    count += 1
                elif self.board_str[r][c] == "r":
                    self.board[r].append(count)
                    count += 1
                elif self.board_str[r][c] == "-":
                    self.board[r].append(0)
                else:
                    self.board[r].append(-1)
        for r in range(0, 8):
            print(self.board[r])

    def animate(self, delta):
        if len(self.player) > 0:
            def on_mouse_release(self, x, y, button, modifiers):
                self.player[1].on_mouse_release(x, y, button, modifiers)

    def draw_player(self):
        count = 1
        self.player.append(0)
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 8:
                    self.player.append(
                        Player(TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE, 'w'))
                elif 8 < self.board[r][c] <= 16:
                    self.player.append(
                        Player(TOP_LEFT[0] + c * BLOCK_SIZE, TOP_LEFT[1] - r * BLOCK_SIZE, 'r'))

    def select(self, r, c):
        if not self.check_select and self.board[r][c] > 8:
            print("select", r, c)
            self.position_select = [r, c]
            self.player_select = self.board[r][c]
            self.board[r][c] = 0
            self.check_select = not self.check_select
        elif (self.check_select and 0 <= self.board[r][c] <= 8 and r == self.position_select[0] - 1
              and self.position_select[1] - 1 <= c <= self.position_select[1] + 1):
            print("release", r, c)
            self.board[r][c] = self.player_select
            self.check_select = not self.check_select


class Control:
    DIR_DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_map = 0
        self.y_map = 7

    def move(self, dir):
        if 8 > self.x_map + self.DIR_DIRECTION[dir][0] >= 0:
            self.x += BLOCK_SIZE * self.DIR_DIRECTION[dir][0]
            self.x_map += self.DIR_DIRECTION[dir][0]
        if 8 > self.y_map + self.DIR_DIRECTION[dir][1] >= 0:
            self.y += BLOCK_SIZE * -self.DIR_DIRECTION[dir][1]
            self.y_map += self.DIR_DIRECTION[dir][1]

    def get_mouse_position_map(self, x, y):
        r, c = -1, -1
        for i in range(0, 8):
            for j in range(0, 8):
                if (x - (TOP_LEFT[0] + j * BLOCK_SIZE))**2 + (y - (TOP_LEFT[1] - i * BLOCK_SIZE))**2 <= (BLOCK_SIZE / 2 - 1)**2:
                    r, c = i, j
                    print(r, c)
        return r, c


class Player():

    def __init__(self, x, y, color):
        if color == 'w':
            self.player = arcade.Sprite(src['white_player'])
        else:
            self.player = arcade.Sprite(src['red_player'])
        self.player.set_position(x, y)
        self.player.draw()
        self.color = color


class World:

    def __init__(self, BOTTOM_LEFT):
        self.control_player = Control(BOTTOM_LEFT[0], BOTTOM_LEFT[1])
        self.map = Map()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and 200 < x < 830 and 40 < y < 670:
            self.left_down = False
            r, c = self.control_player.get_mouse_position_map(x, y)
            self.map.select(r, c)
