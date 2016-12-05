import arcade
import arcade.key

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
BLOCK_SIZE = 79
TOP_LEFT = (235, SCREEN_HEIGHT - 75)
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
            '........',
            '........',
            '........',
            '........',
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
                else:
                    self.board[r].append(0)
        for r in range(0, 8):
            print(self.board[r])

    def animate(self, delta):
        print('a')

    def draw_player(self):
        count = 1
        self.player.append(0)
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 8:
                    self.player.append(
                        Player(TOP_LEFT[0] + c * 79, TOP_LEFT[1] - r * 79, 'w'))
                elif 8 < self.board[r][c] <= 16:
                    self.player.append(
                        Player(TOP_LEFT[0] + c * 79, TOP_LEFT[1] - r * 79, 'r'))

    def select(self, x, y):
        if not self.check_select:
            self.position_select = [x, y]
            self.player_select = self.board[y][x]
            self.board[y][x] = 0
        else :
            self.board[y][x] = self.player_select
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
        self.control = Control(BOTTOM_LEFT[0], BOTTOM_LEFT[1])
        self.map = Map()

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.control.move(0)
        elif key == arcade.key.RIGHT:
            self.control.move(1)
        elif key == arcade.key.UP:
            self.control.move(2)
        elif key == arcade.key.DOWN:
            self.control.move(3)
        elif key == arcade.key.SPACE:
            self.map.select(self.control.x_map, self.control.y_map)
