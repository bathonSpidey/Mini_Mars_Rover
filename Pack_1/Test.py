from numpy.linalg import inv
import argparse
import imutils
import cv2
import smbus
import time
import serial
import time
from PIL import Image
import math

# inv = Inverse
# np.array = matrix zu Array fuer bearbeitung
# np.matrix = array zu matrix fuer berechnung
# Array.transpose() = Transponieren


bus = smbus.SMBus(1)
address1 = 0x04
address = 0x1e

l=True

    
while l:
    
    bus.write_i2c_block_data(address1,11,[int(90),int(0)])
    time.sleep(5)
    break