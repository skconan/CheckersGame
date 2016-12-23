import arcade.key
import constants as const
from player import Player
from bot import Bot
from score import Score
from control import Control

class Pos:

    def __init__(self, r=0, c=0):
        self.r = r
        self.c = c


class Map:

    def __init__(self):
        super().__init__()
        self.score = Score()
        self.pieces = []
        self.check_select = False
        self.select = Pos(-1, -1)
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
        self.draw_pieces()
        self.score.on_draw()
        if self.eat_status:
            arcade.draw_text("Need to eat", const.SCREEN_WIDTH - 190 , const.SCREEN_HEIGHT/2 + 200, arcade.color.WHITE,22)

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

    def it_is_pieces(self, r, c):
        if not self.out_of_range(r, c) and 1 <= self.board[r][c] <= 16:
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

    def generate_pieces(self):
        self.pieces.append(0)
        pos = Pos()
        for r in range(0, 8):
            pos.r = const.TOP_LEFT[1] - r * const.BLOCK_SIZE
            for c in range(0, 8):
                pos.c = const.TOP_LEFT[0] + c * const.BLOCK_SIZE
                if self.it_is_bot(r, c):
                    self.pieces.append(Player(pos.c, pos.r, 'w'))
                elif self.it_is_player(r, c):
                    self.pieces.append(Player(pos.c, pos.r, 'r'))

    def draw_pieces(self):
        for r in range(0, 8):
            for c in range(0, 8):
                if self.it_is_pieces(r, c):
                    self.pieces[self.board[r][c]].player.draw()

    def update_king(self, r, c):
        if self.it_is_bot(r, c) and r == 7:
            self.pieces[self.board[r][c]].character = 'W'
            self.pieces[self.board[r][c]].update_img()
        elif self.it_is_player(r, c) and r == 0:
            self.pieces[self.board[r][c]].character = 'R'
            self.pieces[self.board[r][c]].update_img()

    def update_pieces(self):
        pos = Pos()
        for r in range(0, 8):
            pos.r = const.TOP_LEFT[1] - r * const.BLOCK_SIZE
            for c in range(0, 8):
                pos.c = const.TOP_LEFT[0] + c * const.BLOCK_SIZE
                if self.it_is_pieces(r, c):
                    self.update_king(r, c)
                    self.pieces[self.board[r][c]
                                ].player.set_position(pos.c, pos.r)

    def get_character(self, number):
        return self.pieces[number].character

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

        elif self.get_character(self.player_select) == 'R' and abs(delta_r) >= 2:
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
            for i, j in const.DIR:
                for ct in range(1, 7):
                    if self.it_is_bot(r + i * ct, c + j * ct):
                        if self.it_is_blank(r + i * (ct + 1),
                                            c + j * (ct + 1)):
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
            self.select.r, self.select.c = r, c
            self.player_select = self.board[r][c]
            self.board[r][c] = 0
            self.check_select = not self.check_select

        elif self.check_select and [self.select.r, self.select.c] == [r, c]:
            self.board[r][c] = self.player_select
            self.check_select = not self.check_select

        elif self.check_select and self.it_is_blank(r, c):
            

            if (self.walk(self.select.r, self.select.c, r, c)
                    and not self.eat_status):
                self.board[r][c] = self.player_select
                self.check_select = not self.check_select
                self.status = "Bot"

            elif self.eat(self.select.r, self.select.c, r, c):
                self.score.increase('p')
                self.board[r][c] = self.player_select
                self.check_select = not self.check_select
                if not self.can_eat(r, c):
                    self.status = "Bot"

        if(self.status == "Bot"):
            self.board = self.bot.play(self.board, self.pieces, self.score)
            self.status = "Player"

        self.update_pieces()

class World:

    def __init__(self):
        self.control = Control()
        self.map = Map()
        self.map.generate_pieces()

    def animate(self, delta):
        self.map.animate(delta)

    def on_mouse_release(self, x, y, button):
        if button == arcade.MOUSE_BUTTON_LEFT and self.control.click_in_board(x, y):
            r, c = self.control.get_mouse_position_map(x, y)
            self.map.select_player(r, c)
            self.left_down = False


class WorldRenderer:

    def __init__(self, world):
        self.world = world

    def on_draw(self):
        self.world.map.on_draw()
