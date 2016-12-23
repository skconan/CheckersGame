import constants as const

class Control:

    def __init__(self):
        pass

    def get_mouse_position_map(self, x, y):
        r, c = -1, -1
        radius_block = (const.BLOCK_SIZE / 2 - 1)**2
        for i in range(0, 8):
            for j in range(0, 8):
                r_squared = (y - (const.TOP_LEFT[1]
                                      - i * const.BLOCK_SIZE))**2
                c_squared = (x - (const.TOP_LEFT[0]
                                      + j * const.BLOCK_SIZE))**2
                radius_mouse = r_squared + c_squared

                if (radius_mouse <= radius_block):
                    r, c = i, j
        return r, c

    def click_in_board(self, x, y):
        if 225 < x < 880 and 25 < y < 680:
            return True
        return False
