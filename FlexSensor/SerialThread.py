import FlexSignal as fs # flex signal
import time
import threading
import PySimpleGUI as sg

# If thread has been stopped, the program does not crash
class SerialThread(threading.Thread, sg.Window, sg.Graph):
    def __init__(self, queue, window, graph):
        self.stopped = False
        threading.Thread.__init__(self)
        self.queue = queue
        self.window = window
        self.graph = graph
        self.isRunning = True
        self.flexSignal = fs

        self.minNum = 250
        self.maxNum = 1023
        self.squareColor = '#FFFFFF'

        self.window['-CurrentMin-'].update(self.minNum)
        self.window['-MinInput-'].update(self.minNum)
        self.window['-CurrentMax-'].update(self.maxNum)
        self.window['-MaxInput-'].update(self.maxNum)

    def stop_serial_thread(self):
        print("Stopping thread")
        print(self.stopped)

        self.stopped = True

    def update_min_max(self, min, max):
        print("Update min max")
        self.minNum = min
        self.maxNum = max
        self.window['-CurrentMin-'].update(self.minNum)
        self.window['-CurrentMax-'].update(self.maxNum)

    def rgb_to_hex(self, r, g, b):
        return ('{:X}{:X}{:X}').format(r, g, b)

    def run(self):
        time.sleep(0.2)
        while not self.stopped:
            if self.flexSignal.ser.inWaiting():
                data = self.flexSignal.get_signal_data()
                if(data != ''):
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
