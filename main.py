import pyautogui as auto
import time
import math

TOP_LEFT_X = 952
TOP_LEFT_Y = 230

APPLE_WIDTH = 36

NUM_APPLES_X = 17
NUM_APPLES_Y = 10

TIMER_X = 1625
TIMER_Y = 580

board = auto.screenshot()

board_map = [[0]*NUM_APPLES_X for i in range(NUM_APPLES_Y)]

def white_count(x, y, row):
    count = 0
    if y == 0 or y == 1:
        row-=2
    if y == 2 or y == 3 or y == 4:
        row-=1
    if y == 8 or y == 9:
        row+=1
    for i in range(17):
        px = board.getpixel((TOP_LEFT_X + x * APPLE_WIDTH + 10 + i, TOP_LEFT_Y + y * APPLE_WIDTH + row))
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


# add numbers into board map
for i in range(NUM_APPLES_Y):
    for j in range(NUM_APPLES_X):
        # x, y is j, i
        board_map[i][j] = get_apple_number(j, i)



def move_mouse(from_x, from_y, to_x, to_y):
    
    if to_x > from_x: # dragging to the right
        from_pixel_x = TOP_LEFT_X + from_x * APPLE_WIDTH - 5
        to_pixel_x = TOP_LEFT_X + to_x * APPLE_WIDTH + APPLE_WIDTH + 7
    else: # dragging to the left
        from_pixel_x = TOP_LEFT_X + from_x * APPLE_WIDTH + APPLE_WIDTH + 7
        to_pixel_x = TOP_LEFT_X + to_x * APPLE_WIDTH - 5

    if to_y > from_y: # dragging down
        from_pixel_y = TOP_LEFT_Y + from_y * APPLE_WIDTH - 5
        to_pixel_y = TOP_LEFT_Y + to_y * APPLE_WIDTH + APPLE_WIDTH + 7
    else: # dragging up
        from_pixel_y = TOP_LEFT_Y + from_y * APPLE_WIDTH + APPLE_WIDTH + 7
        to_pixel_y = TOP_LEFT_Y + to_y * APPLE_WIDTH - 5

    auto.moveTo(from_pixel_x, from_pixel_y, duration=.05)
    multiplier = max(abs(from_x - to_x), abs(from_y - to_y))
    auto.dragTo(to_pixel_x, to_pixel_y, .3*multiplier, auto.easeOutQuad, button="left")

    x = min(from_x, to_x)
    ox = max(from_x, to_x)
    y = min(from_y, to_y)
    oy = max(from_y, to_y)

    for i in range(x, ox + 1): # set all between to 0
        for j in range(y, oy + 1):
                board_map[j][i] = 0
    return True


def pair_ten_algorithm(x, y):
    # return if theres no apple
    if board_map[y][x] == 0:
        return False
    
    curr_num = board_map[y][x]
    #print(curr_num)

    # check all surrounding apples if add up to 10
    # right -> down -> left -> up
    temp_x = x + 1
    temp_y = y
    temp_sum = curr_num
    while temp_x < 17:
        temp_sum += board_map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= board_map[temp_y][temp_x]
            temp_x-=1
            temp_y+=1
            while temp_y < 10 and temp_x > x:
                for i in range(x, temp_x + 1): # sum all in new row
                    temp_sum += board_map[temp_y][i]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(y, temp_y + 1): # sub all in excess row
                            temp_sum -= board_map[i][temp_x]
                        temp_x-=1
                        if temp_sum == 10:
                            return move_mouse(x, y, temp_x, temp_y)
                temp_y+=1
            break
        else: # sum is less than 10
            temp_x+=1
    
    temp_x = x
    temp_y = y + 1
    temp_sum = curr_num
    while temp_y < 10:
        temp_sum += board_map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= board_map[temp_y][temp_x]
            temp_x-=1
            temp_y-=1
            while temp_x >= 0 and temp_y > y:
                for i in range(y, temp_y + 1): # sum all in new row
                    temp_sum += board_map[i][temp_x]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(temp_x, x + 1): # sub all in excess row
                            temp_sum -= board_map[temp_y][i]
                        temp_y-=1
                        if temp_sum == 10:
                            return move_mouse(x, y, temp_x, temp_y)
                temp_x-=1
            break
        else: # sum is less than 10
            temp_y+=1


    temp_x = x - 1
    temp_y = y
    temp_sum = curr_num
    while temp_x >= 0:
        temp_sum += board_map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= board_map[temp_y][temp_x]
            temp_x+=1
            temp_y-=1
            while temp_y >=0 and temp_x < x:
                for i in range(temp_x, x + 1): # sum all in new row
                    temp_sum += board_map[temp_y][i]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(temp_y, y + 1): # sub all in excess row
                            temp_sum -= board_map[i][temp_x]
                        temp_x+=1
                        if temp_sum == 10:
                            return move_mouse(x, y, temp_x, temp_y)
                temp_y-=1
            break
        else: # sum is less than 10
            temp_x-=1

    temp_x = x
    temp_y = y - 1
    temp_sum = curr_num
    while temp_y >= 0:
        temp_sum += board_map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= board_map[temp_y][temp_x]
            temp_x+=1
            temp_y+=1
            while temp_x < 17 and temp_y < y:
                for i in range(temp_y, y + 1): # sum all in new row
                    temp_sum += board_map[i][temp_x]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(x, temp_x + 1): # sub all in excess row
                            temp_sum -= board_map[temp_y][i]
                        temp_y+=1
                        if temp_sum == 10:
                            return move_mouse(x, y, temp_x, temp_y)
                temp_x+=1
            break
        else: # sum is less than 10
            temp_y-=1
    return False

# while timer is not out
TIMER_GREEN = (24, 204, 112)
timer_px = board.getpixel((TIMER_X, TIMER_Y))
game_valid = True
optimizing = True
curr_num = 9
while (game_valid):
    game_valid = False
    # find 9s first etc.
    for i in range(NUM_APPLES_Y):
        for j in range(NUM_APPLES_X):
            # run pair 10 algo
            if optimizing:
                if board_map[i][j] == curr_num:
                    if pair_ten_algorithm(j, i):
                        game_valid = True
            else:
                if pair_ten_algorithm(j, i):
                    game_valid = True

    if curr_num > 6:
        curr_num -= 1
    else:
        optimizing = False
