from utils import *

from selenium import webdriver
import time
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def receive():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--mute-audio")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options)

    print("waiting for load finish")
    driver.get("https://buddyboardgames.com/checkers")
    driver.maximize_window()

    print("creating room")
    player_element = driver.find_element(By.ID, "player")
    room_element = driver.find_element(By.ID, "room")
    start_game_element = driver.find_element(By.ID, "start-game")

    player_element.send_keys("receiver")
    room_element.send_keys(room_code)
    start_game_element.click()

    print("waiting for sender")

    sender_found = False

    while not sender_found:
        sender_elements = driver.find_elements(By.ID, "player-1-name")

        while sender_elements:
            sender_element = sender_elements.pop()

            if sender_element.text == "sender":
                sender_found = True
                print("found sender")
                break

        time.sleep(1)

    start_game_lobby_element = driver.find_element(By.ID, "start-game-lobby")
    start_game_lobby_element.click()

    print("logging websockets")

    time.sleep(3)
    # do moves

    # receiver has first move
    next_move = receiver_move_list[0]
    make_a_move(driver, next_move.xi, next_move.yi, next_move.xf, next_move.yf)

    index = 1
    setting_up = True
    while setting_up:
        waiting_for_sender = True
        while waiting_for_sender:
            time.sleep(0.01) # pls dont kill my cpu
            for entry in driver.get_log('performance'):
                try:
                    message: dict = json.loads(entry['message'])['message']
                    if not is_websocket_data(message):
                        continue

                    message: dict = json.loads(message['params']['response']['payloadData'])

                    if not is_take_turn_response(message):
                        continue

                    if message['payload']['previousPlayerIndex'] == (1):
                        waiting_for_sender = False
                except:
                    pass

        print("sending")

        time.sleep(1)
        # do next move
        next_move = receiver_move_list[index]
        make_a_move(driver, next_move.xi, next_move.yi, next_move.xf, next_move.yf)
        if index == len(receiver_move_list) - 1:
            setting_up = False
            break;

        index += 1

    print("done setting up, starting data transfer")

    # start sending that sweet sweet data
    move_over = Move(6, 1, 7, 0)
    reset = Move(7, 0, 6, 1)
    is_at_7_0 = True

    time.sleep(1)
    make_a_move(driver, move_over.xi, move_over.yi, move_over.xf, move_over.yf)

    sending_data = True
    while sending_data:
        waiting_for_sender = True
        while waiting_for_sender:
            time.sleep(0.01) # pls dont kill my cpu
            for entry in driver.get_log('performance'):
                try:
                    message: dict = json.loads(entry['message'])['message']
                    if not is_websocket_data(message):
                        continue

                    message: dict = json.loads(message['params']['response']['payloadData'])

                    if not is_take_turn_response(message):
                        continue

                    if message['payload']['previousPlayerIndex'] == (1):
                        waiting_for_sender = False

                except:
                    pass

        print("sending")
        time.sleep(1)
        # do next move
        if is_at_7_0:
            make_a_move(driver, move_over.xi, move_over.yi, move_over.xf, move_over.yf)
            is_at_7_0 = False
        else:
            make_a_move(driver, reset.xi, reset.yi, reset.xf, reset.yf)
            is_at_7_0 = True





if __name__ == "__main__":
    receive()

