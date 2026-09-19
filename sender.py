from utils import *

from selenium import webdriver
import time
import json

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def send():
    options = Options()
    # options.add_argument("--headless")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options)

    print("waiting for load finish")
    driver.get("https://buddyboardgames.com/checkers")
    driver.maximize_window()

    print("joining room")
    player_element = driver.find_element(By.ID, "player")
    room_element = driver.find_element(By.ID, "room")
    start_game_element = driver.find_element(By.ID, "start-game")

    player_element.send_keys("sender")
    room_element.send_keys(room_code)
    start_game_element.click()

    print("waiting for receiver to start and logging websockets")

    time.sleep(3)
    # do moves

    # sender has first move
    next_move = receiver_move_list[0]
    make_a_move(driver, next_move.xi, next_move.yi, next_move.xf, next_move.yf)

    index = 1
    setting_up = True
    while setting_up:

        waiting_for_receiver = True
        while waiting_for_receiver:
            time.sleep(0.01) # pls dont kill my cpu
            for entry in driver.get_log('performance'): # ick code
                try:

                    message: dict = json.loads(entry['message'])['message']
                    if message['method'] in ('Network.webSocketFrameReceived', 'Network.webSocketFrameSent'):

                        payload: dict = json.loads(message['params']['response']['payloadData'])

                        if payload["type"] == "takeTurnResponse":

                            if payload["payload"]["previusPlayerIndex"] != 1:
                                waiting_for_receiver = False

                            print(payload)
                            print("")
                except:
                    pass

            # do next move
            next_move = receiver_move_list[index]
            make_a_move(driver, next_move.xi, next_move.yi, next_move.xf, next_move.yf)
            index += 1


if __name__ == "__main__":
    send()

