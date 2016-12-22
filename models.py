import arcade
import arcade.key
import constants as const
from bot import Bot
from score import Score


class Map:
    
    def __init__(self):
        super().__init__()
        self.score = Score()
        self.player = []
        self.check_select = False
        self.r_select = -1
        self.c_select = -1
        self.player_select = 0
        self.bot = Bot()
        self.status = 'Player'
        self.eat_status = False
        self.board = [[-1, 1, -1, 2, -1, 3, -1, 4],
                      [5, -1, 6, -1, 7, -1, 8, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 9, -1, 10, -1, 11, -1, 12],
                      [13, -1, 14, -1, 15, -1, 16, -1]]
      

    def animate(self, delta):
        pass

    def on_draw(self):
        self.draw_player()
        self.score.on_draw()

    def generate_player(self):
        self.player.append(0)
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= self.board[r][c] <= 8:
                    self.player.append(
                        Player(const.TOP_LEFT[0] + c * const.BLOCK_SIZE, const.TOP_LEFT[1] - r * const.BLOCK_SIZE, 'w'))
                elif 8 < self.board[r][c] <= 16:
                    self.player.append(
                        Player(const.TOP_LEFT[0] + c * const.BLOCK_SIZE, const.TOP_LEFT[1] - r * const.BLOCK_SIZE, 'r'))

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
                        const.TOP_LEFT[0] + c * const.BLOCK_SIZE, const.TOP_LEFT[1] - r * const.BLOCK_SIZE)

    def out_of_range(self, r, c):
        if 0 <= r <= 7 and 0 <= c <= 7:
            return False
        return True

    def it_is_bot(self, r, c):
        if not self.out_of_range(r, c) and 1 <= self.board[r][c] <= 8:
            return True
        return False

    def it_is_player(self, r, c):
        if not self.out_of_range(r, c) and 9 <= self.board[r][c] <= 16:
            return True
        return False

    def it_is_blank(self, r, c):
        if not self.out_of_range(r, c) and self.board[r][c] == 0:
            return True
        return False

    def basic_cannot_move(self, dr, dc):
        if (dr == 0 or dc == 0 or abs(dr) != abs(dc)):
            return True
        return False

    def get_character(self, number):
        return self.player[number].character

    def eat(self, r_origin, c_origin, r_current, c_current):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)
        if self.basic_cannot_move(delta_r, delta_c):
            return False
        c_step = int(delta_c / abs(delta_c))
        c_start = c_origin + c_step
        c_stop = c_current - c_step

        r_step = int(delta_r / abs(delta_r))
        r_start = r_origin + r_step
        r_stop = r_current - r_step

        if not self.it_is_bot(r_stop, c_stop):
            return False

        if self.get_character(self.player_select) == 'r' and delta_r == -2:
            self.board[r_stop][c_stop] = 0
            return True

        elif self.get_character(self.player_select) == 'R' and delta_r >= -2:
            for r, c in zip(range(r_start, r_stop, r_step), range(c_start, c_stop, c_step)):
                if not self.it_is_blank(r, c) and r != r_stop:
                    return False
            self.board[r_stop][c_stop] = 0
            return True
        return False

    def walk(self, r_origin, c_origin, r_current, c_current):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)

        if self.basic_cannot_move(delta_r, delta_c):
            return False

        if self.get_character(self.player_select) == 'r' and delta_r == -1:
            return True

        elif self.get_character(self.player_select) == 'R':
            c_step = int(delta_c / abs(delta_c))
            c_start = c_origin + c_step
            c_stop = c_current

            r_step = int(delta_r / abs(delta_r))
            r_start = r_origin + r_step
            r_stop = r_current

            for r, c in zip(range(r_start, r_stop, r_step), range(c_start, c_stop, c_step)):
                if not self.it_is_blank(r, c):
                    return False
            return True

        return False

    def can_eat(self, r, c):
        if self.get_character(self.board[r][c]) == 'r':
            if self.it_is_bot(r - 1, c + 1) and self.it_is_blank(r - 2, c + 2):
                return True
            elif self.it_is_bot(r - 1, c - 1) and self.it_is_blank(r - 2, c - 2):
                return True
        elif self.get_character(self.board[r][c]) == 'R':
            dir = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
            for i, j in dir:
                for ct in range(1, 7):
                    if self.it_is_bot(r + i * ct, c + j * ct):
                        if self.it_is_blank(r + i * (ct + 1), c + j * (ct + 1)):
                            return True
                        else:
                            break
                    if self.it_is_player(r + i * ct, c + j * ct):
                        break
        return False

    def need_to_eat(self):
        for r in range(0, 8):
            for c in range(0, 8):
                if self.it_is_player(r, c) and self.can_eat(r, c):
                    return True
        return False

    def select_player(self, r, c):
        if self.status == "Bot":
            pass
        if not self.check_select and self.board[r][c] > 8:
            self.eat_status = False
            if self.can_eat(r, c) or self.need_to_eat():
                self.eat_status = True
            self.r_select, self.c_select = r, c
            self.player_select = self.board[r][c]
            self.board[r][c] = 0
            self.check_select = not self.check_select
            
        elif self.check_select and [self.r_select, self.c_select] == [r, c]:
            self.board[r][c] = self.player_select
            self.check_select = not self.check_select

        elif self.check_select and self.it_is_blank(r, c):
            if self.walk(self.r_select, self.c_select, r, c) and not self.eat_status:
                self.board[r][c] = self.player_select
                self.check_select = not self.check_select
                self.status = "Bot"

            elif self.eat(self.r_select, self.c_select, r, c):
                self.score.increase('p')
                self.board[r][c] = self.player_select
                self.check_select = not self.check_select
                if not self.can_eat(r, c):
                    self.status = "Bot"

        if(self.status == "Bot"):
            self.board = self.bot.play(self.board, self.player, self.score)
            self.status = "Player"
        print(self.status)
        self.update_player()

class Control:

    def __init__(self):
        pass

    def get_mouse_position_map(self, x, y):
        r, c = -1, -1
        for i in range(0, 8):
            for j in range(0, 8):
                if ((x - (const.TOP_LEFT[0] + j * const.BLOCK_SIZE))**2 + (y - 
                (const.TOP_LEFT[1] - i * const.BLOCK_SIZE))**2 <= (const.BLOCK_SIZE / 2 - 1)**2):
                    r, c = i, j
        return r, c
    
    def click_in_board(self, x, y):
        if 200 < x < 830 and 40 < y < 670:
            return True
        return False

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
        

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.control.click_in_board(x, y):
            r, c = self.control.get_mouse_position_map(x, y)
            self.map.select_player(r, c)
            self.left_down = False


class WorldRenderer:

    def __init__(self, world):
        self.world = world

    def on_draw(self):
        self.world.map.on_draw()