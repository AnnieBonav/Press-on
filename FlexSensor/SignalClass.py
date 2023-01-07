import serial
import os

class FlexSignal:
    def __init__(self, fileName):
        self.fileName = fileName
        self.arduinoPort = "COM3"
        self.baud = 9600
        
        self.minSignal = 23
        self.maxSignal = 1023
        self.dataSamples = 40

        self.isRunning = False
        
        self.StartConnection()
        
    
    def StartConnection(self):
        print("before serial")
        self.ser = serial.Serial(self.arduinoPort, self.baud)
        print("Connected to arduino port: " + self.arduinoPort)
        #file = open(self.dataFileName, "a")

    def GetSignalData(self):
        #while self.isRuning: # I create an implicit listener: whenever I change this value oustide, the function will stop running
        getData = str(self.ser.readline())
        data = getData[2:][:-5]
        print(data)
        #return data

    def WriteToFile(self):
        data = 0 #Data should be equal to something gotten from the port
        file = open(self.dataFileName, "a")
        file.write(data + "\n")

    def PrintFileName(self):
        print(self.fileName)