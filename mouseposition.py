import pyautogui

#print your mouse position when send any keyboard coomand
try:
    while True:
        # TODO: Get and print the mouse coordinates.
        input()
        x, y = pyautogui.position()
        print("coordinates XY are ({},{}) ".format(x, y))
except KeyboardInterrupt as e:
   print('\nDone.' + str(e))


