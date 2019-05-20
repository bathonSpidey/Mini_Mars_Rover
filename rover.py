import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

green_lower = np.array([64, 70, 86], np.uint8)
green_upper = np.array([80,255,255], np.uint8)

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
	left_distance = midpoints(image, left_line)
	right_distance = midpoints(image, right_line)
	return np.array([left_line, right_line])

def midpoints(image, line_parameters):
	line_midpoint = [round((line_parameters[0]+line_parameters[2])/2, 2), (round((line_parameters[1]+line_parameters[3])/2, 2))]
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

def roi_horizontal(image):
	height = image.shape[0]
	polygons = np.array([[(0, 300), (0, 370), (image.shape[1], 370), (image.shape[1], 300)]])
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
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	canny = cv2.Canny(blur, 50, 150)
	return canny

def turn(image):
	image_with_h_line = np.zeros_like(frame)
	roi = roi_horizontal(image)
	h_lines = cv2.HoughLinesP(roi, 1, np.pi/180, 100, minLineLength=10)
	fit=[]
	if h_lines is not None:
		for line in h_lines:
			fit.append(line.reshape(4))
		fit_average = np.mean(fit, axis=0)
		x1, y1, x2, y2 = fit_average
		cv2.line(image_with_h_line, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)


		combo_image = cv2.addWeighted(frame, 1, image_with_h_line, 1, 1)
		print("Turn line detected.... Searching for direction....", end=' ')
		try:
			direction = arrow_detection(frame)
			print(direction)
		except:
			print("No direction")
		return combo_image
	else:
		return frame

def detect_lanes(image):
	lane_image = np.copy(image)
	canny_image = canny(lane_image)
	lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=50)
	try:
		averaged_lines = average_slope_intercept(lane_image, lines)
		line_image = display_lines(lane_image, averaged_lines)
		combo_image = cv2.addWeighted(lane_image, 1, line_image, 1, 1)
		return combo_image
	except:
		return frame

def arrow_detection(image):

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, green_lower, green_upper)
	res = cv2.bitwise_and(image, image, mask=mask)
	canny = cv2.Canny(mask, 80, 110)

	dot_image = np.zeros_like(canny)
	image = np.float32(canny)
	corners = cv2.goodFeaturesToTrack(canny, 20, 0.4, 5)
	corners = np.int0(corners)

	right_dots = 0
	left_dots = 0
	xs=[]
	ys=[]
	for corner in corners:
		x, y = corner.ravel()
		xs.append(x)
		ys.append(y)
		cv2.circle(dot_image, (x,y), 5, 255, -1)
	
	arrow_midpoint = int((max(xs)+min(xs))/2)
	for corner in corners:
		if corner[0][0] < int(arrow_midpoint):
			left_dots +=1
		else:
			right_dots +=1
	cv2.line(dot_image, (arrow_midpoint, max(ys)), (arrow_midpoint, min(ys)), (255, 0, 0), 1)
	if right_dots > left_dots:
		direction = 'Right'
	elif left_dots > right_dots:
		direction = 'Left'
	else:
		direction = 'Undefined'

	return direction

#frame = cv2.imread('turn_road.png')
#cv2.waitKey(0)

while True:
	_, frame=cap.read()

	lane_image = detect_lanes(frame)
	turn_image = turn(canny(frame))
	result_image = cv2.addWeighted(lane_image, 1, turn_image, 1, 1)
	cv2.imshow('result', result_image)
	#print('found h line')
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		#cv2.imwrite('turn_road.png', image)
		cv2.destroyAllWindows()
		break
