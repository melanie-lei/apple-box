import pyautogui as auto
import constants as c

board = auto.screenshot()

def white_count(x, y, row):
    count = 0
    # tweaks which pixels it looks at based on row
    if y == 0 or y == 1:
        row-=2
    if y == 2 or y == 3 or y == 4:
        row-=1
    if y == 8 or y == 9:
        row+=1
    for i in range(17):
        px = board.getpixel((c.TOP_LEFT_X + x * c.APPLE_WIDTH + 10 + i, c.TOP_LEFT_Y + y * c.APPLE_WIDTH + row))
        if px[0] > 210 and px[1] > 165 and px[2] > 165: # px is white
            count+=1
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

