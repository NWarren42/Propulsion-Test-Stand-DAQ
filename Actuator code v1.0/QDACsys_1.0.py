
# /++\=============================/\
# | QRET Data Aquisition and Control |
# | Main Control Program             |
#  \_/==============================/

from labjack import ljm
import numpy as np
import msvcrt
from QDAC_Class import *

#----- Creating Labjack Instance -----#
handle = ljm.openS("ANY","ANY","ANY")

#-----------------------#
#--CONTROL PARAMETERS---#
#-----------------------#
'''
USE:   Variables that control data collection 
'''
scanrate = 10    #How many times labjack takes data per second

#-----------#
#--SENSORS--#
#-----------#
'''
USE:    Define data collection Pins that will be stored by the system
        - Each Sensor class stores data from 1 pin.
'''
    #--Define PINS--#

TC1In = "AIN0"


    #--Define SENSORS--#



#=====================#
    # THE RUN LOOP #
#=====================#

# - Some Initial steps -#

intervalHandle = 1                 #An id for the interval  
intervalLength = 1000000/scanrate  #length of interval in microseconds
ljm.startInterval(intervalHandle,intervalLength)

while True:

    #//CHECK FOR KEYBOARD INPUT AND SEND COMMANDS\\#

    #Check for a keyboard input command
    if msvcrt.kbhit():
        command = msvcrt.getch() #saves command

        #checks if command is something important
        if command == b'q':
            print("System shutting down...")
            break

    #//READ DATA\\#

    P1.takeData()

    #//WAIT FOR NEXT INTERVAL\\#
    skippedIntervals = ljm.waitForNextInterval(intervalHandle)
    if skippedIntervals > 0:
         print("\nSkippedIntervals: %s" % skippedIntervals)


#======================#
 # SHUTDOWN PROCEDURE #
#======================#


ljm.close(handle)
print("labjack disconnected")
