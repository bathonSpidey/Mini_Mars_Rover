import cv2
import numpy as np

#lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
#upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}

green_lower = np.array([65, 94, 18], np.uint8)
green_upper = np.array([80,255,255], np.uint8)

red_lower = np.array([0, 130, 220], np.uint8)
red_upper = np.array([10, 255, 255], np.uint8)

blue_lower = np.array([67, 70, 0], np.uint8)
blue_upper = np.array([119, 255, 255], np.uint8)
text_size = 0.5

cap = cv2.VideoCapture(0)
print("Camera connected")

def read_blue_arrow(image):
    image = cv2.flip(image, -1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    kernal = np.ones((5,5), 'uint8')
    blue = cv2.dilate(blue, kernal)
    res = cv2.bitwise_and(image, image, mask=blue)

    _, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        print(area, 'blue')
        if(area>15000):
            x,y,w,h = cv2.boundingRect(contour)
            image = cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(image, 'BLue Arrow', (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            return 'Left', image
        else:
            return 'Undefined', image
        
def read_green_arrow(image):
    image = cv2.flip(image, -1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, green_lower, green_upper)
    kernal = np.ones((5,5), 'uint8')
    blue = cv2.dilate(blue, kernal)
    res = cv2.bitwise_and(image, image, mask=blue)

    _, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        print(area, 'green')
        if(area>7000):
            x,y,w,h = cv2.boundingRect(contour)
            image = cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
            cv2.putText(image, 'Green Arrow', (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            return 'Right', image
        else:
            return 'Undefined', image

while True:
    _, frame=cap.read()
    
    try:
        
        direction_blue, arrow_image= read_blue_arrow(frame)
        direction_green, arrow_image= read_green_arrow(frame)
        if direction_green == 'Right' and direction_blue == 'Undefined':
            print('Turn right')
        elif direction_green == 'Undefined' and direction_blue == 'Left':
            print('Turn Left')
        cv2.imshow("Color Tracking", arrow_image)
    except Exception as e:
        print(e)
        

    #cv2.imshow("Color Tracking", frame)   
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
