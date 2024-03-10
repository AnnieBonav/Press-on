import TkinterFlexSignal as fs, time, threading, tkinter as tk

class SerialThread(threading.Thread):
    def __init__(self, queue, minNumLabel, maxNumLabel, canvas, rectangle):
        threading.Thread.__init__(self)
        self.queue = queue
        # self.root = root
        self.canvas = canvas
        self.rectangle = rectangle

        # If the connection is not found, the serial thread should not start
        self.flexSignal = fs

        # selected_com = "COM4"
        selected_com = "/dev/cu.usbserial-210"
        success = self.flexSignal.start_connection(selected_com)
        self.pause_condition = threading.Condition(threading.Lock())
        if success:
            self.paused = False
            # self.window["-COM-"].update("Selected COM: " + str(selected_com))
            print("Connection was succesfull")
        else:
            self.pause()
            # self.window["-COM-"].update(f"Invalid USB port '{selected_com}'. Please select another COM. ")
            print("Connection failed, add a valid connection")

        self.squareColor = '#FFAFFF'
        self.minNum = 0
        self.maxNum = 650
        self.minNumLabel = minNumLabel
        self.maxNumLabel = maxNumLabel

        print("Finish initializing")

    def pause(self):
        self.paused = True
        print("Pausing")
        self.pause_condition.acquire()
    
    def resume(self):
        self.paused = False
        self.pause_condition.notify()
        self.pause_condition.release()

    def updateMinMax(self, min, max):
        print("Update min max")
        self.minNum = min
        self.maxNum = max

        self.minNumLabel = self.minNum
        self.maxNumLabel = self.maxNum

        print("NEW MIN: ", self.minNum)
        print("NEW MAX: ", self.maxNum)

    def rgbToHex(self, r, g, b):
        return ('{:02X}{:02X}{:02X}').format(r, g, b)

    def run(self):
        time.sleep(0.2)
        while True:
            with self.pause_condition:
                while self.paused:
                    self.pause_condition.wait()
                
                if self.flexSignal.serial_signal.inWaiting():
                    data = self.flexSignal.get_signal_data()
                    if(data != ''):
                        normalizedData = (int(data) -self.minNum) / (self.maxNum - self.minNum)
                    else:
                        normalizedData = 0

                    # self.window['-RawSignal-'].update(data)
                    

                    if(normalizedData > 1):
                        normalizedData = 1
                    elif (normalizedData < 0):
                        normalizedData = 0
                    
                    print("Normalized Data: ", normalizedData)
                    # self.window['-NormalizedSignal-'].update(normalizedData)
                    
                    g = round(min(255, 2* 255 * normalizedData))
                    r = round(min(255, 2* 255 * (1-normalizedData)))

                    # self.window['-RGB-'].update(str(r) + ", " + str(g) + ", 0")
                    self.squareColor = self.rgbToHex(r, g, 00)
                    print("RGB: ", r, g, 0)
                    self.squareColor = "#" + self.squareColor
                    print(self.squareColor)
                    self.canvas.itemconfig(self.rectangle, fill=self.squareColor)
                    # self.window['-Hex-'].update(self.squareColor)

                        # self.graph.DrawCircle((100, 100), 100,fill_color = self.squareColor)
                        # canvas.itemconfig(circle, fill="red")
                    #self.window.itemconfig(self.graph(fill = self.squareColor))