room_code = "asdsdff"

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

def make_a_move(driver: WebDriver, xi: int, yi: int, xf: int, yf: int):
    to_move_element = driver.find_element(By.ID, "game-piece-{y}-{x}".format(y=yi, x=xi))
    to_move_element.click()

    move_to_square_element = driver.find_element(By.ID, "cell-{y}-{x}".format(y=yf, x=xf))
    move_to_square_element.click()

receiver_move_list: dict[int, Move] = {
0: Move( 6, 5, 5, 4),
1: Move( 5, 4, 3, 2),
2: Move( 4, 5, 5, 4),
3: Move( 7, 6, 5, 4),
4: Move( 5, 4, 3, 2),
5: Move( 2, 5, 1, 4),
6: Move( 1, 4, 3, 2),
7: Move( 3, 2, 1, 0),
8: Move( 3, 6, 4, 5),
9: Move( 4, 5, 6, 3),
10: Move( 5, 6, 6, 5),
11: Move( 6, 7, 5, 6),
12: Move( 1, 6, 2, 5),
13: Move( 1, 0, 2, 1),
14: Move( 2, 1, 0, 3),
15: Move( 0, 3, 2, 1),
16: Move( 2, 5, 3, 4),
17: Move( 3, 4, 1, 2)
        }
sender_move_list: dict[int, Move] = {
0: Move( 3, 2, 4, 3),
1: Move( 2, 1, 4, 3),
2: Move( 4, 3, 6, 5),
3: Move( 5, 2, 4, 3),
4: Move( 4, 1, 2, 3),
5: Move( 6, 1, 5, 2),
6: Move( 1, 0, 2, 1),
7: Move( 5, 2, 4, 3),
8: Move( 4, 3, 5, 4),
9: Move( 7, 2, 5, 4),
10: Move( 5, 4, 7, 6),
11: Move( 7, 6, 6, 7),
12: Move( 6, 7, 4, 5),
13: Move( 4, 5, 5, 4),
14: Move( 0, 1, 1, 2),
15: Move( 3, 0, 1, 2),
16: Move( 1, 2, 2, 3),
17: Move( 5, 4, 6, 5)
        }
