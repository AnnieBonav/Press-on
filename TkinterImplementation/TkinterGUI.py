from tkinter import *
import queue as Queue, customtkinter as ctk
import TkinterSerialThread as thread
import TkinterFlexSignal as fs
import time
from tkinter import messagebox
from enum import Enum

isDebugging = False

root = ctk.CTk()

class ErrorType(Enum):
    MIN_NUM_BIGGER_THAN_MAX_NUM = "I am sorry, but the minimum input you are trying to save is bigger than the current maximum input. Please update with a valid number."
    MAX_NUM_SMALLER_THAN_MAX_NUM = "I am sorry, but the maximum input you are trying to save is smaller than the current minimum input. Please update with valid number."
    MAX_NUM_BIGGER_THAN_1023 = "I am sorry, but the maximum input you are trying to save is bigger than 1023. Please update with a valid number."
    MIN_NUM_SMALLER_THAN_1 = "I am sorry, but the minimum input you are trying to save is smaller than 1. Please update with a valid number."
    INVALID_MIN_NUMBER = "I am sorry, but your input for the minimum input is not a valid number. Please make sure it does not contain letters or special characters."
    INVALID_MAX_NUMBER = "I am sorry, but your input for the maximum input is not a valid number. Please make sure it does not contain letters or special characters."

# Setup main variables
screenWidth = root.winfo_screenwidth() // 2
screenHeight = root.winfo_screenheight() // 6 * 5

titleRow = 0
greetingRow = 1
canvasRow = 2
debugButtonRow = 4
debuggingFrameRow = 5
currentRawInputRow = debuggingFrameRow + 1
currentNumsLabel = currentRawInputRow + 1
minNumRow = currentNumsLabel + 1
maxNumRow = minNumRow + 1
colorDataRow = maxNumRow + 1

visualizationSize = 400
initialMin = 1
initialMax = 650

# Title
title = ctk.CTkLabel(root, text="Press-On", font=("Helvetica", 24))
title.grid(row = titleRow, column = 0, columnspan = 2, pady = 10)

# Greeting
greeting = ctk.CTkLabel(root, text = "Hello! This is Press-On, an Application designed to help you visualize the pressure that a user is applying to a ball.", font=("Arial", 16), wraplength=300, pady=10, padx=10, justify="center")
greeting.grid(row = greetingRow, column = 0, columnspan=2)


def toggleDebugging():
    global isDebugging
    if isDebugging:
        debuggingFrame.grid_forget()
    else:
        debuggingFrame.grid(row = 3, column = 0, columnspan = 2)
    
    isDebugging = not isDebugging
    debugButton.configure(text = "Debug" if not isDebugging else "Stop Debugging")

debugButton = ctk.CTkButton(root, text = "Debug", command = toggleDebugging, width = 10, font=("Arial", 14))
debugButton.grid(row = debugButtonRow, column = 0, columnspan = 2, pady = 10)


# Setup main Canvas
# root.geometry(f"{screenWidth}x{screenHeight}")
canvas = ctk.CTkCanvas(root, width = visualizationSize, height = visualizationSize)
canvas.grid(row = canvasRow, column = 0, padx=40, pady = 20)

debuggingFrame = ctk.CTkFrame(root, width=screenWidth//3*2, height=screenHeight//4)
debuggingFrame.grid(row = debuggingFrameRow, column = 0, columnspan = 2)

# Debugging section
currentRawInputLabel = ctk.CTkLabel(debuggingFrame, text=f"Raw input: -1", font=("Arial", 16))
currentRawInputLabel.grid(row = currentRawInputRow, column = 0)

#
# Min Max labels and input
#
minNumLabel = ctk.CTkLabel(debuggingFrame, text = f"Current Min: {initialMin}", font=("Arial", 16))
minNumLabel.grid(row = currentNumsLabel, column = 0)
maxNumLabel = ctk.CTkLabel(debuggingFrame, text = f"Current Max: {initialMax}", font=("Arial", 16))
maxNumLabel.grid(row = currentNumsLabel, column = 1, pady=10)

minNumLabelTitle = ctk.CTkLabel(debuggingFrame, text="Min: ", font=("Arial", 16))
minNumLabelTitle.grid(row = minNumRow, column = 0)

minVar = ctk.IntVar()
minVar.set(initialMin)
minNumInput = ctk.CTkEntry(debuggingFrame, textvariable = minVar, justify="right")
minNumInput.grid(row = minNumRow, column = 1)

maxNumLabelTitle = ctk.CTkLabel(debuggingFrame, text = "Max: ", font=("Arial", 16))
maxNumLabelTitle.grid(row = maxNumRow, column = 0, pady=10)

maxVar = ctk.IntVar()
maxVar.set(initialMax)
maxNumInput = ctk.CTkEntry(debuggingFrame, textvariable = maxVar, justify="right")
maxNumInput.grid(row = maxNumRow, column = 1)

normalizedInputLabel = ctk.CTkLabel(debuggingFrame, text=f"Normalized input: -1", width = 150)
normalizedInputLabel.grid(row = colorDataRow, column = 0)

rgbColorLabel = ctk.CTkLabel(debuggingFrame, text = f"RGB: -1, -1, -1", width = 150)
rgbColorLabel.grid(row = colorDataRow, column = 1)

hexColorLabel = ctk.CTkLabel(debuggingFrame, text = f"Hex: #F00000", width = 150)
hexColorLabel.grid(row = colorDataRow, column = 2)

visualization = canvas.create_oval(10, 10, 400, 400, fill="white")

root.update_idletasks()
root.withdraw()
root.geometry(f"+{(root.winfo_screenwidth() - root.winfo_reqwidth()) // 2}+{(root.winfo_screenheight() - root.winfo_reqheight()) // 2}")
root.deiconify()

debuggingFrame.grid_forget() # Starts with forgetting the debugging frame so it doesnt appear

running = True
serialQueue = Queue.Queue()
elementsDictionary = {
    "minNumLabel": minNumLabel,
    "maxNumLabel": maxNumLabel,
    "canvas": canvas,
    "visualization": visualization,
    "rgbColorLabel": rgbColorLabel,
    "hexColorLabel" : hexColorLabel,
    "currentRawInputLabel" : currentRawInputLabel,
    "normalizedInputLabel" : normalizedInputLabel
}
serialThread = thread.SerialThread(serialQueue, elementsDictionary)
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

root.mainloop()
