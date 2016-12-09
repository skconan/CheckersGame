import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 63
BLOCK_SIZE = 79
TOP_LEFT = (237, SCREEN_HEIGHT - 75)
BOTTOM_LEFT = (237, 73)


class Bot():

    def __init__(self):
        self.board = []
        self.direction = [[1, -1], [1, 1], [2, -2], [2, 2]]

    def check_eat(self, r_origin, c_origin, r_current, c_current, board):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)
        r_white, c_white = r_origin + \
            int(delta_r / 2), c_origin + int(delta_c / 2)
        if delta_r == 2 and abs(delta_c) == 2 and 9 <= board[r_white][c_white] <= 16:
            # self.board[r_white][c_white] = 0
            return True
        return False

    def check_walk(self, r_origin, c_origin, r_current, c_current, board):
        delta_r = (r_current - r_origin)
        delta_c = (c_current - c_origin)

        if(delta_r == 1 and abs(delta_c) == 1):
            # self.board[r_current][c_current] = 0
            return True
        return False

    def calculate_score(self, board, r, c, i, j):
        if self.check_eat(r, c, r+i, c+j, board):
            return 2
        elif self.check_walk(r, c, r+i, c+j, board):
            return 1
        return 0

    def new_board(self, board):
        print ("new_board")
        max = Node()
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= board[r][c] <= 8:
                    # print(board[r][c])
                    for i, j in self.direction:
                        if 0 <= r+i <= 7 and 0 <= c+j <= 7: 
                            if board[r+i][c+j] != 0:
                                score = 0
                            else:
                                score = self.calculate_score(board, r, c, i, j)
                        else :
                            score = 0
                        # print ("direction ",r,c, r+i, c+j,score)
                        if(score > max.score):
                            print(r, c, r + i, c + j)
                            if score == 1:
                                max = Node(board[r][
                                    c], score, r, c, r + i, c + j)
                            elif score == 2:
                                max = Node(board[r][
                                    c], score, r, c, r + i, c + j, r + int(i/2), c + int(j/2))
                            # print(max)
        # print(max.number,max.r_origin,max.c_origin,max.r_current,max.c_current,max.score)
        board[max.r_origin][max.c_origin] = 0
        if max.score == 2:
            board[max.r_eat][max.c_eat] = 0
        board[max.r_current][max.c_current] = max.number
        return board

    def print_board(self, board):
        for i in range(0, 8):
            print(board[i])

    def play(self, board_origin):
        # self.print_board(board_origin)
        tmp = self.new_board(board_origin)
        # self.print_board(tmp)
        return tmp


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
