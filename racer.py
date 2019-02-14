import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time
import pyautogui
    


# KeyEnter = pyautogui.press('return')
# KeySpace = pyautogui.press('space')
# KeyDown = pyautogui.press('down')
# KeyUp = pyautogui.press('up')
# KeyRight = pyautogui.press('right')
# KeyLeft = pyautogui.press('left')

def pressKey(key):
        print("Key " + key + " pressed.")
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)

def testKeypresses():

        for i in list(range(4))[::-1]:
                print(i+1)
                time.sleep(1)
        while True:
                print('return')
                pressKey('right')
                time.sleep(2)
                pressKey('z')
                time.sleep(2)


def draw_lines(img,lines):
        try:
                for line in lines:
                        coords = line[0]
                        cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,0,0],3)
        except:
                pass


def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked






def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    # old vertices [[10,500],[10,300],[300,200],[500,200],[800,300],[800,500],]
    vertices = np.array([[120,450],[120,400],[320,370],[475,370],[675,400],[675,450],
                         ], np.int32)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)

    processed_img = roi(processed_img, [vertices])
    lines = cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),100,5 )
    draw_lines(processed_img,lines)
    
    return processed_img

def main():
    last_time = time.time()
    while True:
        screen =  np.array(ImageGrab.grab(bbox=(100,100,800,600)))
        #print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        new_screen = process_img(screen)
        cv2.imshow('window', new_screen)
        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
main()
