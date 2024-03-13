import TkinterFlexSignal as fs, time, threading, tkinter as tk
import math
import serial.tools.list_ports

class SerialThread(threading.Thread):
    def __init__(self, queue, uiElements, startingCom):
        threading.Thread.__init__(self)
        self.queue = queue
        self.uiElements = uiElements

        # If the connection is not found, the serial thread should not start
        self.flexSignal = fs

        # selected_com = "COM4"
        # selected_com = "/dev/cu.usbserial-210"
        success = self.flexSignal.startConnection(startingCom)
        self.pauseCondition = threading.Condition(threading.Lock())
        if success:
            self.lockAcquired = False
            print("Connection was succesfull")
        else:
            self.pause()
            # self.window["-COM-"].update(f"Invalid USB port '{selected_com}'. Please select another COM. ")
            print("Connection failed, add a valid connection")

        self.squareColor = '#FFAFFF'
        self.minNum = 0
        self.maxNum = 650

        print("Finish initializing")

    def updateCom(self, com):
        self.flexSignal.endConnection()
        if com == "No port selected":
            print("The selected port was the 'No port selected', the program will not continue")
            self.pause()
            return
        success = self.flexSignal.startConnection(com)
        if not success:
            print("The selected port was not valid, the program will not continue")
            self.pause()
            return
        self.resume()
        
    def pause(self):
        print("Pausing")
        self.pauseCondition.acquire()
        self.lockAcquired = True
    
    def resume(self):
        if self.lockAcquired:
            self.lockAcquired = False
            self.pauseCondition.notify()
            self.pauseCondition.release()

    def updateMin(self, min):
        self.minNum = min
        print(f"Updating min in serial thread with Min: {self.minNum}")
        self.uiElements["minNumLabel"].configure(text = "Current min: " + str(self.minNum))

    def updateMax(self, max):
        self.maxNum = max
        print(f"Updating max in serial thread with Max : {self.maxNum}")
        self.uiElements["maxNumLabel"].configure(text = "Current max: " + str(self.maxNum))

    def rgbToHex(self, r, g, b):
        return ('{:02X}{:02X}{:02X}').format(r, g, b)

    def run(self):
        time.sleep(0.2)
        while True:
            comPorts = [comport.device for comport in serial.tools.list_ports.comports()]
            # Check if the current COM port is in the list

            if self.flexSignal.serialSignal.port not in comPorts:
                # If the COM port does not exist, pause the thread and continue to the next iteration
                self.uiElements["currentCom"].set("")
                self.pause()
                continue

            with self.pauseCondition:
                while self.lockAcquired:
                    self.pauseCondition.wait()
                
                if self.flexSignal.serialSignal.inWaiting():
                    data = self.flexSignal.getSignalData()
                    if(data != ''):
                        normalizedData = (int(data) - int(self.minNum) ) / (int(self.maxNum) - int(self.minNum))
                    else:
                        normalizedData = 0

                    self.uiElements["currentRawInputLabel"].configure(text = "Raw input: " + str(data))
                    
                    if(normalizedData > 1):
                        normalizedData = 1
                    elif (normalizedData < 0):
                        normalizedData = 0

                    # i want to create a "transformed" value from the normalized data so the closer it is to 0, the more it impacts that the number is smaller, and the closer it is to one, the less it impacts the decrease. For example: the decrease from 1 to 0.9 impacts less than the decrease from 0.1 to 0. Make the transformation logarithmic please.
                    normalizedData = 1 - (1 - normalizedData) ** 2

                    # epsilon = 1e-7
                    # normalizedData = 1 - math.log(normalizedData + epsilon)

                    self.uiElements["normalizedInputLabel"].configure(text = "Norm. input: " + str(round(normalizedData, 3)))
                    
                    g = round(min(255, 2* 255 * normalizedData))
                    r = round(min(255, 2* 255 * (1-normalizedData)))

                    
                    self.uiElements["rgbColorLabel"].configure(text = "RGB: " + str(r) + ", " + str(g) + ", 0")
                    visualizationColor = "#" + self.rgbToHex(r, g, 00)
                    self.uiElements["canvas"].itemconfig(self.uiElements["visualization"], fill=visualizationColor)
                    self.uiElements["hexColorLabel"].configure(text = "Hex: " + visualizationColor)
