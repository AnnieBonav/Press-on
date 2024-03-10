from tkinter import *
import queue as Queue, customtkinter as ctk
import TkinterSerialThread as thread
import TkinterFlexSignal as fs
import time
isDebugging = False

root = ctk.CTk()

# Setup main variables
screenWidth = root.winfo_screenwidth() // 2
screenHeight = root.winfo_screenheight() // 6 * 5

titleRow = 0
greetingRow = 1
canvasRow = 2
debugButtonRow = 4
debuggingFrameRow = 5
currentRawValueRow = debuggingFrameRow + 1
minNumRow = currentRawValueRow + 1
maxNumRow = minNumRow + 1
colorDataRow = maxNumRow + 1

# Title
title = ctk.CTkLabel(root, text="Press-On", font=("Helvetica", 24))
title.grid(row = titleRow, column = 0, columnspan = 2, pady = 10)

# Greeting
greeting = ctk.CTkLabel(root, text = "Hello! This is Press-On, an Application designed to help you visualize the pressure that a user is applying to a ball.", font=("Arial", 16), wraplength=300)
greeting.grid(row = greetingRow, column = 0, columnspan=2)


def toggleDebugging():
    printFoo()
    global isDebugging
    print("Toggling debugging, was", isDebugging)
    if isDebugging:
        debuggingFrame.grid_forget()
    else:
        debuggingFrame.grid(row = 3, column = 0, columnspan = 2)
    
    isDebugging = not isDebugging
    print("Toggling debugging, now", isDebugging)
    debugButton["text"] = "Debug" if not isDebugging else "Stop Debugging"

debugButton = ctk.CTkButton(root, text = "Debug", command = toggleDebugging, width = 10, font=("Arial", 14))
debugButton.grid(row = debugButtonRow, column = 0, columnspan = 2, pady = 10)


# Setup main Canvas
# root.geometry(f"{screenWidth}x{screenHeight}")
canvas = ctk.CTkCanvas(root, width=screenWidth//3*2, height=screenHeight//2, bg="white")
canvas.grid(row = canvasRow, column = 0, padx=40)

debuggingFrame = ctk.CTkFrame(root, width=screenWidth//3*2, height=screenHeight//4)
debuggingFrame.grid(row = debuggingFrameRow, column = 0, columnspan = 2)

# Debugging section
rawValue = 1023
currentRawValue = ctk.CTkLabel(debuggingFrame, text=f"I am a mock value: {rawValue}", font=("Arial", 16))
currentRawValue.grid(row = currentRawValueRow, column = 0)

#
# Min Max labels and input
#
minNumLabel = Label(debuggingFrame, text="Min: ", font=("Arial", 16))
minNumLabel.grid(row = minNumRow, column = 0)

fooBar = ctk.Variable()
minNumInput = ctk.CTkEntry(debuggingFrame, textvariable = fooBar)
minNumInput.grid(row = minNumRow, column = 1)


maxNumLabel = ctk.CTkLabel(debuggingFrame, text = "Max: ", font=("Arial", 16), justify="left")
maxNumLabel.grid(row = maxNumRow, column = 0)

maxNumInput = ctk.CTkEntry(debuggingFrame)
maxNumInput.grid(row = maxNumRow, column = 1)


#
# Testing
#
normalizedValue = .9
normalizedValueLabel = ctk.CTkLabel(debuggingFrame, text=f"I am a normalized value{normalizedValue}")
normalizedValueLabel.grid(row = colorDataRow, column = 0)

r = 50
g = 50
b = 50
rgbColorLabel = ctk.CTkLabel(debuggingFrame, text = f"({r}, {g}, {b})")
rgbColorLabel.grid(row = colorDataRow, column = 1)

def printFoo():
    # minNumInput.focus_force()
    print(fooBar)

rectangle = canvas.create_rectangle(150, 150, 350, 350, fill="blue")
rectangle = canvas.create_rectangle(150, 150, 350, 350, fill="red")


def changeColor():
    current_color = canvas.itemcget(circle, "fill")
    if current_color == "green":
        canvas.itemconfig(circle, fill="red")
    else:
        canvas.itemconfig(circle, fill="green")
    root.after(1000, changeColor)

circle = canvas.create_oval(50, 50, 150, 150, fill="green")
changeColor()

root.update_idletasks()
root.withdraw()
root.geometry(f"+{(root.winfo_screenwidth() - root.winfo_reqwidth()) // 2}+{(root.winfo_screenheight() - root.winfo_reqheight()) // 2}")
root.deiconify()

debuggingFrame.grid_forget() # Starts with forgetting the debugging frame so it doesnt appear


running = True
serialQueue = Queue.Queue()

serialThread = thread.SerialThread(serialQueue, minNumLabel, maxNumLabel, canvas, rectangle)
serialThread.start()

def updateNumbers():
    serialThread.updateMinMax(int(minNumInput.get()), int(maxNumInput.get()))

updateNumbersButton = ctk.CTkButton(debuggingFrame, text="Update Min-Max", command = updateNumbers)
updateNumbersButton.grid(row = 10, column = 0, columnspan = 2)

root.mainloop()
