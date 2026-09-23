room_code = "aafyuytuyyyyuudsadf"

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import json

class Move:
    xi: int
    yi: int
    xf: int
    yf: int


    def __init__(self, xi, yi, xf, yf) -> None:
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf

def is_websocket_data(message) -> bool:
    if message['method'] in ('Network.webSocketFrameReceived', 'Network.webSocketFrameSent'):
        return True
    return False

def is_take_turn_response(payload) -> bool:
    if payload['type'] in ('takeTurnResponse'):
        return True
    return False

def make_a_smove(driver: WebDriver, move: Move):
    make_a_move(driver, move.xi, move.yi, move.xf, move.yf)

def make_a_move(driver: WebDriver, xi: int, yi: int, xf: int, yf: int):
    to_move_element = driver.find_element(By.ID, "game-piece-{y}-{x}".format(y=yi, x=xi))
    to_move_element.click()

    move_to_square_element = driver.find_element(By.ID, "cell-{y}-{x}".format(y=yf, x=xf))
    move_to_square_element.click()

receiver_move_list: dict[int, Move] = {
0:  Move( 6, 5, 5, 4),
1:  Move( 5, 4, 3, 2),
2:  Move( 2, 5, 3, 4),
3:  Move( 1, 6, 3, 4),
4:  Move( 3, 4, 1, 2),
5:  Move( 4, 5, 3, 4),
6:  Move( 5, 6, 3, 4),
7:  Move( 3, 4, 2, 3),
8:  Move( 2, 3, 0, 1),
9:  Move( 3, 6, 4, 5),
10:  Move( 4, 5, 3, 4),
11:  Move( 0, 7, 1, 6),
12:  Move( 2, 7, 1, 6),
13:  Move( 4, 7, 3, 6),
14:  Move( 0, 1, 1, 0),
15:  Move( 6, 7, 5, 6),
16:  Move( 7, 6, 5, 4),
17:  Move( 0, 5, 1, 4),
18:  Move( 5, 4, 4, 3),
19:  Move( 1, 0, 0, 1),
20:  Move( 0, 1, 1, 0),
21:  Move( 1, 0, 3, 2),
22:  Move( 3, 2, 2, 3),
23:  Move( 2, 3, 4, 5),
24:  Move( 4, 5, 3, 4),
25:  Move( 3, 4, 4, 5),
26:  Move( 4, 5, 6, 3),
27:  Move( 6, 3, 5, 4),
28:  Move( 5, 4, 4, 5),
29:  Move( 4, 5, 5, 4),
30:  Move( 5, 4, 3, 2),
31:  Move( 3, 2, 4, 1),
32:  Move( 4, 1, 6, 3),
33:  Move( 6, 3, 5, 2),
34:  Move( 5, 2, 6, 1)
        }
sender_move_list: dict[int, Move] = {
0:  Move( 3, 2, 4, 3),
1:  Move( 2, 1, 4, 3),
2:  Move( 4, 3, 2, 5),
3:  Move( 1, 2, 2, 3),
4:  Move( 0, 1, 2, 3),
5:  Move( 2, 3, 4, 5),
6:  Move( 1, 0, 2, 1),
7:  Move( 2, 1, 1, 2),
8:  Move( 5, 2, 4, 3),
9:  Move( 6, 1, 5, 2),
10:  Move( 4, 3, 2, 5),
11:  Move( 2, 5, 0, 7),
12:  Move( 0, 7, 2, 5),
13:  Move( 2, 5, 4, 7),
14:  Move( 4, 1, 3, 2),
15:  Move( 4, 7, 6, 5),
16:  Move( 3, 2, 2, 3),
17:  Move( 2, 3, 0, 5),
18:  Move( 5, 2, 3, 4),
19:  Move( 3, 0, 2, 1),
20:  Move( 0, 5, 1, 6),
21:  Move( 1, 6, 2, 7),
22:  Move( 2, 7, 1, 6),
23:  Move( 7, 2, 6, 3),
24:  Move( 1, 6, 2, 7),
25:  Move( 6, 3, 5, 4),
26:  Move( 5, 0, 4, 1),
27:  Move( 4, 1, 3, 2),
28:  Move( 2, 7, 1, 6),
29:  Move( 3, 2, 4, 3),
30:  Move( 7, 0, 6, 1),
31:  Move( 6, 1, 5, 2),
32:  Move( 1, 6, 2, 5),
33:  Move( 2, 5, 3, 4)
        }
