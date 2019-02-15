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

def line_line_intersection(line1,line2):
    x1 = line1.item(0)
    y1 = line1.item(1)
    x2 = line1.item(2)
    y2 = line1.item(3)

    x3 = line2.item(0)
    y3 = line2.item(1)
    x4 = line2.item(2)
    y4 = line2.item(3)

    px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    return np.array([px,py])


def make_coordinates(image,line_parameters):
    slope, intercept = line_parameters

    y1 = image.shape[0]
    y2 = int(y1*(3/5))

    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)

    return np.array([x1,y1,x2,y2])




def average_slope_intercept(image,lines):
    left_fit = []
    right_fit = []
    max_slope = 0.35
    min_slope = 0.2
    try:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2),(y1,y2),1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope > -max_slope and slope < min_slope:
                left_fit.append((slope,intercept))
            elif slope < max_slope and slope > min_slope:
                right_fit.append((slope,intercept))
        #print("left lines: " , left_fit)
        #print("right lines: " , right_fit)
        right_fit_avg = np.average(right_fit,axis=0)
        left_fit_avg = np.average(left_fit,axis=0)

        left_line = make_coordinates(image,left_fit_avg)
        right_line = make_coordinates(image,right_fit_avg)
        return np.array([left_line,right_line])

    except:
        print("no lines found")
        return np.array([])


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
            coords = line
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,0,0],3)
    except:
        pass

def draw_point(img, coord):
    try:
        print("Circle coords: ",coord.item(0),coord.item(1))
        cv2.circle(img,(int(coord.item(0)),int(coord.item(1))),10,(255, 0, 0), -1)
    except:
        print("Unable to draw the point!")


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
    vertices = np.array([[120,450],[120,380],[320,380],[475,350],[675,400],[675,450],
                         ], np.int32)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)

    processed_img = roi(processed_img, [vertices])
    lines = cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),100,5 )
    avg_lines = average_slope_intercept(processed_img,lines)

    if avg_lines.size != 0:
        intersection = line_line_intersection(avg_lines[0],avg_lines[1])
        draw_point(processed_img, intersection)

    draw_lines(processed_img,avg_lines)
    
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

