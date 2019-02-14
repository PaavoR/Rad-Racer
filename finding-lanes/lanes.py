import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def canny(image):
    gray = cv2.cvtColor(lane_image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # in tutorial 50,150
    canny = cv2.Canny(blur,200,400)
    return canny

def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image

def region_of_intrest(image):
    region = np.array([[(0,350),(0,300),(200,233),(360,233),(560,300),(560,350)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,region,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

image = cv2.imread('test-image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
cropped_image = region_of_intrest(canny)
lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40, maxLineGap=5)
line_image = display_lines(lane_image, lines)
plt.imshow(line_image)
plt.show()