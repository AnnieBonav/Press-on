import PySimpleGUI as sg
import SignalClass
import time
import threading
import queue as Queue
import serial
import tkinter as tk




#flexSignal = SignalClass.FlexSignal("Annie.csv")
#flexSignal.PrintFileName()
#flexSignal.GetSignalData()

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        ser = serial.Serial('COM3',9600)
        getData = str(ser.readline())
        data = getData[2:][:-5]
        print(data)
        time.sleep(0.2)
        while True:
            if ser.inWaiting():
                text = ser.readline(ser.inWaiting())
                self.queue.put(text)

class App(tk.Tk):
    def __init__(self):
        self.layout = [  [sg.Text("Welcome, Annie")],
            [sg.Text("This is the signal", key = '-RawSignal-')],
            [sg.Button('Get Signal', key = '-StartSignal-'), sg.Button('Stop', key = '-StopSignal-')] ]

        self.window = sg.Window('Window Title', self.layout)



        tk.Tk.__init__(self)
        self.geometry("1000x750")
        frameLabel = tk.Frame(self, padx=40, pady =40)
        self.text = tk.Text(frameLabel, wrap='word', font='TimesNewRoman 37',
                            bg=self.cget('bg'), relief='flat')
        frameLabel.pack()
        self.text.pack()
        self.queue = Queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    def process_serial(self):
        value=True
        while self.queue.qsize():
            try:
                new=self.queue.get()
                if value:
                    self.text.delete(1.0, 'end')
                    value=False
                    self.text.insert('end',new)
            except Queue.Empty:
                pass
        self.after(100, self.process_serial)

app = App()
app.mainloop()

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

#if __name__ == '__main__':
    #p = Process(target = myName, args = ('Annie',))
    #p.start()

app = App()
app.mainloop()