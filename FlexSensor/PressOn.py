import PySimpleGUI as sg
import SignalClass
import time
import threading as Thread
import queue as Queue
import serial



#flexSignal = SignalClass.FlexSignal("Annie.csv")
#flexSignal.PrintFileName()
#flexSignal.GetSignalData()


def getData():
    ser = serial.Serial('COM3',9600)
    getData = str(ser.readline())
    data = getData[2:][:-5]
    print(data)




running = True

class App():
    def __init__(self):
        self.layout = [  [sg.Text("Welcome, Annie")],
            [sg.Text("This is the signal", key = '-RawSignal-')],
            [sg.Button('Get Signal', key = '-StartSignal-'), sg.Button('Stop', key = '-StopSignal-')] ]
        self.window = sg.Window('Window Title', self.layout)
        self.running = True
        self.RunApp()
        

    def RunApp(self):
        while self.running:
            print("running")
            event, values = self.window.read()

            if event == '-StartSignal-':
                self.window['-RawSignal-'].update(4)
                #t = Thread(target = getData)
                #t.start()


            if event == '-StopSignal-':
                self.window['-RawSignal-'].update(0)
                #flexSignal.isRunning = False
                print("I am stopping")
                #window['-RawSignal-'].update(0)

            if event == sg.WIN_CLOSED:
                self.running = False
                self.window.close()

app = App()

