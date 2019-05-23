# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:58:34 2019

@author: Abir
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt


def read_image(add):
    return cv2.imread(add)

def gray(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#def mask(img)

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
        print("Left")
    elif countL<countR:
        print("Right")
    else:
        print("None")
    return cv2.circle(gray,(x,y),3,255,-1)
"""


def make_points(gray,corners):
    for i in corners:
        x,y = i.ravel()
        if x<300:
            print("Left")
        elif x>500:
            print("Right")
        return cv2.circle(gray,(x,y),3,255,-1)
img1=read_image("arrow1.jpg")
img2=read_image("arrow3.jpeg")

gray1=gray(img1)
gray2=gray(img2)

corners1=corners(gray1)
corners2=corners(gray2)
print("corners1:",corners1)
print("corners2:", corners2)

display1=make_points(gray1, corners1)
display2=make_points(gray2,corners2)


plt.imshow(img1),plt.show()
plt.imshow(img2),plt.show()
"""
cap = cv2.VideoCapture(0)
print("Camera connected")

while True:
    _, image=cap.read()

	#image = cv2.imread('download.png')
    gray_image = gray(image)
    try:
        display = corners(gray_image)
    except:
        pass
    cv2.imshow('result', gray_image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

"""
cv2.imshow("gray1",display1)
cv2.imshow("gray2", display2)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""