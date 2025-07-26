import pyautogui as auto
import time
import math

top_left_x = 952
top_left_y = 230
#, 982, 230
apple_width = 36
# 36

num_apples_x = 17
num_apples_y = 10

timer_x = 1625
timer_y = 580

board = auto.screenshot()

board_map = [[0]*num_apples_x for i in range(num_apples_y)]

# timerpx = board.getpixel((timer_x, timer_y)) # (24, 204, 112)

#print(timerpx)

def white_count(x, y, row):
    count = 0
    if y == 0 or y == 1:
        row-=2
    if y == 2 or y == 3 or y == 4:
        row-=1
    if y == 8 or y == 9:
        row+=1
    for i in range(17):
        px = board.getpixel((top_left_x + x * apple_width + 10 + i, top_left_y + y * apple_width + row))
        #print(top_left_x + x * apple_width + 10 + i, end=" ")
        #print(top_left_y + y * apple_width + row, end=" ")
        #print(px, end=" ")
        if px[0] > 210 and px[1] > 165 and px[2] > 165: # px is white
            count+=1
    #print("\n")
    #print("row and count")
    #print(row)
    #print(count)
    return count

def get_apple_number(x, y):

    if white_count(x, y, 24) < 5:
        if white_count(x, y, 14) > 6:
            return 7
        else:
            return 4
    else:
        if white_count(x, y, 16) > 5:
            if white_count(x, y, 22) >= 6:
                return 8
            else:
                return 9
        else:
            if white_count(x, y, 22) > 5:
                return 6
            elif white_count(x, y, 18) > 6:
                return 5
            elif white_count(x, y, 20) > 4:
                return 3
            elif white_count(x, y, 25) > 8 and white_count(x, y, 14) > 6:
                return 2
            else:
                return 1



for i in range(num_apples_y):
    for j in range(num_apples_x):
        # j , i is x, y coords
        board_map[i][j] = get_apple_number(j, i)
        print(board_map[i][j], end="   ")

    print("\n")



# if +24 is small, 4 or 7
    # if +12 is big, 7
    # else 4
# else
    # if +15 is >= 8? is 8 or 9
        # +21 is >, is 8
        # else 9
    # else is 5, 3, 6, 1, 2
        # if + 21 is >, is 6
        # else if + 12 > 10?, is 5
        # else if + 17 is >6, is 3
        # else if +15 > 8, is 2
        # else is 1

# 5, (25, 20), (30, 30) NOT(20, 30) (25, 37)


# 8, (25, 20)

# find all pairs?