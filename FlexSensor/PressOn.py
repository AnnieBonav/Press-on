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
    
    def run(self):
        time.sleep(0.2)
        while self.isRunning:
            if self.flexSignal.ser.inWaiting():
                data = self.flexSignal.GetSignalData()
                self.window['-RawSignal-'].update(data)
        

class App():
    def __init__(self):
        self.layout = [  [sg.Text("Welcome, Annie")],
            [sg.Text("This is the signal", key = '-RawSignal-')],
            [sg.Button('Get Signal', key = '-StartSignal-'), sg.Button('Stop', key = '-StopSignal-')] ]
        self.window = sg.Window('Window Title', self.layout)
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


