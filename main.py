room_code = "xx"

from selenium import webdriver
import time
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    options = Options()
    # options.add_argument("--headless")
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

    while True:
        time.sleep(0.01) # pls dont kill my cpu
        for entry in driver.get_log('performance'):
            try:
                message: dict = json.loads(entry['message'])['message']
                if message['method'] in ('Network.webSocketFrameReceived', 'Network.webSocketFrameSent'):
                    payload: dict = json.loads(message['params']['response']['payloadData'])
                    if payload["type"] == "takeTurnResponse":
                        if payload["payload"]["previusPlayerIndex"] == 0:
                            continue # receivers move

                        print(payload)
                        print("")
            except:
                pass

if __name__ == "__main__":
    main()
