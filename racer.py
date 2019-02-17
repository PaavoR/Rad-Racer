import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time
import pyautogui

import process_image
    


# KeyEnter = pyautogui.press('return')
# KeySpace = pyautogui.press('space')
# KeyDown = pyautogui.press('down')
# KeyUp = pyautogui.press('up')
# KeyRight = pyautogui.press('right')
# KeyLeft = pyautogui.press('left')



def main():
    last_time = time.time()
    while True:
        screen =  np.array(ImageGrab.grab(bbox=(100,100,800,600)))
        #print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        new_screen = process_image.process_img(screen)
        cv2.imshow('window', new_screen)
        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
main()

