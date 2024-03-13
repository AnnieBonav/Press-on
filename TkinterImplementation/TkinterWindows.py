from tkinter import *
import queue as Queue, customtkinter as ctk
import TkinterSerialThread as thread
import TkinterFlexSignal as fs
import time
from tkinter import messagebox
from enum import Enum
import threading
import re, serial.tools.list_ports

class ErrorType(Enum):
    MIN_NUM_BIGGER_THAN_MAX_NUM = "I am sorry, but the minimum input you are trying to save is bigger than the current maximum input. Please update with a valid number."
    MAX_NUM_SMALLER_THAN_MAX_NUM = "I am sorry, but the maximum input you are trying to save is smaller than the current minimum input. Please update with valid number."
    MAX_NUM_BIGGER_THAN_1023 = "I am sorry, but the maximum input you are trying to save is bigger than 1023. Please update with a valid number."
    MIN_NUM_SMALLER_THAN_1 = "I am sorry, but the minimum input you are trying to save is smaller than 1. Please update with a valid number."
    INVALID_MIN_NUMBER = "I am sorry, but your input for the minimum input is not a valid number. Please make sure it does not contain letters or special characters."
    INVALID_MAX_NUMBER = "I am sorry, but your input for the maximum input is not a valid number. Please make sure it does not contain letters or special characters."

isDebugging = False


class WindowsPressOnUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Press-On")

        #
        # VARIABLES
        #
        self.currentCom = ctk.StringVar()
        self.comPorts = []
        self.comInfo = []
        self.comComboBox = ctk.CTkComboBox(self, values = self.comPorts, font=("Arial", 14), command = self.comPicker)
        self.serialQueue = Queue.Queue()
        self.serialThread = thread.SerialThread(self.serialQueue)

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
            "colorDataRow" : 10,
            "visualizationSize" : 400,
            "initialMin" : 1,
            "initialMax" : 650,
            "screenWidth" : self.winfo_screenwidth() // 2,
            "screenHeight" : self.winfo_screenheight() // 6 * 5,
        }

        # Call starting functions
        self.initializeComPorts()

        #
        # ELEMENTS
        #

        # Title
        self.title = ctk.CTkLabel(self, text="Press-On", font=("Helvetica", 24))
        self.title.grid(row = self.uiValues["titleRow"], column= 0, pady = 10, columnspan = 2)

        # Greeting
        self.greeting = ctk.CTkLabel(self, text = "Hello! This is Press-On, an Application designed to help you visualize the pressure that a user is applying to a ball.", font=("Arial", 16), wraplength=450, pady=10, padx=10, justify="center")
        self.greeting.grid(row = self.uiValues["greetingRow"], column = 0, columnspan = 2, padx = 20)
        
        #
        # Setup Canvas
        #
        canvas = ctk.CTkCanvas(self, width = self.uiValues["visualizationSize"], height = self.uiValues["visualizationSize"])
        canvas.grid(row = self.uiValues["canvasRow"], column = 0, padx=40, pady = 20, columnspan = 2)

        #
        # COM Port selection
        #
        comComboBox = ctk.CTkComboBox(self, values = self.comPorts, font=("Arial", 14), command = lambda : self.comPicker(self,self.comComboBox.get()))
        comComboBox.grid(row = self.uiValues["comInfoRow"], column = 0)
        
        self.currentCom.trace_add("write", self.handleComChange)
        self.currentCom.set(comComboBox.get())
        for com in self.comInfo:
            if re.search(r"USB Serial", com):
                print(f"Found COM Port with 'USB Serial': {com}")
                comComboBox.set(self.comPorts[self.comInfo.index(com)])
                self.currentCom.set(self.comPorts[self.comInfo.index(com)])
                break

        refreshComPortButton = ctk.CTkButton(self, text = "Refresh COM Ports", command = self.refreshComPorts, font=("Arial", 14))
        refreshComPortButton.grid(row = self.uiValues["comInfoRow"], column = 1)

        #
        # Debug button
        #

        debugButton = ctk.CTkButton(self, text = "Debug", command = self.toggleDebugging, width = 10, font=("Arial", 14))
        debugButton.grid(row = self.uiValues["debugButtonRow"], column = 0, columnspan = 2, pady = 10)

        #
        # Setup debugging Frame
        #
        debuggingFrame = ctk.CTkFrame(self, width=self.uiValues["screenWidth"]//3*2, height=self.uiValues["screenHeight"]//4)
        debuggingFrame.grid(row = self.uiValues["debuggingFrameRow"], column = 0, columnspan = 2)

        # Debugging section
        currentRawInputLabel = ctk.CTkLabel(debuggingFrame, text=f"Raw input: -1", font=("Arial", 16))
        currentRawInputLabel.grid(row = self.uiValues["currentRawInputRow"], column = 0)

        #
        # Min Max labels and input
        #
        minNumLabel = ctk.CTkLabel(debuggingFrame, text = f"Current Min: {self.uiValues['initialMin']}", font=("Arial", 16))
        minNumLabel.grid(row = self.uiValues["currentNumsLabel"], column = 0)
        maxNumLabel = ctk.CTkLabel(debuggingFrame, text = f"Current Max: {self.uiValues['initialMax']}", font=("Arial", 16))
        maxNumLabel.grid(row = self.uiValues["currentNumsLabel"], column = 1, pady=10)

        minNumLabelTitle = ctk.CTkLabel(debuggingFrame, text="Min: ", font=("Arial", 16))
        minNumLabelTitle.grid(row = self.uiValues["minNumRow"], column = 0)

        minVar = ctk.IntVar()
        minVar.set(self.uiValues["initialMin"])
        minNumInput = ctk.CTkEntry(debuggingFrame, textvariable = minVar, justify="right")
        minNumInput.grid(row = self.uiValues["minNumRow"], column = 1)

        maxNumLabelTitle = ctk.CTkLabel(debuggingFrame, text = "Max: ", font=("Arial", 16))
        maxNumLabelTitle.grid(row = self.uiValues["maxNumRow"], column = 0, pady=10)

        maxVar = ctk.IntVar()
        maxVar.set(self.uiValues["initialMax"])
        maxNumInput = ctk.CTkEntry(debuggingFrame, textvariable = maxVar, justify="right")
        maxNumInput.grid(row = self.uiValues["maxNumRow"], column = 1)

        normalizedInputLabel = ctk.CTkLabel(debuggingFrame, text=f"Normalized input: -1", width = 150)
        normalizedInputLabel.grid(row = self.uiValues["colorDataRow"], column = 0)

        rgbColorLabel = ctk.CTkLabel(debuggingFrame, text = f"RGB: -1, -1, -1", width = 150)
        rgbColorLabel.grid(row = self.uiValues["colorDataRow"], column = 1)

        hexColorLabel = ctk.CTkLabel(debuggingFrame, text = f"Hex: #F00000", width = 150)
        hexColorLabel.grid(row = self.uiValues["colorDataRow"], column = 2)

        visualization = canvas.create_oval(10, 10, 400, 400, fill="white")

        self.update_idletasks()
        # self.withdraw()
        self.geometry(f"+{(self.winfo_screenwidth() - self.winfo_reqwidth()) // 2}+{(self.winfo_screenheight() - self.winfo_reqheight()) // 2}")
        # self.deiconify()
        self.mainloop()

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

    def comPicker(self, choice):
        newCom = self.comComboBox.get()
        print(f"Updating COM in Serial Thread to {newCom}")
        self.serialThread.updateCom(newCom)

    def toggleDebugging(self, isDebugging):
        if isDebugging:
            self.debuggingFrame.grid_forget()
        else:
            self.debuggingFrame.grid(row = self.debuggingFrameRow, column = 0, columnspan = 2)
        
        isDebugging = not isDebugging
        self.debugButton.configure(text = "Debug" if not isDebugging else "Stop Debugging")

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
        self.comComboBox = ctk.CTkComboBox(self, values = self.comPorts, font=("Arial", 14), command = lambda: self.comPicker(self.comComboBox.get()))
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
    


def RunUI():
        
    
    

    debuggingFrame.grid_forget() # Starts with forgetting the debugging frame so it doesnt appear
    elementsDictionary = {
        "minNumLabel": minNumLabel,
        "maxNumLabel": maxNumLabel,
        "canvas": canvas,
        "visualization": visualization,
        "rgbColorLabel": rgbColorLabel,
        "hexColorLabel" : hexColorLabel,
        "currentRawInputLabel" : currentRawInputLabel,
        "normalizedInputLabel" : normalizedInputLabel,
        "currentCom" : currentCom
    }

    serialThread.initialize(elementsDictionary, comComboBox.get())
    serialThread.start()

    def popup(errorType) :
        messagebox.showerror("Error updating the numbers",errorType.input)  

    def updateMin():
        min = minVar.get()
        max = maxVar.get()
        print("GOT MIN")
        try:
            min = int(min)
        except:
            popup(ErrorType.INVALID_MIN_NUMBER)
            return
        
        if min <= 0:
            popup(ErrorType.MIN_NUM_SMALLER_THAN_1)
            return
        
        elif min >= max:
            popup(ErrorType.MIN_NUM_BIGGER_THAN_MAX_NUM)
            return
        
        print(f"Updating Min: {min}")
        serialThread.updateMin(min)

    def updateMax():
        min = minVar.get()
        max = maxVar.get()
        print("GOT MAX")
        try:
            max = int(max)
        except:
            popup(ErrorType.INVALID_MAX_NUMBER)
            return
        
        if max <= min:
            popup(ErrorType.MAX_NUM_SMALLER_THAN_MAX_NUM)
            return
        
        if max > 1023:
            popup(ErrorType.MAX_NUM_BIGGER_THAN_1023)
            return

        print(f"Updating Max: {max}")
        serialThread.updateMax(max)

    minNumSave = ctk.CTkButton(debuggingFrame, text="Save", command = updateMin)
    minNumSave.grid(row = minNumRow, column = 2)

    maxNumSave = ctk.CTkButton(debuggingFrame, text="Save", command = updateMax)
    maxNumSave.grid(row = maxNumRow, column = 2)


    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()