import PySimpleGUI as sg
import SignalClass
import time
import threading
import queue as Queue
import serial

class SerialThread(threading.Thread, sg.Window):
    def __init__(self, queue, window):
        threading.Thread.__init__(self)
        self.queue = queue
        self.window = window
        self.isRunning = True
        self.flexSignal = SignalClass.FlexSignal("Annie.csv")

        self.colorCounter = 0
        self.squareColor = '#FFFFFF'
        self.graph = self.window.Element("graph")
        self.graph.DrawRectangle((200, 200), (250, 250),fill_color=self.squareColor)
    
    def rgb_to_hex(self, r, g, b):
        return ('{:X}{:X}{:X}').format(r, g, b)

    def run(self):
        time.sleep(0.2)
        while self.isRunning:
            if self.flexSignal.ser.inWaiting():
                data = self.flexSignal.GetSignalData()
                self.window['-RawSignal-'].update(data)
                if(self.colorCounter >= 255):
                    self.colorCounter = 0
                else:
                    self.colorCounter += 1

                self.squareColor = self.rgb_to_hex(self.colorCounter,0,0)
                self.squareColor = "#" + self.squareColor
                self.graph.DrawRectangle((200, 200), (250, 250),fill_color=self.squareColor)
        

class App():
    def __init__(self):
        buttonSize = (12,3)
        textFont = 'Franklin 18'

        self.layout = [[sg.Text("Welcome, Annie", font = textFont, size = (80,1))],
        [sg.Graph(
            canvas_size=(400, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 400),
            key="graph"
        )],
            [sg.Text("This is the signal", key = '-RawSignal-', font = textFont)],
            [sg.Button('Get Signal', key = '-StartSignal-', size = buttonSize), sg.Button('Stop', key = '-StopSignal-', size = buttonSize)]]
        
        self.window = sg.Window('Press-on', self.layout)
        self.window.Finalize()
        self.running = True

        self.queue = Queue.Queue()
        self.thread = SerialThread(self.queue, self.window)
        self.thread.start()

        
        self.RunApp()

    

    def RunApp(self):
        while self.running:
            event, values = self.window.read()

            if event == '-StartSignal-':
                

                self.window['-RawSignal-'].update(4)


            if event == '-StopSignal-':
                self.window['-RawSignal-'].update(0)

            if event == sg.WIN_CLOSED:
                self.running = False
                self.thread.isRunning = False
                self.window.close()


PressOnApp = App()


