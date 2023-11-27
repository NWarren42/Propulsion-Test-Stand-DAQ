
# /++\=============================/\
# | QRET Data Aquisition and Control |
# | Main Control Program             |
#  \_/==============================/

from labjack import ljm
import numpy as np
import msvcrt
from QDAC_Class import *

#________________________________#
#                                #

handle = ljm.openS("ANY","ANY","ANY")
# Ensure triggered stream is disabled.
ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX", 0)
           # Enabling internally-clocked stream.
ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)

#________________________________#
#                                #

#---------------------#
#--KEYBOARD CONTROLS--#
#---------------------#
'''
USE:   defines buttons to be used for the control of actuators
        - Each actuator should have a button for both Open and Close
        - each command will need to be added in the SEND COMMANDS portion of the control loop
'''
# NOTE: "q" shuts down program

bOpen_N2    = b'v' #Opens N2 valve
bClose_N2   = b'c' #Closes N2 valve

bOpen_NO    = b'o' #Opens NO valve
bClose_NO   = b'i' #Closes NO valve

#-----------------------#
#--CONTROL PARAMETERS---#
#-----------------------#
'''
USE:   Variables that control data collection 
'''
alert_timer_max = 2     #Number of seconds to wait before raising a valve state error
scanrate        = 10    #How many times labjack takes data per second

#-------------#
#--ACTUATORS--#
#-------------#
'''
USE:   Define Actuators to be controlled by the system
        - Each actuator must have:
         - 2 Input pins
         - 1 Output pins
        - Declare actuators using variables defined in PINS
        - An alert system should be declared for each actuator
'''
    #--Define PINS--#

N2out_1 = "FIO4"
N2in_1  = "FIO0"
N2in_2  = "FIO1"

NOout_1 = "FIO5"
NOin_1  = "FIO2"
NOin_2  = "FIO3"

    #--Define ACTUATORS--#

N2valve = valve(handle,N2out_1,N2in_1,N2in_2)
NOvalve = valve(handle,N2out_1,N2in_1,N2in_2)

    #--Define ALERT SYSTEMS--#

N2alert = alert('N2',alert_timer_max,scanrate)
NOalert = alert('N0',alert_timer_max,scanrate)

#-----------#
#--SENSORS--#
#-----------#
'''
USE:    Define data collection Pins that will be stored by the system
        - Each Sensor class stores data from 1 pin.
'''
    #--Define PINS--#

P1in = "AIN10"

    #--Define SENSORS--#

P1 = pinOut(handle,P1in)

#=====================#
    # THE RUN LOOP #
#=====================#

# - Some Initial steps -#

intervalHandle = 1                 #An id for the interval  
intervalLength = 1000000/scanrate  #length of interval in microseconds
ljm.startInterval(intervalHandle,intervalLength)

while True:

    #//SCAN VALVE STATUS\\#
    N2valve.checkState()
    NOvalve.checkState()

    #//CHECK FOR KEYBOARD INPUT AND SEND COMMANDS\\#

    #Check for a keyboard input command
    if msvcrt.kbhit():
        command = msvcrt.getch() #saves command

        #checks if command is something important
        if   command == bClose_N2:
            N2valve.close()

        elif command == bClose_NO:
            NOvalve.close()

        elif command == bOpen_N2:
            N2valve.open()

        elif command == bOpen_NO:
            NOvalve.open()
        
        elif command == b'q':
            print("system shutting down...")
            break

    #//READ DATA\\#

    P1.takeData()

    #//ALERT SYSTEMS\\#

    N2alert.update(N2valve)
    NOalert.update(NOvalve)

    #//WAIT FOR NEXT INTERVAL\\#
    skippedIntervals = ljm.waitForNextInterval(intervalHandle)
    if skippedIntervals > 0:
         print("\nSkippedIntervals: %s" % skippedIntervals)


#======================#
 # SHUTDOWN PROCEDURE #
#======================#

#Stops the stream and closes the labjack
print("Control loop ended")
ljm.cleanInterval(intervalHandle)
ljm.close(handle)
print("labjack disconnected")
