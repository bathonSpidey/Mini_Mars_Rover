import cv2
import numpy as np

#lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
#upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}

red_lower=np.array([0, 130, 220], np.uint8)
red_upper=np.array([10,255,255], np.uint8)

blue_lower = np.array([97, 100, 117], np.uint8)
blue_upper = np.array([117,255,255], np.uint8)

cap = cv2.VideoCapture(1)
print("Camera connected")

def readBLue(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	blue = cv2.inRange(hsv, red_lower, red_upper)
	kernal = np.ones((5,5), 'uint8')
	blue = cv2.dilate(blue, kernal)
	res = cv2.bitwise_and(img, img, mask=blue)

	contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area>20):
			x,y,w,h = cv2.boundingRect(contour)
			img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
			cv2.putText(img, 'Blue Color', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
			print("Found BLUE color")
			return True
	return False

	

def readRed(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	red = cv2.inRange(hsv, red_lower, red_upper)
	kernal = np.ones((5,5), 'uint8')
	red = cv2.dilate(red, kernal)
	res = cv2.bitwise_and(img, img, mask=red)

	contours, hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area>20):
			x,y,w,h = cv2.boundingRect(contour)
			img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
			cv2.putText(img, 'Red Color', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
			print("Found Red color")
			return True
	return False

while True:
	_, img=cap.read()

	#b = readBLue(img)
	r = readRed(img)

	cv2.imshow("Color Tracking", img)	
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break
