import cv2
import numpy as np

# Calculates line1 and line2 intersection point
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

# Draws lines to the img
def draw_lines(img,lines):
    try:
        for line in lines:
            coords = line
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,0,0],3)
    except:
        pass

# Draws point to img
def draw_point(img, coord):
    try:
        print("Circle coords: ",coord.item(0),coord.item(1))
        cv2.circle(img,(int(coord.item(0)),int(coord.item(1))),10,(255, 0, 0), -1)
    except:
        print("Unable to draw the point!")


# Takes img and roi-vertices and return masked img
def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

# Takes imgage and line parameters y=mx + b and return two points (x1,y1),(x2,y2) 
# which are in the line 
def make_coordinates(image,line_parameters):
    slope, intercept = line_parameters

    y1 = image.shape[0]
    y2 = int(y1*(3/5))

    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)

    return np.array([x1,y1,x2,y2])


# Finds left and right laneline from all the lines.
def find_lane_lines(image,lines):
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






def process_img(original_image):
    # change image to gray
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # detects edges from the image
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    # roi vertices
    vertices = np.array([[120,450],[120,380],[320,380],[475,350],[675,400],[675,450],
                         ], np.int32)
    # blur the image to better finding the lines
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)

    # region of intrest from the whole img
    processed_img = roi(processed_img, [vertices])

    # find lines from the image
    lines = cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),100,5 )
    lane_lines = find_lane_lines(processed_img,lines)

    if lane_lines.size != 0:
        # find intersection pooint from lanelines and draw it to image
        intersection = line_line_intersection(lane_lines[0],lane_lines[1])
        draw_point(processed_img, intersection)

    draw_lines(processed_img,lane_lines)
    
    return processed_img