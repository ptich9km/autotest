import pyautogui
import time


def jumpperson(num):
    if num == 1:
        while True:
            time.sleep(3)
            pyautogui.moveTo(838, 390)
            time.sleep(1)
            pyautogui.click()

    elif num == 2:
        while True:
            time.sleep(3)
            pyautogui.moveTo(838, 390)
            time.sleep(1)
            pyautogui.click()

            pyautogui.moveTo(1732, 391)
            time.sleep(1)
            pyautogui.click()
            time.sleep(3)
    else:
        exit()


jumpperson(1)

#jumpperson(1)