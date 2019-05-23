import cv2


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
<<<<<<< HEAD
    cam.set(28,12)
    cam.set(10,100)
    cam.set(3, 1280) # set the resolution
    cam.set(4, 720)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
=======
    #cam.set(28,12)
    #cam.set(10,100)
>>>>>>> 9b0291587e33e734ff07e0ca536970e2a7c2b7be
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=False)


if __name__ == '__main__':
    main()
