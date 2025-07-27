import pyautogui as auto
import time
import math
from apple_numbers import get_apple_number
from algorithm import pair_ten_algorithm
import constants as c
from constants import board_map as map


# add numbers into board map
for i in range(c.NUM_APPLES_Y):
    for j in range(c.NUM_APPLES_X):
        # x, y is j, i
        map[i][j] = get_apple_number(j, i)

game_valid = True
optimizing = True
opt_num = 9
# run game while there are still combos left
while (game_valid):
    game_valid = False

    for i in range(c.NUM_APPLES_Y):
        for j in range(c.NUM_APPLES_X):
            # run pair 10 algo optimized numbers (8, 8, 7) first
            if optimizing:
                if map[i][j] == opt_num:
                    if pair_ten_algorithm(j, i):
                        game_valid = True
            else:
                if pair_ten_algorithm(j, i):
                    game_valid = True

    if opt_num > 6:
        opt_num -= 1
    else:
        optimizing = False
