#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 18:52:28 2019

@author: spidey
"""

import numpy as np
import cv2

<<<<<<< HEAD
cap = cv2.VideoCapture(0) # my webcam
cap.set(3, 1280) # set the resolution
cap.set(4, 720)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
=======
cap = cv2.VideoCapture(1)

>>>>>>> 9b0291587e33e734ff07e0ca536970e2a7c2b7be
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()