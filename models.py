import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
TOP_LEFT = (235, SCREEN_HEIGHT - 75)
BOTTOM_LEFT = (237, 73)

src = {"white_player": "images/player00.fw.png",
       "red_player": "images/player01.fw.png"}
white_player_list = []
red_player_list = []
board = [
    ".w.w.w.w",
    "w.w.w.w.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".r.r.r.r",
    "r.r.r.r."
]
board_control = [
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
    "x.......",
]


class Control:

    def __init__(self, r, c):
        self.r = r
        self.c = c

    def animate(self):
        if False :
            self.r += 5

class player:

    def draw_player(self):
        global red_player_list, white_player_list, board
        for r in range(0, 8):
            for c in range(0, 8):
                if board[r][c] == "w":
                    white_player_list.append(WhitePlayer(
                        TOP_LEFT[0] + c * 79, TOP_LEFT[1] - r * 79))
                elif board[r][c] == "r":
                    red_player_list.append(
                        RedPlayer(TOP_LEFT[0] + c * 79, TOP_LEFT[1] - r * 79))


class WhitePlayer():

    def __init__(self, x, y):
        self.player = arcade.Sprite(src['white_player'])
        self.player.set_position(x, y)
        self.player.draw()


class RedPlayer():

    def __init__(self, x, y):
        self.player = arcade.Sprite(src['red_player'])
        self.player.set_position(x, y)
        self.player.draw()
