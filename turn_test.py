#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 11:18:29 2019

@author: spidey
"""

import cv2
import numpy as np
import time
import direction as dr
#import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
#cap.set(10, 30)
#cap.set(11, 50)
print("Camera connected")

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    hight = image.shape[0]
    y1 = 250
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
        if slope < 0 and slope > -2:
            left_fit.append((slope, intercept)) 
        elif slope > 0 and slope < 2:
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

def roi(image):
    height = image.shape[0]
    polygons = np.array([[(0, 0), (0, 300), (250, 90), (400, 90), (640, 300), (640, 0)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
            cv2.line(line_image, (320, 0), (320, 480), (0, 0, 255), 1)
    return line_image

def canny(image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def corners(gray):
    countL=0
    countR=0
    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    corners = np.int0(corners)
    print(corners)
    for i in corners:
        x,y = i.ravel()
        if x<400:
            countL+=1
        elif x>400:
            countR+=1
    if countL>countR:
        return 'Left'
    elif countL<countR:
        return 'Right'
    else:
        print("None")

def checkColor(image):
    count=0
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
    res = cv2.bitwise_and(image,image, mask=mask)
    ret,thrshed = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
    _,contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >10000:
            print('object found')
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            corners()
            cv2.putText(image, 'Green Object Detected', (10,80), cv2.FONT_HERSHEY_SIMPLEX, 1.0,(255, 255, 255),lineType=cv2.LINE_AA)
            cv2.rectangle(image,(5,40),(400,100),(0,255,255),2)
            count+=1
    print('count', count)
    if count==10:
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        a=corners(gray)
        j=0
        while j<20:
            dr.goCustom(90,90)
            j+=1
            n=0
            while n<1:
                dr.stop(2)
                if a =='Left':
                    dr.left()
                else:
                    dr.right()
                n=n+1

def check_turning(dis):
    if int(dis[1]) < 100:
        dr.goCustom(80, 90)
        print('left')
    elif int(dis[1]) > 150:
        dr.goCustom(90, 80)
        print('right')
    else:
        #dr.goStraight()
        dr.goCustom(70,70)
        print('straight')

turnTo=False
while True:
    _, image=cap.read()
    #dr.goStraight()
    #time.sleep(2)
    #dr.stop(3)

#image = cv2.imread('roverroadvision.png')
    if turnTo:
        print('I am busy turning')
        i=0
        while True:
            checkColor(image)
            if i>20:
                TurnTo=False
                break
            i+=1
    else: 
        try:
            lane_image = np.copy(image)
            canny_image = canny(lane_image)
            cropped_image = roi(canny_image)
            lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=50)
            averaged_lines, distances = average_slope_intercept(lane_image, lines)
            line_image = display_lines(lane_image, averaged_lines)
            combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
            cv2.imshow("Result", combo_image)   
            check_turning(distances)
        except:
            cv2.imshow("Result", image)
            dr.goCustom(70,90)
            turnTo=True
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
cv2.waitKey(0)