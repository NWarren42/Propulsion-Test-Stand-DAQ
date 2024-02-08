from labjack import ljm
import numpy as np
import msvcrt
from QDAC_Class import *
import time

handle = ljm.openS("T7","ANY","ANY")


testSensor = thermocouple(handle, "AIN0")

#print(ljm.eReadName(handle, testSensor.tempOutputRegister))



for i in range(0, 1000): 
    time.sleep(0.1)
    testSensor.takeData()
    print(testSensor.data[i])


