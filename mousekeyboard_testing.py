import pyautogui
import time
import os
import random

'''
# keyhold
# alt + L - Drones:Launch drone
# R - Drones:Return to drone bay
# Alt+H - Reprocessing Plant
# PointTogoX PointTogoY - point to jump in Asteroid belt
# need to install in linux next app - wmctrl
'''

def SetActiveWindow(name):
    try:
        time.sleep(0.1)
        os.system('wmctrl -a "EVE - {}"'.format(name))
        return 1
    except Exception as ккккe:
        print("Window EVE is not opened " + str(e))
        return 0

#Constants
#You_character_name = 'Pticher2'
You_character_name = 'Alexey Krasnogorov'
PointUndocButtonX = 914
PointUndocButtonY = 464
PointTogoX = 114
PointTogoY = 466
PointTogoSecX = 114
PointTogoSecY = 486
PointTogoX1 = 0
PointTogoY1 = 0
PointTogoX2 = 0
PointTogoY2 = 0
PointSelectOreX = 845
PointSelectOreY = 475
PointSelectOreX1 = 0
PointSelectOreY1 = 0
PointSelectOreX2 = 0
PointSelectOreY2 = 0
PointSelectOreX3 = 0
PointSelectOreY3 = 0
PointComehomeX = 887
PointComehomeY = 475
PointComehomeX1 = 0
PointComehomeY1 = 0
teamViewerkillX = 1198
teamViewerkillY = 587

def killteamview():
    detectteamview = os.system('wmctrl -l | grep Sponsored')
    time.sleep(0.5)
    if detectteamview == 256:
        time.sleep(0.1)
    else:
        os.system('wmctrl -a "Sponsored session"')
        pyautogui.moveTo(teamViewerkillX, teamViewerkillY)
        time.sleep(0.5)
        print("Kill this bug")
        pyautogui.click()

