import FlexSignal as fs # flex signal
import time
import threading
import PySimpleGUI as sg


# If thread has been stopped, the program does not crash
class SerialThread(threading.Thread, sg.Window, sg.Graph):
    def __init__(self, queue, window, graph):
        threading.Thread.__init__(self)
        self.queue = queue
        self.window = window
        self.graph = graph
        # If the connection is not found, the serial thread should not start
        self.flexSignal = fs
        success = self.flexSignal.start_connection("COM4")

        self.pause_condition = threading.Condition(threading.Lock())
        if success:
            self.paused = False
            print("Connection was succesfull")
        else:
            self.pause()
            print("Connection failed, add a valid connection")

        self.minNum = 250
        self.maxNum = 1023
        self.squareColor = '#FFFFFF'

        self.window['-CurrentMin-'].update(self.minNum)
        self.window['-MinInput-'].update(self.minNum)
        self.window['-CurrentMax-'].update(self.maxNum)
        self.window['-MaxInput-'].update(self.maxNum)
        print("Finish initializing")

    def pause(self):
        self.paused = True
        print("Pausing")
        self.pause_condition.acquire()
    
    def resume(self):
        self.paused = False
        self.pause_condition.notify()
        self.pause_condition.release()

    def update_min_max(self, min, max):
        print("Update min max")
        self.minNum = min
        self.maxNum = max
        self.window['-CurrentMin-'].update(self.minNum)
        self.window['-CurrentMax-'].update(self.maxNum)

    def rgb_to_hex(self, r, g, b):
        return ('{:X}{:X}{:X}').format(r, g, b)

    def run(self):
        print("i am in run")
        time.sleep(0.2)
        while True:
            with self.pause_condition:
                while self.paused:
                    self.pause_condition.wait()
                
                if self.flexSignal.serial_signal.inWaiting():
                    data = self.flexSignal.get_signal_data()
                    if(data != ''):
                        print(type(data), data, " minNum: ", self.minNum, " maxNum: ", self.maxNum)
                        normalizedData = (int(data) -self.minNum) / (self.maxNum - self.minNum)
                    else:
                        normalizedData = 0
                    self.window['-RawSignal-'].update(data)
                    

                    if(normalizedData > 1):
                        normalizedData = 1
                    elif (normalizedData < 0):
                        normalizedData = 0
                        
                    self.window['-NormalizedSignal-'].update(normalizedData)
                    
                    g = round(min(255, 2* 255 * normalizedData))
                    r = round(min(255, 2* 255 * (1-normalizedData)))

                    self.window['-RGB-'].update(str(r) + ", " + str(g) + ", 0")
                    self.squareColor = self.rgb_to_hex(r, g, 00)
                    self.squareColor = "#" + self.squareColor + "0"
                    self.window['-Hex-'].update(self.squareColor)

                    self.graph.DrawCircle((100, 100), 100,fill_color = self.squareColor)
                    #self.graph.DrawRectangle((200, 200), (250, 250),fill_color= 'red')
