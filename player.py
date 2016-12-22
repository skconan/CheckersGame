import arcade


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
