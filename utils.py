from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

room_code = "aahh"
receiver_move_list: dict[int, Move] = {}
sender_move_list: dict[int, Move] = {}

def make_a_move(driver: WebDriver, xi: int, yi: int, xf: int, yf: int):
    to_move_element = driver.find_element(By.ID, "game-piece-{y}-{x}".format(y=yi, x=xi))
    to_move_element.click()

    move_to_square_element = driver.find_element(By.ID, "cell-{y}-{x}".format(y=yf, x=xf))
    move_to_square_element.click()

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
