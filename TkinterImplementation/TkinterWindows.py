from tkinter import *
import queue as Queue, customtkinter as ctk
import PressOnFlexSignal as poSignal
from tkinter import messagebox
from enum import Enum
import threading, re, serial.tools.list_ports, math, time

class ErrorType(Enum):
    MIN_NUM_BIGGER_THAN_MAX_NUM = "I am sorry, but the minimum input you are trying to save is bigger than the current maximum input. Please update with a valid number."
    MAX_NUM_SMALLER_THAN_MAX_NUM = "I am sorry, but the maximum input you are trying to save is smaller than the current minimum input. Please update with valid number."
    MAX_NUM_BIGGER_THAN_1023 = "I am sorry, but the maximum input you are trying to save is bigger than 1023. Please update with a valid number."
    MIN_NUM_SMALLER_THAN_1 = "I am sorry, but the minimum input you are trying to save is smaller than 1. Please update with a valid number."
    INVALID_MIN_NUMBER = "I am sorry, but your input for the minimum input is not a valid number. Please make sure it does not contain letters or special characters."
    INVALID_MAX_NUMBER = "I am sorry, but your input for the maximum input is not a valid number. Please make sure it does not contain letters or special characters."

class WindowsPressOnUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Press-On")
        self.isDebugging = False
        self.running = True
        #
        # VARIABLES
        #
        self.currentCom = ctk.StringVar()
        self.comPorts = []
        self.comInfo = []
        self.comComboBox = ctk.CTkComboBox(self, values = self.comPorts, font=("Arial", 14), command = self.comPicker)
        self.serialQueue = Queue.Queue()
        ## self.serialThread = thread.SerialThread(self.serialQueue)

        self.uiValues = {
            "titleRow" : 0,
            "greetingRow" : 1,
            "canvasRow" : 2,
            "comInfoRow" : 3,
            "debugButtonRow" : 4,
            "debuggingFrameRow" : 5,
            "currentRawInputRow" : 6,
            "currentNumsLabel" : 7,
            "minNumRow" : 8,
            "maxNumRow" : 9,
            "otherDataRow" : 10,
            "visualizationSize" : 400,
            "initialMin" : 1,
            "initialMax" : 650,
            "screenWidth" : self.winfo_screenwidth() // 2,
            "screenHeight" : self.winfo_screenheight() // 6 * 5,
            "minVar" : ctk.IntVar(),
            "maxVar" : ctk.IntVar(),
            "min" : -1,
            "max" : -1,
        }

        # Call starting functions
        self.initializeComPorts()

        #
        # ELEMENTS Section
        #

        # Title
        self.title = ctk.CTkLabel(self, text="Press-On", font=("Helvetica", 24))
        self.title.grid(row = self.uiValues["titleRow"], column= 0, pady = 10, columnspan = 2)

        # Greeting
        self.greeting = ctk.CTkLabel(self, text = "Hello! This is Press-On, an Application designed to help you visualize the pressure that a user is applying to a ball.", font=("Arial", 16), wraplength=450, pady=10, padx=10, justify="center")
        self.greeting.grid(row = self.uiValues["greetingRow"], column = 0, columnspan = 2, padx = 20)
        
        # Canvas
        self.canvas = ctk.CTkCanvas(self, width = self.uiValues["visualizationSize"], height = self.uiValues["visualizationSize"])
        self.canvas.grid(row = self.uiValues["canvasRow"], column = 0, padx=40, pady = 20, columnspan = 2)
        # Visualization
        self.visualization = self.canvas.create_oval(10, 10, 400, 400, fill="white")

        #
        # COM Port Section
        #

        # Combo COM Port selection
        self.comComboBox = ctk.CTkComboBox(self, values = self.comPorts, font=("Arial", 14), command = self.comPicker)
        self.comComboBox.grid(row = self.uiValues["comInfoRow"], column = 0)
                
        self.currentCom.trace_add("write", self.handleComChange)
        self.currentCom.set(self.comComboBox.get())
        for com in self.comInfo:
            if re.search(r"USB Serial", com):
                print(f"Found COM Port with 'USB Serial': {com}")
                self.comComboBox.set(self.comPorts[self.comInfo.index(com)])
                self.currentCom.set(self.comPorts[self.comInfo.index(com)])
                break
        
        # Refresh COM Port button
        self.refreshComPortButton = ctk.CTkButton(self, text = "Refresh COM Ports", command = self.refreshComPorts, font=("Arial", 14))
        self.refreshComPortButton.grid(row = self.uiValues["comInfoRow"], column = 1)

        #
        # Debug Section
        #
        # Debug button
        self.debugButton = ctk.CTkButton(self, text = "Debug", command = self.toggleDebugging, width = 10, font=("Arial", 14))
        self.debugButton.grid(row = self.uiValues["debugButtonRow"], column = 0, columnspan = 2, pady = 10)

        # Debugging Frame
        self.debuggingFrame = ctk.CTkFrame(self, width=self.uiValues["screenWidth"]//3*2, height=self.uiValues["screenHeight"]//4)
        self.debuggingFrame.grid(row = self.uiValues["debuggingFrameRow"], column = 0, columnspan = 2)

        # Debugging section
        self.currentRawInputLabel = ctk.CTkLabel(self.debuggingFrame, text=f"Raw input: -1", font=("Arial", 16))
        self.currentRawInputLabel.grid(row = self.uiValues["currentRawInputRow"], column = 0)

        #
        # Min Max Section
        #

        # Current MinNum Label
        self.currentMinNumLabel = ctk.CTkLabel(self.debuggingFrame, text = f"Current Min: {self.uiValues['initialMin']}", font=("Arial", 16))
        self.currentMinNumLabel.grid(row = self.uiValues["currentNumsLabel"], column = 0)
        # Min num label
        self.minNumLabel = ctk.CTkLabel(self.debuggingFrame, text="Min: ", font=("Arial", 16))
        self.minNumLabel.grid(row = self.uiValues["minNumRow"], column = 0)
        # Min num input	variable
        self.uiValues["minVar"].set(self.uiValues["initialMin"])
        self.uiValues["min"] = self.uiValues["initialMin"]
        # Min num input
        self.minNumInput = ctk.CTkEntry(self.debuggingFrame, textvariable = self.uiValues["minVar"], justify="right")
        self.minNumInput.grid(row = self.uiValues["minNumRow"], column = 1)

        # Current MaxNum Label
        self.currentMaxNumLabel = ctk.CTkLabel(self.debuggingFrame, text = f"Current Max: {self.uiValues['initialMax']}", font=("Arial", 16))
        self.currentMaxNumLabel.grid(row = self.uiValues["currentNumsLabel"], column = 1, pady=10)
        # Max num label
        self.maxNumLabelTitle = ctk.CTkLabel(self.debuggingFrame, text = "Max: ", font=("Arial", 16))
        self.maxNumLabelTitle.grid(row = self.uiValues["maxNumRow"], column = 0, pady=10)
        # Max num input variable
        self.uiValues["maxVar"].set(self.uiValues["initialMax"])
        self.uiValues["max"] = self.uiValues["initialMax"]
        # Max num input
        self.maxNumInput = ctk.CTkEntry(self.debuggingFrame, textvariable = self.uiValues["maxVar"], justify="right")
        self.maxNumInput.grid(row = self.uiValues["maxNumRow"], column = 1)

        #
        # Other data section
        #
        # Normalized data label
        self.normalizedInputLabel = ctk.CTkLabel(self.debuggingFrame, text=f"Normalized input: -1", width = 150)
        self.normalizedInputLabel.grid(row = self.uiValues["otherDataRow"], column = 0)
        # RGB color label
        self.rgbColorLabel = ctk.CTkLabel(self.debuggingFrame, text = f"RGB: -1, -1, -1", width = 150)
        self.rgbColorLabel.grid(row = self.uiValues["otherDataRow"], column = 1)
        # Hex color label
        self.hexColorLabel = ctk.CTkLabel(self.debuggingFrame, text = f"Hex: #F00000", width = 150)
        self.hexColorLabel.grid(row = self.uiValues["otherDataRow"], column = 2)

        # Handling starting window stuff
        self.update_idletasks()
        # self.withdraw()
        self.geometry(f"+{(self.winfo_screenwidth() - self.winfo_reqwidth()) // 2}+{(self.winfo_screenheight() - self.winfo_reqheight()) // 2}")
        # self.deiconify()
        self.debuggingFrame.grid_forget() # Starts with forgetting the debugging frame so it doesnt appear

        self.uiElements = {
            "currentMinNumLabel": self.currentMinNumLabel,
            "currentMaxNumLabel": self.currentMaxNumLabel,
            "canvas": self.canvas,
            "visualization": self.visualization,
            "rgbColorLabel": self.rgbColorLabel,
            "hexColorLabel" : self.hexColorLabel,
            "currentRawInputLabel" : self.currentRawInputLabel,
            "normalizedInputLabel" : self.normalizedInputLabel,
            "currentCom" : self.currentCom
        }

        # Initializes the serial thread with the elements dictionary (so the thread can update the elements) and the com port (so the thread can use it to begin the listening)
        ## self.serialThread.initialize(self.uiElements, self.comComboBox.get())
        ## self.serialThread.start()

        self.minNumSave = ctk.CTkButton(self.debuggingFrame, text="Save", command = self.updateMin)
        self.minNumSave.grid(row = self.uiValues["minNumRow"], column = 2)

        maxNumSave = ctk.CTkButton(self.debuggingFrame, text="Save", command = self.updateMax)
        maxNumSave.grid(row = self.uiValues["maxNumRow"], column = 2)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        # Create serial connection
        self.flexSignal = poSignal
        self.startConnection(self.comComboBox.get())

        # Create a new thread and start it
        updateThread = threading.Thread(target = self.threadTask)
        updateThread.start()

        self.mainloop()

    def startConnection(self, startingCom):
        success = self.flexSignal.startConnection(startingCom)
        self.pauseCondition = threading.Condition(threading.Lock())
        if success:
            self.lockAcquired = False
            print("Connection was succesfull")
        else:
            self.pause()
            print("Connection failed, add a valid connection")
    
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

    def rgbToHex(self, r, g, b):
        return ('{:02X}{:02X}{:02X}').format(r, g, b)

    def getUpdatedData(self):
        comPorts = [comport.device for comport in serial.tools.list_ports.comports()]
            # Check if the current COM port is in the list

        if self.flexSignal.serialSignal.port not in comPorts:
            # If the COM port does not exist, pause the thread and continue to the next iteration
            self.uiElements["currentCom"].set("")
            self.pause()
            return
    
        minVar = self.uiValues["min"]
        maxVar = self.uiValues["max"]
        data = self.flexSignal.getSignalData()
        if data != "":
            try:
                normalizedData = (int(data) - int(minVar)) / (int(maxVar) - int(minVar))
            except Exception:
                return
        else:
            normalizedData = 0

        self.rawInput = data
        self.uiElements["currentRawInputLabel"].configure(text = "Raw input: " + str(data))

        # i want to create a "transformed" value from the normalized data so the closer it is to 0, the more it impacts that the number is smaller, and the closer it is to one, the less it impacts the decrease. For example: the decrease from 1 to 0.9 impacts less than the decrease from 0.1 to 0. Make the transformation logarithmic please.
        normalizedData = 1 - (1 - normalizedData) ** 2

        # TODO: Abstract the decision of the transformation to a method that can be selected by the therapist
        # epsilon = 1e-7
        # normalizedData = 1 - math.log(normalizedData + epsilon)

        if int(self.rawInput) == 1023:
            normalizedData = 1
        if(normalizedData > 1):
            normalizedData = 1
        elif (normalizedData < 0):
            normalizedData = 0

        self.normalizedData = str(round(normalizedData, 3))

        self.uiElements["normalizedInputLabel"].configure(text = "Norm. input: " + self.normalizedData)
        
        g = round(min(255, 2* 255 * normalizedData))
        r = round(min(255, 2* 255 * (1-normalizedData)))
        rgbLabel = "RGB: " + str(r) + ", " + str(g) + ", 0"
        self.uiElements["rgbColorLabel"].configure(text = rgbLabel)

        color = self.rgbToHex(r, g, 00)
        visualizationColor = "#" + color
        self.uiElements["canvas"].itemconfig(self.uiElements["visualization"], fill = visualizationColor)
        self.uiElements["hexColorLabel"].configure(text = "Hex: " + visualizationColor)
    
    def threadTask(self):
        while self.running:
            self.getUpdatedData()


    def onClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.flexSignal.endConnection()
            self.running = False
            time.sleep(2)
            self.destroy()

    def popup(self, errorType : ErrorType) :
        messagebox.showerror("Error updating the numbers", errorType.value)  

    def updateMin(self):
        min = self.uiValues["minVar"].get()
        max = self.uiValues["maxVar"].get()
        print("GOT MIN")
        try:
            min = int(min)
        except:
            self.popup(ErrorType.INVALID_MIN_NUMBER)
            return
        
        if min <= 0:
            self.popup(ErrorType.MIN_NUM_SMALLER_THAN_1)
            return
        
        elif min >= max:
            self.popup(ErrorType.MIN_NUM_BIGGER_THAN_MAX_NUM)
            return
        
        print(f"Updating Min: {min}")
        self.uiValues["min"] = min
        self.uiElements["currentMinNumLabel"].configure(text = f"Current Min: {min}")

    def updateMax(self):
        min = self.uiValues["minVar"].get()
        max = self.uiValues["maxVar"].get()
        print("GOT MAX")
        try:
            max = int(max)
        except:
            self.popup(ErrorType.INVALID_MAX_NUMBER)
            return
        
        if max <= min:
            self.popup(ErrorType.MAX_NUM_SMALLER_THAN_MAX_NUM)
            return
        
        if max > 1023:
            self.popup(ErrorType.MAX_NUM_BIGGER_THAN_1023)
            return

        print(f"Updating Max: {max}")
        self.uiValues["max"] = max
        self.uiElements["currentMaxNumLabel"].configure(text = f"Current Max: {max}")

    #
    # METHODS
    #
        
    def handleComChange(self, *args):
        com = self.currentCom.get()
        print(f"Com changed to '{com}'")
        if com == "":
            self.comComboBox.set(self.comPorts[-1])
            print("Com is empty, probably because the serial thread detected that it is missing. Setting to 'No port selected'")
            return
    
    def initializeComPorts(self):
        # Get all available COM ports
        self.comPorts = [port.device for port in serial.tools.list_ports.comports()]
        # Get more information about the connected devices on the COM ports
        self.comInfo = []
        for port in self.comPorts:
            self.comInfo.append(serial.tools.list_ports.comports()[self.comPorts.index(port)].description)

        self.comPorts.append("No port selected")
        self.comInfo.append("No info to show")

        # Print the list of COM ports and their corresponding device information
        for port, info in zip(self.comPorts, self.comInfo):
            print(f"COM Port: {port}, Device Info: {info}")

        # Print the list of COM ports
        print(self.comPorts, "\n\n")

    def comPicker(self, something):
        print("Com picker something", something)
        newCom = self.comComboBox.get()
        print(f"Updating COM in Serial Thread to {newCom}")
        self.updateCom(newCom)
        ## self.serialThread.updateCom(newCom)

    def toggleDebugging(self):
        if self.isDebugging:
            self.debuggingFrame.grid_forget()
        else:
            self.debuggingFrame.grid(row = self.uiValues["debuggingFrameRow"], column = 0, columnspan = 2)
        
        self.isDebugging = not self.isDebugging
        self.debugButton.configure(text = "Debug" if not self.isDebugging else "Stop Debugging")

    def refreshComPorts(self):
        print("Refreshing COM Ports")
        self.comPorts.clear()
        self.comPorts = [port.device for port in serial.tools.list_ports.comports()]
        comInfo = []
        for port in self.comPorts:
            print("Port: ", port)
            comInfo.append(serial.tools.list_ports.comports()[self.comPorts.index(port)].description)

        self.comPorts.append("No port selected")
        comInfo.append("No info to show")

        self.comComboBox.destroy()
        self.comComboBox = ctk.CTkComboBox(self, values = self.comPorts, font=("Arial", 14), command = self.comPicker)
        self.comComboBox.grid(row = self.uiValues["comInfoRow"], column = 0)

        # looks if the com that was selected still exists, if it does, then it is chosen. If it does not, then the first com is chosen
        com = self.currentCom.get()
        if com in self.comPorts:
            self.comComboBox.set(com)
            return
        # If the com that was selected is not in the list anymore, then the "No port selected" is chosen
        self.comComboBox.set(self.comPorts[-1])

if __name__ == "__main__":
    app = WindowsPressOnUI()
    print("App ended")

    
    