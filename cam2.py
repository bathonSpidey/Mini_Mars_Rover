#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 19:43:43 2019

@author: spidey
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    a=np.double(frame)
    b=a-15
    frame2 = np.uint8(b)
    cv2.imshow('frame',frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
 
'''   
img1 = cv2.imread('abc.jpg')
a = np.double(img1)
b = a + 15
img2 = np.uint8(b)
cv2.imshow("frame",img1)
cv2.imshow("frame2",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''