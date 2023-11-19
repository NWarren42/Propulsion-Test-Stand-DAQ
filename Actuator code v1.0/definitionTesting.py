from labjack import ljm
import numpy as np
import msvcrt
from QDAC_Class import *

handle = ljm.openS("T7","ANY","ANY")


testSensor = sensor(handle, "AIN0", 0)

testSensor.takeData

print(testSensor.data)