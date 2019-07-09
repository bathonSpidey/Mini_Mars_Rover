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

def goCustom(a,b):
    bus.write_i2c_block_data(address1,2,[int(a), int(b)]) #From the back Left-wheel speed and Right-wheel speed

def goStraight():
    bus.write_i2c_block_data(address1,11,[int(90),int(90)] )#From the back Left-wheel speed and Right-wheel speed
    
def stop(sleep_time):
    bus.write_i2c_block_data(address1,4,[int(90),int(90)])
    time.sleep(sleep_time)
    
def left():
    bus.write_i2c_block_data(address1,3,[int(90),int(90)])
    time.sleep(2)

def leftCustom(angle):
    bus.write_i2c_block_data(address1,12,[int(angle),0])
    time.sleep(2)
    

"""  
def reverse(sleep_time):
    bus.write_i2c_block_data(address1,10,[int(90),int(90)])
    time.sleep(sleep_time)
"""

def right():
    bus.write_i2c_block_data(address1,9,[int(90),int(90)])
    time.sleep(2)
    bus.write_i2c_block_data(address1,4,[int(90),int(90)])

def rightCustom(angle):
    bus.write_i2c_block_data(address1,13,[int(angle),0])
    time.sleep(2)
    
def read_distance():
    number=bus.read_i2c_block_data(address1,0,1)
    return number[0]

    

if __name__=="__main__":
    while True:
        pass

        

