from tkinter import *
import queue as Queue
import TkinterSerialThread as thread
import TkinterFlexSignal as fs
import time
isDebugging = False

root = Tk()

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
title = Label(text="Press-On", font=("Arial", 24), background="pink")
title.grid(row = titleRow, column = 0, columnspan = 2)

# Greeting
greeting = Label(text = "Hello! This is Press-On, an Application designed to help you visualize the pressure that a user is applying to a ball.", font=("Arial", 16), wraplength=300)
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

debugButton = Button(root, text = "Debug", command = toggleDebugging, width = 10)
debugButton.grid(row = debugButtonRow, column = 0, columnspan = 2)


# Setup main Canvas
root.geometry(f"{screenWidth}x{screenHeight}")
canvas = Canvas(root, width=screenWidth//3*2, height=screenHeight//2, background="pink")
canvas.grid(row = canvasRow, column = 0)

# Setup debugging Canvas
# debuggingCanvas = Canvas(root, width=screenWidth//3*2, height=screenHeight//3, background="green")
# debuggingCanvas.pack()

debuggingFrame = Frame(root, background="red", width=screenWidth//3*2, height=screenHeight//4)
debuggingFrame.grid(row = debuggingFrameRow, column = 0, columnspan = 2)

# Debugging section
rawValue = 1023
currentRawValue = Label(debuggingFrame, text=f"I am a mock value: {rawValue}", font=("Arial", 16))
currentRawValue.grid(row = currentRawValueRow, column = 0)

#
# Min Max labels and input
#
minNumLabel = Label(debuggingFrame, text="Min: ", font=("Arial", 16))
minNumLabel.grid(row = minNumRow, column = 0)

fooBar = "Foo Bar"
minNumInput = Entry(debuggingFrame, name="a-name", textvariable=fooBar, border=4, background="pink")
minNumInput.grid(row = minNumRow, column = 1)

maxNumLabel = Label(debuggingFrame, text="Max: ", font=("Arial", 16), justify="left")
maxNumLabel.grid(row = maxNumRow, column = 0)

maxNumInput = Entry(debuggingFrame, border=4, background="pink")
maxNumInput.grid(row = maxNumRow, column = 1)

#
# Testing
#
normalizedValue = .9
normalizedValueLabel = Label(debuggingFrame, text=f"I am a normalized value{normalizedValue}", background="green")
normalizedValueLabel.grid(row = colorDataRow, column = 0)

r = 50
g = 50
b = 50
rgbColorLabel = Label(debuggingFrame, text = f"({r}, {g}, {b})")
rgbColorLabel.grid(row = colorDataRow, column = 1)

def printFoo():
    # minNumInput.focus_force()
    print(fooBar)

square = canvas.create_rectangle(150, 150, 350, 350, fill="blue")

def changeColor():
    current_color = canvas.itemcget(circle, "fill")
    if current_color == "green":
        canvas.itemconfig(circle, fill="red")
    else:
        canvas.itemconfig(circle, fill="green")
    root.after(1000, changeColor)

circle = canvas.create_oval(50, 50, 150, 150, fill="green")
changeColor()

# running = True
# serial_queue = Queue.Queue()

# serial_thread = thread.SerialThread(serial_queue, root, square)
# serial_thread.start()
root.update_idletasks()
root.withdraw()
root.geometry(f"+{(root.winfo_screenwidth() - root.winfo_reqwidth()) // 2}+{(root.winfo_screenheight() - root.winfo_reqheight()) // 2}")
root.deiconify()

debuggingFrame.grid_forget() # Starts with forgetting the debugging frame so it doesnt appear
root.mainloop()
