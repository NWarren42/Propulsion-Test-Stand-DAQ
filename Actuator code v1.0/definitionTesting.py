from labjack import ljm
import numpy as np
import msvcrt
import time
import websockets
import asyncio
from QDAC_Class import *

handle = ljm.openS("T7","ANY","ANY")

#Websocket connection code that hasn't worked
# def sendData():
#      with connect("ws://localhost:3000/") as websocket:
#           websocket.send(testLoadCell.data[-1])
#           message = websocket.recv()
#           print("Recieved: ", message)



#Load cell accquire data funcitons
testLoadCell = sensor(handle, "AIN0", True)

def acquireDataTimed(duration, interval): #duration is overall duration of measuring data, and interval is how often it reads and stores data, both are in seconds
        startTime = time.time()
        endTime = startTime + duration

        while time.time() < endTime:
            testLoadCell.takeData()
            print(testLoadCell.data[-1])
            time.sleep(interval)
            return testLoadCell.data[-1]

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

# More websocket code that does not fully work (not sure why)
# async def communicateWithServer():
#      url = "wss://api.golioth.io/v1/ws/"

#      async with websockets.connect(url) as ws:
                  
#         await ws.send(acquireDataTimed(10, 0.01))
#         while True:
#             recvText = await ws.recv()
#             print("> {}".format(recvText))


# asyncio.get_event_loop().run_until_complete(communicateWithServer())

acquireDataTimed(10, 0.01) #arbitrary time values