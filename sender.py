from inspect import currentframe

from utils import *

from selenium import webdriver
import time
import json
import sys

from bitstring import BitArray

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def send():
    data_file = open(sys.argv[1], "rb")
    data = BitArray(data_file.read()).bin

    print("sending" +  str(len(data)) + " bits")

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--mute-audio")
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

    index = 0
    setting_up = True
    while setting_up:

        waiting_for_receiver = True
        while waiting_for_receiver:
            time.sleep(0.01) # pls dont kill my cpu
            for entry in driver.get_log('performance'): # ick code
                try:
                    message: dict = json.loads(entry['message'])['message']
                    if not is_websocket_data(message):
                        continue

                    message: dict = json.loads(message['params']['response']['payloadData'])

                    if not is_take_turn_response(message):
                        continue

                    if message['payload']['previousPlayerIndex'] == (0):
                        waiting_for_receiver = False
                except:
                    pass

        print("sending")

        time.sleep(1)
        # do next move
        next_move = sender_move_list[index]
        make_a_move(driver, next_move.xi, next_move.yi, next_move.xf, next_move.yf)
        if index == len(sender_move_list) - 1:
            setting_up = False
            break;

        index += 1
    # start sending that sweet sweet data

    time.sleep(3) #shitty buttt it lwk works a lil
    data_size = len(data)
    current_position = 0

    print("starting to send data")
    while current_position < data_size - 2:
        current_binary = data[current_position:current_position + 2]
        current_position += 2
        move = Move(0, 0, 0, 0)
        center = Move(0, 0, 0, 0)

        match current_binary:
            case '00':
                move = Move(3, 4, 4, 3)
                center = Move(4, 3, 3, 4)

            case '01':
                move = Move(3, 4, 2, 3)
                center = Move(2, 3, 3, 4)

            case '10':
                move = Move(3, 4, 2, 5)
                center = Move(2, 5, 3, 4)

            case '11':
                move = Move(3, 4, 4, 5)
                center = Move(4, 5, 3, 4)

        print("making first move")
        make_a_smove(driver, move)

        print("waiting")
        wait_for_receiver(driver)
        time.sleep(1)
        print("going home")
        make_a_smove(driver, center)
        print("waiting")
        wait_for_receiver(driver)

        time.sleep(1)


# Who needs async await when you can do this
def wait_for_receiver(driver):
    waiting_for_receiver = True
    while waiting_for_receiver:
        time.sleep(0.01) # pls dont kill my cpu
        for entry in driver.get_log('performance'): # ick code
            try:
                message: dict = json.loads(entry['message'])['message']
                if not is_websocket_data(message):
                    continue

                message: dict = json.loads(message['params']['response']['payloadData'])

                if not is_take_turn_response(message):
                    continue

                if message['payload']['previousPlayerIndex'] == (0):
                    waiting_for_receiver = False
            except:
                pass


if __name__ == "__main__":
    send()

