import cv2
import numpy as np

blue_lower = np.array([110,50,50], np.uint8)
blue_upper = np.array([130,255,255], np.uint8)


def convert_image(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,blue_lower, blue_upper)
	res = cv2.bitwise_and(image, image, mask=mask)
	canny = cv2.Canny(mask, 80, 110)
	#blur = cv2.GaussianBlur(canny, (5,5), 1)
	return canny

def arrow_detection(image):
	image = np.float32(image)
	corners = cv2.goodFeaturesToTrack(image, 100, 0.1, 10)
	corners = np.int0(corners)

	right_dots = 0
	left_dots = 0
	for corner in corners:
		x, y = corner.ravel()
		cv2.circle(image, (x,y), 5, 255, -1)
		if corner[0][0] < int(image.shape[1]/2):
			left_dots +=1
		else:
			right_dots +=1
	
	if left_dots > right_dots:
		return "Left"
	elif left_dots < right_dots:
		return "Right"
	else:
		return "None"

cap = cv2.VideoCapture(0)
print("Camera connected")

while True:
	_, image=cap.read()

	#image = cv2.imread('download.png')
	canny_image = convert_image(image)
	try:
		direction = arrow_detection(canny_image)
		print(direction)
	except:
		pass
	cv2.imshow('result', canny_image)
	
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break
	
#cv2.waitKey(0)