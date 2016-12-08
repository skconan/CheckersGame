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

    def calculate_score(self, board_origin, r, c, i, j):
        if 0 <= r + i < 8 and 0 <= c + j < 8:
            if board_origin[r+i][c+j] == 0:
                return 1
            elif board_origin[r+i][c+j] > 8:
                return 2
        return 0

    def new_board(self, board_origin):
        max = Node()
        for r in range(0, 8):
            for c in range(0, 8):
                if 1 <= board_origin[r][c] <= 8:
                    print(board_origin[r][c])
                    for i, j in [[1, -1], [1, 1]]:
                        score = self.calculate_score(board_origin, r, c, i, j)
                        if(score > max.score):
                            print(r, c, r + i, c + j)
                            max = Node(board_origin[r][c], score, r, c, r + i, c + j)
                            # print(max)
        # print(max.number,max.r_origin,max.c_origin,max.r_current,max.c_current,max.score)
        board_origin[max.r_origin][max.c_origin] = 0
        board_origin[max.r_current][max.c_current] = max.number
        return board_origin

    def print_board(self, board):
        for i in range(0, 8):
            print(board[i])

    def play(self, board_origin):
        self.print_board(board_origin)
        tmp = self.new_board(board_origin)
        self.print_board(tmp)
        return tmp


class Node():

    def __init__(self, number=0, score=0, r_origin=0, c_origin=0, r_current=0, c_current=0):
        self.number = number
        self.score = score
        self.r_origin = r_origin
        self.c_origin = c_origin
        self.r_current = r_current
        self.c_current = c_current
