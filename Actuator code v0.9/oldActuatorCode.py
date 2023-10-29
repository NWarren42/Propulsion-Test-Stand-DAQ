from labjack import ljm
import time
import msvcrt
import numpy as np
​
#---------------------#
#--KEYBOARD CONTROLS--#
#---------------------#
​
bOpen_N2    = b'v' #Opens N2 valve
bClose_N2   = b'c' #Closes N2 valve
​
bOpen_NO    = b'o' #Opens NO valve
bClose_NO   = b'i' #Closes NO valve
​
#----OTHER DEFINABLES-----#
Alert_timer_max = 2    #Number of seconds to wait before raising a valve state error
scanrate = 10         #How many times labjack takes data per second
​
​
#-- LABJACK DIO ports for actuator--#
N2in_1  = "FIO0"
N2in_2  = "FIO1"
​
NOin_1  = "FIO2"
NOin_2  = "FIO3"
​
N2out_1 = "FIO4"
#N2out_2 = N/A
​
NOout_1 = "FIO5"
#NOout_2 = N/A
​
#-- LABJACK READ ports --# (need to add a variable for each one below class definitions)
Tin_1 = ""
Tin_2 = ""
Pin_1 = "AIN10"
Pin_2 = ""
​
#put all read ports in this array
#used to define which ports to read from during stream
namelist = [Pin_1]
​
readAdresses,readTypes = ljm.namesToAddresses(len(namelist),namelist)
​
#--Opening labjack and confiuring pins--#
​
handle = ljm.openS("ANY","ANY","ANY")
​
#ljm.eStreamStop(handle) # in case stream is still running
​
​
class valve:
    def __init__(self,handle,Pout1,Pin1,Pin2):
​
        self.Pout = Pout1   #defines pin used to control valve
        self.Pin1 = Pin1    #defines pins used to read valve state
        self.Pin2 = Pin2
        self.handle = handle
​
        self.control = False # Desired state of valve (False = Closed, True = Open)
        self.state = False  #Current state of valve
        self.moving = False #whether valve is moving or not
​
    def open(self):
        ljm.eWriteName(self.handle,self.Pout,1)
        self.control = True
        return
​
    def close(self):
        ljm.eWriteName(self.handle,self.Pout,0)
        self.control = False
        return
​
    def checkState(self):
        #read DIO ports
        in1 = ljm.eReadName(self.handle,self.Pin1)
        in2 = ljm.eReadName(self.handle,self.Pin2)
​
        if in1 == 1 and in2 == 1:
            self.state = False
        elif in1 == 1 and in2 == 0:
            self.state = True
        elif in1 == 0 and in2 == 0:
            self.moving = True
        else:
            print("N2 valve : unknown position")
            print(in1,in2)
        return 
​
class PinOut:
    def __init__ (self,handle,PinName,filename):
        self.handle = handle
        self.name = PinName
        self.address,self.type = ljm.nameToAddress(PinName)
        self.data = []
        self.file = filename
​
    def TakeData(self):
        value = ljm.eReadAddress(self.handle, self.address)
        self.data.append(value)
        return
​
    def WipeData(self):
        self.data = []
        return
    
    def SavetoCSV(self):
        DatatoSave = np.array(self.data)
        np.savetxt(self.file,DatatoSave,delimiter=",",fmt='%f')
        return
​
​
​
#---VALVES---#
N2Valve = valve(handle,N2out_1,N2in_1,N2in_2)
NOValve = valve(handle,NOout_1,NOin_1,NOin_2)
​
#---PINOUTS---#
Pressure1 = PinOut(handle,Pin_1,"PT1.csv")
​
​
#Initiallizing alert timer variables
alert_N2 = 0
alert_NO = 0
​
#TEST PART#
ljm.eWriteName(handle,"DIO7",1)
​
# Ensure triggered stream is disabled.
ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX", 0)
​
           # Enabling internally-clocked stream.
ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)
​
print("control loop starting...")
#start stream
intervalHandle = 1
intervalLength = 1000000/scanrate  #length of interval in microseconds
dt = 1/scanrate  #length of intervat in seconds
alertmax = Alert_timer_max/(intervalLength/1000000)
ljm.startInterval(intervalHandle,intervalLength)
​
#control loop
while True:
    # print("control signal: ",N2Valve.control)
    # print("read system state: ",N2Valve.state)
    
    #Scan valve status:
    N2Valve.checkState()            # It is important that imputs gets read before sending output commands.
    NOValve.checkState()            #Otherwise the statements that valves have opened or closed may not get activated
​
    #Check for a keyboard input command
    if msvcrt.kbhit():
        command = msvcrt.getch() #saves command
​
        #checks if command is something important
        if   command == bClose_N2:
            N2Valve.close()
​
        elif command == bClose_NO:
            NOValve.close()
​
        elif command == bOpen_N2:
            N2Valve.open()
​
        elif command == bOpen_NO:
            NOValve.open()
        
        elif command == b'q':
            print("system shutting down...")
            break
​
    #Counters to alert if valve has failed to change state, as well as announce a change of state
    #Counts up as time passes with state discontinuity
    if N2Valve.control != N2Valve.state:
        alert_N2 += 1       
    if NOValve.control != NOValve.state:
        alert_NO += 1
​
    #Alert system for N2 valve
    if alert_N2 > 0:
​
        #If State has been corrected
        if N2Valve.control == N2Valve.state:
            alert_N2 = 0
            N2Valve.moving = False
            if N2Valve.state == True:
                print("N2 valve is OPEN")
                print("response time: {} ms".format(alert_N2*dt*1000))
            else:
                print("N2 valve is ClOSED")
                print("response time: {} ms".format(alert_N2*dt*1000))
        
        #If state has not yet been corrected
        else: 
            #If it has been too long and state has not changed
            if alert_N2 >= alertmax:
                alert_N2 = 0
                if N2Valve.state == True:
                    print("N2 valve has FAILED to CLOSE")
                        #Resest valve control
                    N2Valve.control = N2Valve.open()   
                    
                else:
                    print("N2 valve has FAILED to OPEN")
                        #Reset valve control
                    N2Valve.control = N2Valve.close()
​
    #Alert system for NO valve
    if alert_NO > 0:
​
        #If State has been corrected
        if NOValve.control == NOValve.state:
            alert_NO = 0
            NOValve.moving = False
            if NOValve.state == True:
                print("NO valve is OPEN")
                print("response time: {} ms".format(alert_NO*dt*1000))
            else:
                print("NO valve is ClOSED")
                print("response time: {} ms".format(alert_NO*dt*1000))
                
        
        #If state has not yet been corrected
        else: 
            #If it has been too long and state has not changed
            if alert_NO >= alertmax:
                alert_NO = 0 
                if NOValve.state == True:
                    print("NO valve has FAILED to CLOSE")
                        #Resest valve control
                    NOValve_control = NOValve.open()   
                    
                else:
                    print("NO valve has FAILED to OPEN")
                        #Reset valve control
                    NOValve.control = NOValve.close()
​
​
    #-----DATA Aquisition-----#
    #run the Takedata function for each Pinout type variable.
    Pressure1.TakeData()
                                 
  
    skippedIntervals = ljm.waitForNextInterval(intervalHandle)
    if skippedIntervals > 0:
         print("\nSkippedIntervals: %s" % skippedIntervals)
​
#Stops the stream and closes the labjack
print("Control loop ended")
ljm.cleanInterval(intervalHandle)
ljm.close(handle)
print("labjack disconnected")