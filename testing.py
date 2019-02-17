import cv2
import numpy as np 
import pyscreenshot as ImageGrab
from PIL import Image
import process_image


original_image =  np.array(ImageGrab.grab(bbox=(100,100,800,600)))
processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
# detects edges from the image
processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

# roi vertices
vertices = np.array([[120,450],[120,380],[320,380],[475,350],[675,400],[675,450],
                         ], np.int32)
# blur the image to better finding the lines
processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
# region of intrest from the whole img
processed_img = process_image.roi(processed_img, [vertices])

im = Image.fromarray(processed_img)
# im.save('test-image-roi.jpg')


