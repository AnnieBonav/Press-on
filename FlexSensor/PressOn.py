import PySimpleGUI as sg
import SignalClass
import time
from multiprocessing import Process

layout = [  [sg.Text("Welcome, Annie")],
            [sg.Text("This is the signal", key = '-RawSignal-')],
            [sg.Button('Get Signal', key = '-StartSignal-'), sg.Button('Stop', key = '-StopSignal-')] ]

window = sg.Window('Window Title', layout)

flexSignal = SignalClass.FlexSignal("Annie.csv")
flexSignal.PrintFileName()
flexSignal.GetSignalData()

def myName(name):
    running = True
    while running:
        event, values = window.read()

        if event == '-StartSignal-':
            window['-RawSignal-'].update(4)
            #flexSignal.isRunning = True
            
            
            #while flexSignal.isRunning:
                #flexSignal.GetSignalData()
                #time.sleep(100)
                #window['-RawSignal-'].update(data)


        if event == '-StopSignal-':
            window['-RawSignal-'].update(0)
            #flexSignal.isRunning = False
            print("I am stopping")
            #window['-RawSignal-'].update(0)

        if event == sg.WIN_CLOSED:
            running = False
            window.close()

if __name__ == '__main__':
    p = Process(target = myName, args = ('Annie',))
    p.start()

print("end")