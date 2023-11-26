from labjack import ljm
import numpy as np
import msvcrt
import time
from QDAC_Class import *

handle = ljm.openS("T7","ANY","ANY")


# testSensor = sensor(handle, "AIN0", 0)

testLoadCell = sensor(handle, "AIN0", True)

# testSensor.takeData

# print(testSensor.data)

def acquireContinuousData(duration, interval): #duration and interval in seconds
        start_time = time.time()
        end_time = start_time + duration

        while time.time() < end_time:
            testLoadCell.takeData()
            time.sleep(interval)

def printLoadTestData():
    for i in range(len(testLoadCell.data)):
        print(testLoadCell.data[i])

acquireContinuousData(10, 0.01)
printLoadTestData()