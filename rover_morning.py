import cv2
import numpy as np
import time
import statistics
from statistics import mode
import direction as dr
#import matplotlib.pyplot as plt

green_lower = np.array([65, 94, 18], np.uint8)
green_upper = np.array([80,255,255], np.uint8)

red_lower = np.array([0, 130, 220], np.uint8)
red_upper = np.array([10, 255, 255], np.uint8)

blue_lower = np.array([67, 70, 0], np.uint8)
blue_upper = np.array([119, 255, 255], np.uint8)
text_size = 0.5

cap = cv2.VideoCapture(0)
print("Camera connected")

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    hight = image.shape[0]
    y1 = 350
    y2 = 50
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
    right_fit = []
    left_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < -0.5 and slope > -4:
            left_fit.append((slope, intercept)) 
        elif slope > 0.5 and slope < 4:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    left_distance = midpoints(image, left_line)
    right_distance = midpoints(image, right_line)
    return np.array([left_line, right_line]), [left_distance, right_distance]


def midpoints(image, line_parameters):
    line_midpoint = [(line_parameters[0] +line_parameters[2])/2, (line_parameters[1]+line_parameters[3])/2]
    cv2.circle(image, (int(line_midpoint[0]), int(line_midpoint[1])), 3, (0,0,255), -1)
    if line_midpoint[0] < 320:
        cv2.line(image, (int(line_midpoint[0]), int(line_midpoint[1])), (320, int(line_midpoint[1])), (0, 0, 255), 2)
    else: 
        cv2.line(image, (int(line_midpoint[0]), int(line_midpoint[1])), (320, int(line_midpoint[1])), (0, 0, 255), 2)
    
    line_distance = str(abs(320 - int(line_midpoint[0])))   
    cv2.putText(image, line_distance, (int((line_midpoint[0]+320)/2), int((line_midpoint[1]-5))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), lineType=cv2.LINE_AA)
    return line_distance


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return line_image

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def check_turning(dis):
    if int(dis[0]) < 245:
        dr.goCustom(110, 90)
        print('-->')
    elif int(dis[1]) < 235:
        dr.goCustom(90, 110)
        print('<--')
    else:
        print('^')
        dr.goStraight()

def detect_lanes(image):
    lane_image = np.copy(image)
    canny_image = canny(lane_image)
        #cropped_image = roi(image)
    lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=50)
    averaged_lines, distances = average_slope_intercept(lane_image, lines)
    line_image = display_lines(lane_image, averaged_lines)
    combo_image = cv2.addWeighted(lane_image, 1, line_image, 1, 1)
    cv2.line(line_image, (320, 0), (320, 480), (255, 0, 255), 1)
    cv2.putText(combo_image, 'Lanes', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), lineType=cv2.LINE_AA)
    cv2.imshow('Result', combo_image)
    return combo_image, distances



def turn(direction):
    if direction == 'Left':
        dr.left()
        print('Turning left')
        return
    if direction == 'Right':
        dr.right()
        print('Turning right')
        return

def readRed(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, red_lower, red_upper)
    kernal = np.ones((5,5), 'uint8')
    blue = cv2.dilate(blue, kernal)
    res = cv2.bitwise_and(image, image, mask=blue)

    _, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1):
            x,y,w,h = cv2.boundingRect(contour)
            image = cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(image, 'RED Light', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            return image, True
    return image, False

def read_green_arrow(img):
    image = cv2.flip(img, -1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, green_lower, green_upper)
    kernal = np.ones((5,5), 'uint8')
    blue = cv2.dilate(blue, kernal)
    res = cv2.bitwise_and(image, image, mask=blue)

    _, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        print(area, 'green')
        if(area>100):
            x,y,w,h = cv2.boundingRect(contour)
            image = cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
            return 'Right', image
        else:
            return 'Undefined', image

def read_blue_arrow(img):
    image = cv2.flip(img, -1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    kernal = np.ones((5,5), 'uint8')
    blue = cv2.dilate(blue, kernal)
    res = cv2.bitwise_and(image, image, mask=blue)

    _, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image = cv2.flip(image, -1)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        print(area, 'blue')
        if(area>100):
            x,y,w,h = cv2.boundingRect(contour)
            image = cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(image, 'BLue Arrow', (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            return 'Left', image
        else:
            return 'Undefined', image

turn_command=False
turn_com=False

while True:
    _, frame=cap.read()
    image, statement = readRed(frame)
    if statement == False:

            
        try:
            image_with_lanes, distance = detect_lanes(frame)
            cv2.imshow('Result', image_with_lanes)
        except Exception as e:
            print(e, 'lane detection error')
            cv2.imshow('Result', image)

    else:
        cv2.imshow('Result', image)
        print('Stop, red light')
    
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        #cv2.imwrite('roi.png', frame)
        cv2.destroyAllWindows()
        break