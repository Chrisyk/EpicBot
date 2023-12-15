from multiprocessing.connection import wait
import time
import numpy as np
import cv2 as cv
import os
import pyautogui
from threading import Thread
from Vision import Vision
from windowcapture import WindowCapture
import random
import keyboard

os.chdir(os.path.dirname(os.path.abspath(__file__)))

mysticCounter = 0
bookmarkCounter = 0
friendshipCounter = 0
nothing = 0
skystonesRemaining = 2000
image = 'Images\\Mystic_Bookmark.JPG'
image2 = 'Images\\bookmark.JPG'
image3 = 'Images\\Friendship_bookmark.JPG'
image4 = 'Images\\Refresh.JPG'
image5 = 'Images\\Confirm.JPG'
image6 = 'Images\\skystones_over.JPG'
image7 = 'Images\\Connecting.JPG'

mystic = cv.imread(image,cv.IMREAD_UNCHANGED)
bookmark = cv.imread(image2,cv.IMREAD_UNCHANGED)
friendship = cv.imread(image3,cv.IMREAD_UNCHANGED)
refresh = cv.imread(image4,cv.IMREAD_UNCHANGED)
confirm = cv.imread(image5,cv.IMREAD_UNCHANGED)
skystonesOver = cv.imread(image6,cv.IMREAD_UNCHANGED)
Connecting = cv.imread(image7,cv.IMREAD_UNCHANGED)


def increaseMystic():
        global mysticCounter
        mysticCounter = mysticCounter + 1
        print('mystic ',mysticCounter)

def increaseBookmark():
        global bookmarkCounter
        bookmarkCounter = bookmarkCounter + 1
        print('bookmark ',bookmarkCounter)

def increaseFriendship():
        global friendshipCounter
        friendshipCounter = friendshipCounter + 1
        print('friendship ',friendshipCounter)

def bot_click(x,y,w,h):
        targets = Vision.get_click_points(x,y,w,h)
        target = Vision.get_screen_position(Vision,targets[0])
        number1 = random.randint(-100, 25)
        number2 = random.randint(1, 3)

        pyautogui.moveTo(x=target[0] + number1,y=target[1]+ number2)
        pyautogui.click()
        time.sleep(random.uniform(0.5,0.7))
        
 

def bot_buy(x,y,w,h):
        targets = Vision.get_click_points(x,y,w,h)
        target = Vision.get_screen_position(Vision,targets[0])
        pyautogui.moveTo(x=target[0] + random.randint(1,100) + 650,y=target[1] + random.randint(30,34))
        pyautogui.click()
        pyautogui.moveTo(x=target[0] + random.randint(1,100) + 650,y=target[1] + random.randint(30,34))
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        #pyautogui.typewrite(['g','g'], interval=1)
        confirmBuy(0.8)
        time.sleep(0.5)

def find_needle(objective, threshold, bot_action, counterName):

    result = cv.matchTemplate(screenshot,objective,cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    #print('Best match confidence: %s' % str(max_val))

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    
    if max_val >= threshold:
        if counterName == 'mysticCounter':
                increaseMystic()
        elif counterName == 'friendshipCounter':
                increaseFriendship()
        elif counterName == 'bookmarkCounter':
                increaseBookmark()

        goal_w = objective.shape[1]
        goal_h = objective.shape[0]

        top_left = max_loc
        bottom_right = top_left[0] + goal_w, top_left[1] + goal_h
        
        bot_action(max_loc[0],max_loc[1], goal_w, goal_h)

def stopProgram():
        print('Found ' + str(mysticCounter) + ' mystics')
        print('Found ' + str(bookmarkCounter) + ' bookmarks')
        print('Found ' + str(friendshipCounter) + ' friendship')
        print('Done.')

        quit()

def loopUntilNotFound(objective, threshold):
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
        result = cv.matchTemplate(screenshot,objective,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        while (max_val > threshold):
                print ('Connecting...')
                time.sleep(0.5)
                screenshot = pyautogui.screenshot()
                screenshot = np.array(screenshot)
                screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
                result = cv.matchTemplate(screenshot,objective,cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)


def confirmBuy(threshold):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
    confirm = cv.imread('Images\\buy_confirm.JPG',cv.IMREAD_UNCHANGED)
    result = cv.matchTemplate(screenshot,confirm,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    
    if max_val >= threshold:
            goal_w = confirm.shape[1]
            goal_h = confirm.shape[0]
            targets = Vision.get_click_points(max_loc[0],max_loc[1], goal_w, goal_h)
            target = Vision.get_screen_position(Vision,targets[0])
            number1 = random.randint(-150, 5)
            number2 = random.randint(1, 3)

            pyautogui.moveTo(x=target[0] - 200 + number1,y=target[1]+ number2)
            pyautogui.click()
            pyautogui.moveTo(x=target[0] - 200 + number1,y=target[1]+ number2)
            time.sleep(random.uniform(0.2,0.5))
            pyautogui.click()





while keyboard.is_pressed('space') == False and skystonesRemaining > 0:

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)

        find_needle(skystonesOver,0.9,stopProgram, 'nothing')
        find_needle(mystic,0.9, bot_buy,'mysticCounter')
        find_needle(bookmark,0.95, bot_buy,'bookmarkCounter')
        #find_needle(friendship,0.95, bot_buy,'friendshipCounter')
        x = random.randint(925,1700)
        y = random.randint(800,900)
        pyautogui.moveTo(x,y)
        pyautogui.dragTo(x + random.randint(-20,10), y - random.randint(500,520),0.5, button='left')
        time.sleep(random.uniform(1.5,2))
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
        find_needle(mystic,0.9, bot_buy, 'mysticCounter')
        find_needle(bookmark,0.95, bot_buy, 'bookmarkCounter')
        #find_needle(friendship,0.95, bot_buy,'friendshipCounter')

        find_needle(refresh,0.9,bot_click, nothing)

        time.sleep(0.1)

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)

        result = cv.matchTemplate(screenshot,confirm,cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        locations = np.where(result >= 0.9)
        locations = list(zip(*locations[::-1]))
        
        if max_val <= 0.9:
                find_needle(refresh,0.9,bot_click, nothing)
        

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)


        find_needle(confirm,0.9 , bot_click, nothing)

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)

        find_needle(confirm,0.8 , bot_click, nothing)
        

        skystonesRemaining = skystonesRemaining - 3
        print(skystonesRemaining)
        time.sleep(random.uniform(0.1,0.3))

        loopUntilNotFound(Connecting,0.75)
        

        
        #cv.imshow('Result', screenshot)
        #cv.resizeWindow('Result', 1440, 1080)

print('Found ' + str(mysticCounter) + ' mystics')
print('Found ' + str(bookmarkCounter) + ' bookmarks')
print('Found ' + str(friendshipCounter) + ' friendship')
print('done.')
quit()