# Select Mining - start mining
def SelectMining():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        #select in menu Mining - ore1
        PointSelectOreX1 = PointSelectOreX - 34
        PointSelectOreY1 = PointSelectOreY + 47
        #select in menu Mining - ore2
        PointSelectOreX2 = PointSelectOreX1 + 4
        PointSelectOreY2 = PointSelectOreY1 + 17
        time.sleep(2)
        pyautogui.moveTo(PointSelectOreX, PointSelectOreY)
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
        #select menu Mining
        pyautogui.moveTo(PointSelectOreX1, PointSelectOreY1)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        # -Ore 1
        pyautogui.keyDown('ctrlleft')
        time.sleep(1)
        pyautogui.click()
        time.sleep(3)
        pyautogui.keyUp('ctrlleft')
        time.sleep(1)
        pyautogui.press('f1')
        time.sleep(1)
        # -Ore 2
        pyautogui.moveTo(PointSelectOreX2, PointSelectOreY2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.keyDown('ctrlleft')
        time.sleep(1)
        pyautogui.click()
        time.sleep(3)
        pyautogui.keyUp('ctrlleft')
        time.sleep(1)
        pyautogui.moveTo(PointSelectOreX2, PointSelectOreY2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('f2')
        time.sleep(1)
        #Salvage drone engage
        pyautogui.press('f')
        time.sleep(3)
    else:
        print("Window EVE is not opened")

def UnSelectMining():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        time.sleep(2)
        #select in menu Mining - ore1
        PointSelectOreX1 = PointSelectOreX - 34
        PointSelectOreY1 = PointSelectOreY + 47
        #select in menu Mining - ore2
        PointSelectOreX2 = PointSelectOreX1 + 4
        PointSelectOreY2 = PointSelectOreY1 + 17
        #choose overview mine
        pyautogui.moveTo(PointSelectOreX, PointSelectOreY)
        time.sleep(1)
        pyautogui.click()
        # choose ore 1 and unselect
        time.sleep(1)
        pyautogui.moveTo(PointSelectOreX1, PointSelectOreY1)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('ctrlleft', 'shiftleft')
        # choose ore 2 and unselect
        time.sleep(1)
        pyautogui.moveTo(PointSelectOreX2, PointSelectOreY2)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('ctrlleft', 'shiftleft')
        time.sleep(1)
        # Unpress ore strip miners 1 2
        pyautogui.press('f1')
        time.sleep(1)
        pyautogui.press('f2')
        time.sleep(1)
        # Unselect targeting
        pyautogui.moveTo(215.639)
        time.sleep(1)
        pyautogui.click(215,639, button='right')
        time.sleep(2)
    else:
        print("Window EVE is not opened")

def docExit():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        pyautogui.moveTo(PointUndocButtonX,PointUndocButtonY)
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
    else:
        print("Window EVE is not opened")

def SelectPointJump1():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        time.sleep(1)
        pyautogui.hotkey('altleft', 'e')
        # Use random_coodrinate location(One or two)
        rnd = random.randint(0,1)
        if rnd == 1:
            pyautogui.moveTo(PointTogoX, PointTogoY)
            PointTogoX1 = PointTogoX + 20
            PointTogoY1 = PointTogoY + 5
        else:
            pyautogui.moveTo(PointTogoSecX, PointTogoSecY)
            PointTogoX1 = PointTogoSecX + 20
            PointTogoY1 = PointTogoSecY + 5
        time.sleep(1)
        pyautogui.click(button='right')
        time.sleep(2)
        pyautogui.moveTo(PointTogoX1, PointTogoY1)
        time.sleep(1)
        pyautogui.moveTo(PointTogoX1, PointTogoY1)
        pyautogui.click(button='right')
        time.sleep(2)
        pyautogui.moveTo(423, 644)
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
        pyautogui.hotkey('altleft', 'e')
        time.sleep(2)
    else:
        print("Window EVE is not opened")


def launch_drone():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        time.sleep(1)
        # -launch drone
        for i in range(15):
            time.sleep(2)
            pyautogui.hotkey('altleft', 'l')
    else:
        print("Window EVE is not opened")

def return_drone_to_board():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        # drone come home
        time.sleep(2)
        pyautogui.press('r')
        time.sleep(3)
        pyautogui.press('r')
        time.sleep(3)
        pyautogui.press('r')
        time.sleep(3)
        pyautogui.press('r')
        # off strip miners
        time.sleep(3)
        pyautogui.press('f1')
        time.sleep(3)
        pyautogui.press('f2')
        time.sleep(1)
        pyautogui.moveTo(509, 602)
        time.sleep(1)
        pyautogui.click(button='right')
        time.sleep(2)
    else:
        print("Window EVE is not opened")

def jump_to_home():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        time.sleep(1)
        # Way to home
        PointComehomeX1 = PointComehomeX - 34
        PointComehomeY1 = PointComehomeY + 47
        time.sleep(2)
        pyautogui.moveTo(PointComehomeX, PointComehomeY)
        pyautogui.click()
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(PointComehomeX1, PointComehomeY1)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('d')
        time.sleep(80)
        pyautogui.press('d')
    else:
        print("Window EVE is not opened")

def SellOreInStation():
    time.sleep(1)
    killteamview()
    time.sleep(1)
    if SetActiveWindow(You_character_name) == 1:
        time.sleep(2)
        pyautogui.hotkey('altleft', 'c')
        time.sleep(3)
        # select Ore channel
        pyautogui.moveTo(125, 410)
        time.sleep(1)
        pyautogui.click()
        time.sleep(3)
        # select all
        pyautogui.moveTo(358, 502)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('ctrlleft', 'a')
        time.sleep(1)
        pyautogui.moveTo(322, 427)
        time.sleep(1)
        pyautogui.click(button='right')
        time.sleep(2)
        pyautogui.moveTo(367, 468)
        time.sleep(2)
        pyautogui.click()
        # reprocess
        time.sleep(3)
        pyautogui.moveTo(772, 877)
        time.sleep(1)
        pyautogui.click()
        time.sleep(3)
        # close Inventory
        pyautogui.hotkey('altleft', 'h')
        time.sleep(2)
        pyautogui.hotkey('altleft', 'c')
        time.sleep(1)
    else:
        print("Window EVE is not opened")

def start_working_day():

    docExit()
    time.sleep(20)
    SelectPointJump1()
    time.sleep(30)
    #SelectPointJump1
    #time.sleep(50)
    launch_drone()
    time.sleep(1)
    SelectMining()
    time.sleep(600)
    UnSelectMining()
    time.sleep(1)
    SelectMining()
    time.sleep(600)
    UnSelectMining()
    time.sleep(2)
    SelectMining()
    time.sleep(600)
    return_drone_to_board()
    time.sleep(5)
    jump_to_home()
    time.sleep(20)
    SellOreInStation()
    time.sleep(10)


while True:
    start_working_day()