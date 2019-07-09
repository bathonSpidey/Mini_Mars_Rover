import cv2
import numpy as np

green_lower = np.array([57, 151, 18], np.uint8)
green_upper = np.array([80,255,255], np.uint8)
text_size = 0.5

def convert_image(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,green_lower, green_upper)
	res = cv2.bitwise_and(image, image, mask=mask)
	canny = cv2.Canny(mask, 80, 110)
	blur = cv2.GaussianBlur(canny, (5,5), 1)
	return blur

def arrow_detection(image):
    dot_image = np.zeros_like(image)
    image = np.float32(image)
    image = convert_image(frame)
    try:
        corners = cv2.goodFeaturesToTrack(image, 100, 0.1, 5)
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
    except Exception as p:
        print(p)
        return image, 'Undefined'

cap = cv2.VideoCapture(0)
print("Camera connected")

while True:
	_, frame=cap.read()

	#image = cv2.imread('download.png')
	canny_image = convert_image(frame)
	try:
            dot_image, direction = arrow_detection(canny_image)
            print(direction)
            cv2.imshow('result', dot_image)     
	except Exception as e: print(e)
	
	
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break
	
#cv2.waitKey(0)