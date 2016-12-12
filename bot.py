class Bot():

    def __init__(self):
        self.board = []
        self.player = []

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

    def get_character(self, number):
        return self.player[number].character

    def can_eat(self, r, c):
        if self.get_character(self.board[r][c]) == 'w':
            if self.it_is_player(r + 1, c + 1) and self.it_is_blank(r + 2, c + 2):
                print("w ", r, c, "can eat")
                return r + 2, c + 2, r + 1, c + 1,  True
            elif self.it_is_player(r + 1, c - 1) and self.it_is_blank(r + 2, c - 2):
                print("w ", r, c, "can eat")
                return r + 2, c - 2, r + 1, c - 1, True

        elif self.get_character(self.board[r][c]) == 'W':
            print("W ", r, c, "maybe eat")
            dir = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
            for i, j in dir:
                for ct in range(1, 7):
                    if self.it_is_player(r + i * ct, c + j * ct):
                        if self.it_is_blank(r + i * (ct + 1), c + j * (ct + 1)):
                            print("W ", r, c, "can eat")
                            return r + i * (ct + 1), c + j * (ct + 1), r + i * ct, c + j * ct, True
                        else:
                            break
                    elif self.it_is_bot(r + i * ct, c + j * ct):
                        break
        return 0, 0, 0, 0, False

    def player_can_eat(self, r, c):
        if self.it_is_player(r + 1, c + 1) or self.it_is_player(r + 1, c - 1):
            return True
        return False

    def can_walk(self, r, c):
        if self.get_character(self.board[r][c]) == 'w':
            if self.it_is_blank(r + 1, c + 1):
                print("w ", r, c, "can walk")
                return r + 1, c + 1,  True
            elif self.it_is_blank(r + 1, c - 1):
                print("w ", r, c, "can walk")
                return r + 1, c - 1, True

        # elif self.get_character(self.board[r][c]) == 'W':
            # print("W ", r, c, "maybe eat")
            # dir = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
            # for i, j in dir:
            #     for ct in range(1, 7):
            #         if self.it_is_player(r + i * ct, c + j * ct):
            #             if self.it_is_blank(r + i * (ct + 1), c + j * (ct + 1)):
            #                 print("W ", r, c, "can eat")
            #                 return r + i * (ct + 1), c + j * (ct + 1), r + i * ct, c + j * ct, True
            #             else:
            #                 break
            #         elif self.it_is_bot(r + i * ct, c + j * ct):
            #             break
        return 0, 0, False

    def new_board(self):
        print("new_board")
        max = Node()
        for r in range(0, 8):
            for c in range(0, 8):
                if not self.it_is_bot(r, c):
                    continue
                score = 0
                r_current, c_current, r_eat, c_eat, eat_status = self.can_eat(
                    r, c)
                if eat_status:
                    if self.player_can_eat(r_current, c_current):
                        score = 3
                    else:
                        score = 4
                else:
                    r_current, c_current, walk_status = self.can_walk(
                        r, c)
                    if walk_status:
                        if self.player_can_eat(r_current, c_current):
                            score = 1
                        else:
                            score = 2

                if(score > max.score):
                    if score == 1 or score == 2:
                        max = Node(self.board[r][
                            c], score, r, c, r_current, c_current)
                    elif score == 3 or score == 4:
                        max = Node(self.board[r][
                            c], score, r, c, r_current, c_current, r_eat, c_eat)

                    # print(max)
        print("number", max.number, "origin ", max.r_origin, max.c_origin,
              "current ", max.r_current, max.c_current, "score ", max.score)
        self.board[max.r_origin][max.c_origin] = 0
        if max.score >= 3:
            self.board[max.r_eat][max.c_eat] = 0
        self.board[max.r_current][max.c_current] = max.number

    def print_board(self, board):
        for i in range(0, 8):
            print(self.board[i])

    def play(self, board_origin, player_origin):
        # self.print_board(board_origin)
        self.board = board_origin
        self.player = player_origin
        self.new_board()
        # self.print_board(tmp)
        return self.board


class Node():

    def __init__(self, number=0, score=0, r_origin=0, c_origin=0, r_current=0, c_current=0, r_eat=0, c_eat=0):
        self.number = number
        self.score = score
        self.r_origin = r_origin
        self.c_origin = c_origin
        self.r_current = r_current
        self.c_current = c_current
        self.r_eat = r_eat
        self.c_eat = c_eat
