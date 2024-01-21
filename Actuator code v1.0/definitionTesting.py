from labjack import ljm
import numpy as np
import msvcrt
import time
import keyboard
from QDAC_Class import *

handle = ljm.openS("T7","ANY","ANY")


# testSensor = sensor(handle, "AIN0", 0)

# testSensor.takeData

# print(testSensor.data)

testLoadCell = sensor(handle, "AIN0", True)

# Acquire data from a sensor for a set amount of time
def acquireDataTimed(duration, interval): #duration and interval in seconds, duration is total data collection time and interval is how frequently it collects data
        startTime = time.time()
        endTime = startTime + duration

        while time.time() < endTime:
            testLoadCell.takeData()
            print(testLoadCell.data[-1])
            time.sleep(interval)

# Acquire data from a sensor with no predetermined end time, it will end with user input into the terminal (Ctrl + C)
def acquireDataIndefinite(interval):
    stopAcquisition = False

    if keyboard.is_pressed('space'):
         stopAcquisition = True
         print("Data acquisition was manually halted")

    try:
        while(not stopAcquisition):
            testLoadCell.takeData()
            print(testLoadCell.data[-1])
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Data acquisition was stopped using keyboard interrupt")

def printAllLoadTestData():
    for i in range(len(testLoadCell.data)):
        print(testLoadCell.data[i])

# testLoadCell.wipeData()