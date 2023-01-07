import PySimpleGUI as sg
import SignalClass
import time
import threading
import queue as Queue
import serial

#flexSignal.GetSignalData()


def getData():
    ser = serial.Serial('COM3',9600)
    getData = str(ser.readline())
    data = getData[2:][:-5]
    print(data)

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.isRunning = True
        #flexSignal = SignalClass.FlexSignal("Annie.csv")
        #flexSignal.PrintFileName()
    
    def run(self):
        print("Entered run:")
        ser = serial.Serial('COM4',9600)
        time.sleep(0.5)
        while self.isRunning:
            if ser.inWaiting():
                data = str(ser.readline(ser.inWaiting()))
                data = data[2:][:-5]
                self.queue.put(data)
                #print("Inside while: ", data)
        

class App():
    def __init__(self):
        self.layout = [  [sg.Text("Welcome, Annie")],
            [sg.Text("This is the signal", key = '-RawSignal-')],
            [sg.Button('Get Signal', key = '-StartSignal-'), sg.Button('Stop', key = '-StopSignal-')] ]
        self.window = sg.Window('Window Title', self.layout)
        self.running = True

        self.queue = Queue.Queue()
        self.thread = SerialThread(self.queue)
        self.thread.start()

        self.RunApp()

    def process_serial(self):
        value=True
        print(self.queue.qsize())
        
    def RunApp(self):
        while self.running:
            self.process_serial()
            event, values = self.window.read()


            if event == '-StartSignal-':
                self.window['-RawSignal-'].update(4)
                self.queue.get()


            if event == '-StopSignal-':
                self.window['-RawSignal-'].update(0)
                #flexSignal.isRunning = False
                print("I am stopping")
                #window['-RawSignal-'].update(0)

            if event == sg.WIN_CLOSED:
                self.running = False
                self.thread.isRunning = False
                self.window.close()

app = App()

