from labjack import ljm
import numpy as np
import msvcrt
import time
from QDAC_Class import *

handle = ljm.openS("T7","ANY","ANY")


# testSensor = sensor(handle, "AIN0", 0)

# testSensor.takeData

# print(testSensor.data)

testLoadCell = sensor(handle, "AIN0", True)

def acquireDataTimed(duration, interval): #duration and interval in seconds
        startTime = time.time()
        endTime = startTime + duration

        while time.time() < endTime:
            testLoadCell.takeData()
            print(testLoadCell.data[-1])
            time.sleep(interval)

def acquireDataIndefinite(interval):
     try:
          while(True):
            testLoadCell.takeData()
            print(testLoadCell.data[-1])
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Data acquisition was manually halted")

def printAllLoadTestData():
    for i in range(len(testLoadCell.data)):
        print(testLoadCell.data[i])

testLoadCell.wipeData()
acquireDataTimed(10, 0.01) #arbitrary time values