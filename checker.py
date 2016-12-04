import arcade
 
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
TOP_LEFT = (235, SCREEN_HEIGHT-75) 
BOTTOM_LEFT = (235, 75) 
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
bg_src = "images/board.fw.png"
white_player_src = "images/player00.fw.png"
red_player_src = "images/player01.fw.png"
white_player_list=[]
red_player_list=[]

class WhitePlayer():
    def __init__(self, x, y):
        self.player = arcade.Sprite(white_player_src)
        self.player.set_position(x, y)
        self.player.draw()

class RedPlayer():
    def __init__(self, x, y):
        self.player = arcade.Sprite(red_player_src)
        self.player.set_position(x, y)
        self.player.draw()

class CheckerGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.bg = arcade.Sprite(bg_src)
        self.bg.set_position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        
    def draw_player(self):
        global red_player_list, white_player_list, board
        for r in range (0, 8):
            for c in range (0, 8):
                if board[r][c] == "w":
                    white_player_list.append(WhitePlayer(TOP_LEFT[0]+c*79, TOP_LEFT[1]-r*79))
                elif board[r][c] == "r":
                    red_player_list.append(RedPlayer(TOP_LEFT[0]+c*79, TOP_LEFT[1]-r*79))

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self.draw_player()

if __name__ == '__main__':
    window = CheckerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()