import cv2
import numpy as np
import time
import statistics
from statistics import mode
#import direction as dr
#import matplotlib.pyplot as plt

green_lower = np.array([64, 70, 86], np.uint8)
green_upper = np.array([80,255,255], np.uint8)
text_size = 0.5

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

def average_h_slope_intercept(image, lines):
	h_line_fit=[]
	for line in lines:
	    x1, y1, x2, y2 = line.reshape(4)
	    parameters = np.polyfit((x1, x2), (y1, y2), 1)
	    slope = parameters[0]
	    intercept = parameters[1]
	    if slope > -0.5 and slope < 0.5:
	    	h_line_fit.append((slope, intercept))
	h_line_fit_average = np.average(h_line_fit, axis=0)

   	

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
    polygons = np.array([[(0, 140), ]])
    #polygons = np.array([[(0, 0), (0, 640), (640, 640), (490, 640), (380, 100), (100, 160), (0, 400)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def roi_h(image):
	height = image.shape[0]
	polygons = np.array([[(0, 450), (640, 450), (640, 480), (0, 480)]])
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
    return line_image

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def arrow_image_convertion(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, green_lower, green_upper)
	res = cv2.bitwise_and(image, image, mask=mask)
	canny = cv2.Canny(mask, 80, 110)
	blur = cv2.GaussianBlur(canny, (5,5), 1)
	return blur

def check_turning(dis):
    if int(dis[1]) < 100:
        dr.goCustom(80, 90)
        #print("Adjusting left")
    elif int(dis[1]) > 150:
        dr.goCustom(90, 80)
        #print('Adjusting right')
    else:
    	#print('going forward')
        dr.goStraight()

def detect_lanes(image):
	lane_image = np.copy(image)
	canny_image = canny(lane_image)
	#cropped_image = roi(image)
	lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=50)
	averaged_lines, distances = average_slope_intercept(lane_image, lines)
	line_image = display_lines(lane_image, averaged_lines)
	combo_image = cv2.addWeighted(lane_image, 1, line_image, 1, 1)

	cv2.line(line_image, (320, 0), (320, 480), (0, 0, 255), 1)
	cv2.putText(combo_imagex, 'Lanes', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), lineType=cv2.LINE_AA)

	return combo_image, distances

def detect_h_line(image):
	h_lane_image = np.copy(image)
	canny_image = canny(h_lane_image)
	roi_image = roi_h(canny_image)
	lines = cv2.HoughLinesP(roi_image, 1, np.pi/180, 100, np.array([]), minLineLength=50, maxLineGap=50)
	if lines is not None:
		h_lane_image = display_lines(image, lines)
		combo_image = cv2.addWeighted(h_lane_image, 1, frame, 1, 1)
		cv2.putText(combo_image, 'Hor. line', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0), lineType=cv2.LINE_AA)
		turn_command=True
		return combo_image, turn_command
	else:
		turn_command=False
		cv2.putText(h_lane_image, 'Hor. line', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), lineType=cv2.LINE_AA)
		return h_lane_image, turn_command

def arrow_detection(image):
	dot_image = np.zeros_like(image)
	image = np.float32(image)
	image = arrow_image_convertion(frame)
	try:
		corners = cv2.goodFeaturesToTrack(image, 20, 0.1, 5)
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
			pass
		cv2.putText(dot_image, 'Arrow', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0), lineType=cv2.LINE_AA)
		return dot_image, direction
	except:
		cv2.putText(image, 'Hor. line', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), lineType=cv2.LINE_AA)
		return image, 'Undefined'

def turn(direction):
	if direction == 'Left':
		#dr.left()
		print('Turning left')
	if direction == 'Right':
		#dr.right()
		print('Turning right')

turn_com=False

while True:
	_, frame=cap.read()

	direction_list= []

	if turn_com==False:
		try:
			image_with_lanes, distance = detect_lanes(frame)
			check_turning(distance)
			cv2.imshow('Result', image_with_lanes)
		except:
			turn_com=True
			#dr.stop(0.5)
			print('Stop')
	else:
		try:
			image_with_h_lane, turn_command = detect_h_line(frame)
			cv2.imshow('Result', image_with_h_lane)
			print('Going for forward horizontal line')
			#dr.goStraight()
			if turn_command == True:
				for i in range(11):
					arrow_image, direction = arrow_detection(frame)
					direction_list.append(direction)
				direction = mode(direction_list)
				turn(direction)
				print("Im truning", direction)
				cv2.imshow('Result', arrow_image)
				time.sleep(2)
				turn_com=False
		except:
			pass
			cv2.putText(frame, 'Original', (10, 610), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), lineType=cv2.LINE_AA)
			cv2.imshow('Result', frame)
	
	if cv2.waitKey(10) & 0xFF == ord('q'):
	    cap.release()
	    #cv2.imwrite('roi.png', frame)
	    cv2.destroyAllWindows()
	    break
cv2.waitKey(0)