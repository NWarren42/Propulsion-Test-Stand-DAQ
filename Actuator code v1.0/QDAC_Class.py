#.==================================.#
#| QRET Data Aquisition and Control |#
#| Class Dctionary                  |#
# \================================/ #
from labjack import ljm
import numpy as np
import time

class thermocouple:
 
    def __init__ (self, handle, pin):
        self.handle = handle
        self.address = ljm.nameToAddress(pin)

        # Creating data storage array
        self.data = []

        # Register Setup
        self.equationRegister = pin + "_EF_INDEX"
        self.unitRegister = pin + "_EF_CONFIG_A"
        self.tempOutputRegister = pin + "_EF_READ_A"

        ljm.eWriteName(handle, self.equationRegister, 22) # Set the equation to apply to the pin to be the one to handle K-type thermocouples
        ljm.eWriteName(handle, self.unitRegister, 1) # To set the temperature units. 0 = K, 1 = C, 2 = F.
    
    def takeData (self):
        self.data.append(ljm.eReadName(self.handle, self.tempOutputRegister))

class pressureTransducer:

    def __init__ (self, handle, pin):
        self.handle = handle
        self.address = ljm.nameToAddress(pin)

        # Creating data storage array
        self.data = []

    def takeData (self):
        self.data.append(ljm.eReadAddress(self.handle, self.address))

class loadCell: 
    
    def __init__ (self, handle, highPin, lowPin):
        self.handle = handle
        self.highAddress = ljm.nameToAddress(highPin)

        self.negChannelRegister = highPin + "_NEGATIVE_CH" # Creating string to access negative channel

        lowPinInt = int(''.join(filter(str.isdigit, lowPin))) # Parsing negative pin input to get the integer value of the pin
        ljm.eWriteName(self.handle, self.negChannelRegister, lowPinInt) # Writing integer value of relative pin to neg channel register

        # Creating data storage array
        self.data = []

    def takeData (self):
            self.data.append(ljm.eReadAddress(self.handle, self.highAddress))

