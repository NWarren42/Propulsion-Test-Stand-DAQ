#.==================================.#
#| QRET Data Aquisition and Control |#
#| Class Dctionary                  |#
# \================================/ #
from labjack import ljm
import numpy as np
import time


#/----------------\#
#| Actuator Valve |#
#\----------------/#
'''
DEF : Intended for use with HANBAY MDx-xxxDT5 actuated ball valve 

INPUTS:
    [int] handle   - the handle of a connected LabJack
    [string] Pout1 - [Grey] Output pin, used for controlling state of valve
    [string] Pin1  - [Brown] first of two input pins used for reading state of valve
    [string] Pin2  - [Blue] second of two input pins used for reading state of valve

FIELDS :
    [int] handle   - stores handle of connected LabJack 
    [string] Pout  - stores output pin 
    [string] Pin1  - stores input pin 1 
    [string] Pin2  - stores input pin 2 
    [bool] control - The desired state of the valve (False = Closed, True = Open)
    [bool] state   - The actual state of the valve (False = Closed, True = Open)
    [bool] move    - Describes if Valve is currently moving (False = Static, True = Moving)

METHODS :
    open        - commands valve to open
    close       - commands valve to close
    checkState  - reads input pins to determine if valve is open, closed, or moving

'''
class valve:    
    def __init__(self,handle,Pout1,Pin1,Pin2):

        self.handle = handle
        self.Pout = Pout1   #defines pin used to control valve
        self.Pin1 = Pin1    #defines pins used to read valve state
        self.Pin2 = Pin2 

        self.control = False # Desired state of valve (False = Closed, True = Open)
        self.state = False  #Current state of valve
        self.move = False #whether valve is moving or not

    def open(self):
        ljm.eWriteName(self.handle,self.Pout,1)
        self.control = True
        return

    def close(self):
        ljm.eWriteName(self.handle,self.Pout,0)
        self.control = False
        return

    def checkState(self):           
        #read DIO ports
        in1 = ljm.eReadName(self.handle,self.Pin1)
        in2 = ljm.eReadName(self.handle,self.Pin2)

        # decides state based on actuator manual reference 
        if in1 == 1 and in2 == 1:
            self.state = False
        elif in1 == 1 and in2 == 0:
            self.state = True
        elif in1 == 0 and in2 == 0:
            self.move = True
        else:
            print("N2 valve : unknown position")
            print(in1,in2)
        return 

#/-----------------------\#
#| Actuator Alert System |#
#\-----------------------/#  
'''
DEF : An alert system for a valve. tracks response time and informs if a valve did not reach it's destination
    - Each valve should be assigned its own alert system.

INPUTS : 
    [string] name        - name of the monitered valve
    [int]    maxTime     - The time in seconds to wait before flagging a failed movement and reseting the valve
    [int]    scanRate    - The scan rate of the labJack

FEILDS :
    [string] name    - Stores the name of the valve
    [int]    maxTime - Stores the maximum amount of time to wait for a valve movement
    [int]    dt      - The timestep between each iterval of the labJack
    [int]    count   - counter for determining response time. Also used to flag failed movements

METHODS :
    update - updates the alert system as to the current state of the valves. The method is in charge of the following tasks:
             - reseting the system on move completion
             - keeping track of response times
             - flagging failiures to move
        Inputs:
            [class] valve - The valve that the alert system is assigned to. See "valve" class for more information on valve fields.

'''

class alert:
    def __init__(self,name,maxTime,scanRate):
        
        self.name       = name
        self.maxCount    = maxTime*scanRate
        self.dt         = 1/scanRate
        self.count      = 0
        
    def update(self,valve):

        #check if there is descrepancy in desired vs. actual state
        if (valve.control == valve.state):
            if self.count > 0: 

                #display state change and response time
                if valve.state == True:
                    print("{} valve is OPEN".format(self.name))
                    print("response time: {} ms".format(self.count*self.dt*1000))
                else:
                    print("{} valve is ClOSED".format(self.name))
                    print("response time: {} ms".format(self.count*self.dt*1000))

                #reset count
                self.count = 0
        
        #If there is a discrepancy
        else:
            self.count += 1
            if valve.move == False :        #If valve is moving then we don't care
                  
                #if too much time has elapsed, reset valve and inform user
                if self.count >= self.maxCount:
                    self.count = 0 
                    if valve.state == True:
                        print("{} valve has FAILED to CLOSE".format(self.name))
                        #Resest valve control
                        valve.open()   
                    
                    else:
                        print("{} valve has FAILED to OPEN".format(self.name))
                            #Reset valve control
                        valve.close()
        return  
   

#/--------------\#
#| Sensor Input |#
#\--------------/#
'''
DEF: collects, stores, and writes input data from the specified pin
   - uses numpy to save data to file

INPUTS:
    [int] handle     - the handle of a connected LabJack
    [string] pinName - Name of input pin for data collection

FIELDS:
    [int]handle   - stores handle of connected LabJack 
    [string] name - Name of the Pin being read 
    [int] address - Adress of the Pin being read
    type          - Type of Pin being read
    [list] data   - list of data collected

METHODS:
    takeData    - reads the pin from LabJack and adds value to data.
    wipeData    - clears all data stored
    savetoCSV   - saves stored data in a csv file
        Inputs:
            [string] file - filepath to save data

'''

class sensor:           
    def __init__ (self,handle,dataPin,differential):
        self.handle = handle
        self.address,self.type = ljm.nameToAddress(dataPin)
        
        if(len(dataPin)==5): # If the specified pin has 5 characters, it has a double digit index
            pinNumber = int(dataPin[3] + dataPin[4])
        else:
            pinNumber = int(dataPin[3])

        diffString = dataPin + "_NEGATIVE_CH"
        if(differential):
            ljm.eWriteName(handle, diffString, pinNumber + 1) # Sets relative pin to the pin adjacent to it
        else:
            ljm.eWriteName(handle, "AIN0_NEGATIVE_CH", "AIN_COM") # Set relative pin to ground if non-differential measurement

        
        self.data = []

    def takeData(self):
        value = ljm.eReadAddress(self.handle, self.address, 3) #The number at the end corresponds to the datatype, 3 represents LJM_FLOAT32 which I believe is a 32 bit floating point number
        self.data.append(value)
        return

    def wipeData(self):
        self.data = []
        return
    
    def savetoCSV(self,fileName):
        DatatoSave = np.array(self.data)
        np.savetxt("/tests/" + fileName + '-' + time.asctime,DatatoSave,delimiter=",",fmt='%f')
        return
