import pyautogui as auto
import constants as c
from constants import board_map as map


# movem mouse and delete from board
def move_mouse(from_x, from_y, to_x, to_y):
    
    if to_x > from_x: # dragging to the right
        from_pixel_x = c.TOP_LEFT_X + from_x * c.APPLE_WIDTH - 5
        to_pixel_x = c.TOP_LEFT_X + to_x * c.APPLE_WIDTH + c.APPLE_WIDTH + 7
    else: # dragging to the left
        from_pixel_x = c.TOP_LEFT_X + from_x * c.APPLE_WIDTH + c.APPLE_WIDTH + 7
        to_pixel_x = c.TOP_LEFT_X + to_x * c.APPLE_WIDTH - 5

    if to_y > from_y: # dragging down
        from_pixel_y = c.TOP_LEFT_Y + from_y * c.APPLE_WIDTH - 5
        to_pixel_y = c.TOP_LEFT_Y + to_y * c.APPLE_WIDTH + c.APPLE_WIDTH + 7
    else: # dragging up
        from_pixel_y = c.TOP_LEFT_Y + from_y * c.APPLE_WIDTH + c.APPLE_WIDTH + 7
        to_pixel_y = c.TOP_LEFT_Y + to_y * c.APPLE_WIDTH - 5

    auto.moveTo(from_pixel_x, from_pixel_y, duration=.05)
    multiplier = max(abs(from_x - to_x), abs(from_y - to_y))
    auto.dragTo(to_pixel_x, to_pixel_y, .3*multiplier, auto.easeOutQuad, button="left")

    x = min(from_x, to_x)
    ox = max(from_x, to_x)
    y = min(from_y, to_y)
    oy = max(from_y, to_y)

    for i in range(x, ox + 1): # set all between to 0
        for j in range(y, oy + 1):
                map[j][i] = 0
    return True


def pair_ten_algorithm(x, y):
    # return if theres no apple
    if map[y][x] == 0:
        return False

    curr_num = map[y][x]

    # check all surrounding apples if add up to 10
    # right -> down -> left -> up
    temp_x = x + 1
    temp_y = y
    temp_sum = curr_num
    while temp_x < 17:
        temp_sum += map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= map[temp_y][temp_x]
            temp_x-=1
            temp_y+=1
            while temp_y < 10 and temp_x > x:
                for i in range(x, temp_x + 1): # sum all in new row
                    temp_sum += map[temp_y][i]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(y, temp_y + 1): # sub all in excess row
                            temp_sum -= map[i][temp_x]
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
        temp_sum += map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= map[temp_y][temp_x]
            temp_x-=1
            temp_y-=1
            while temp_x >= 0 and temp_y > y:
                for i in range(y, temp_y + 1): # sum all in new row
                    temp_sum += map[i][temp_x]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(temp_x, x + 1): # sub all in excess row
                            temp_sum -= map[temp_y][i]
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
        temp_sum += map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= map[temp_y][temp_x]
            temp_x+=1
            temp_y-=1
            while temp_y >=0 and temp_x < x:
                for i in range(temp_x, x + 1): # sum all in new row
                    temp_sum += map[temp_y][i]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(temp_y, y + 1): # sub all in excess row
                            temp_sum -= map[i][temp_x]
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
        temp_sum += map[temp_y][temp_x]
        if temp_sum == 10: # makes 10
            return move_mouse(x, y, temp_x, temp_y)
        elif temp_sum > 10: # 10 isnt possible
            temp_sum -= map[temp_y][temp_x]
            temp_x+=1
            temp_y+=1
            while temp_x < 17 and temp_y < y:
                for i in range(temp_y, y + 1): # sum all in new row
                    temp_sum += map[i][temp_x]
                if temp_sum == 10:
                    return move_mouse(x, y, temp_x, temp_y)
                if temp_sum > 10:
                    while temp_sum > 10:
                        for i in range(x, temp_x + 1): # sub all in excess row
                            temp_sum -= map[temp_y][i]
                        temp_y+=1
                        if temp_sum == 10:
                            return move_mouse(x, y, temp_x, temp_y)
                temp_x+=1
            break
        else: # sum is less than 10
            temp_y-=1
    return False
