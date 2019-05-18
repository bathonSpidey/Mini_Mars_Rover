import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(1)
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
	midpoints(image, left_line)
	midpoints(image, right_line)
	return np.array([left_line, right_line])

def midpoints(image, line_parameters):
	line_midpoint = [(line_parameters[0]+line_parameters[2])/2, (line_parameters[1]+line_parameters[3])/2]
	cv2.circle(image, (int(line_midpoint[0]), int(line_midpoint[1])), 3, (0,0,255), -1)
	if line_midpoint[0] < 320:
		cv2.line(image, (int(line_midpoint[0]), int(line_midpoint[1])), (320, int(line_midpoint[1])), (0, 0, 255), 2)
	else: 
		cv2.line(image, (int(line_midpoint[0]), int(line_midpoint[1])), (320, int(line_midpoint[1])), (0, 0, 255), 2)
	
	line_distance = str(abs(320 - int(line_midpoint[0])))	
	cv2.putText(image, line_distance, (int((line_midpoint[0]+320)/2), int((line_midpoint[1]-5))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), lineType=cv2.LINE_AA) 



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

while True:
	_, image=cap.read()

#image = cv2.imread('roverroadvision.png')
	lane_image = np.copy(image)
	canny_image = canny(lane_image)
	cropped_image = roi(canny_image)
	lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=50)
	averaged_lines = average_slope_intercept(lane_image, lines)
	line_image = display_lines(lane_image, averaged_lines)
	combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
	cv2.imshow("Result", combo_image)	
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break
cv2.waitKey(0)