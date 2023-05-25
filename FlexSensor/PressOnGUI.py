import PySimpleGUI as sg
import SignalClass
import time
import threading
import queue as Queue

import SerialConnection as sc

serial_port = None

print(sc.get_serial_port())
sc.set_serial_port("COM4")
print(sc.get_serial_port())

class SerialThread(threading.Thread, sg.Window, sg.Graph):
    def __init__(self, queue, window, graph):
        threading.Thread.__init__(self)
        self.queue = queue
        self.window = window
        self.graph = graph
        self.isRunning = True
        self.flexSignal = SignalClass.FlexSignal("Annie.csv")

        self.minNum = 250
        self.maxNum = 1023
        self.squareColor = '#FFFFFF'

        self.window['-CurrentMin-'].update(self.minNum)
        self.window['-MinInput-'].update(self.minNum)
        self.window['-CurrentMax-'].update(self.maxNum)
        self.window['-MaxInput-'].update(self.maxNum)

        
    def UpdateMinMax(self, min, max):
        self.minNum = min
        self.maxNum = max
        self.window['-CurrentMin-'].update(self.minNum)
        self.window['-CurrentMax-'].update(self.maxNum)

    def rgb_to_hex(self, r, g, b):
        return ('{:X}{:X}{:X}').format(r, g, b)

    def run(self):
        time.sleep(0.2)
        while self.isRunning:
            if self.flexSignal.ser.inWaiting():
                data = self.flexSignal.GetSignalData()
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
        

class App():
    def __init__(self):
        buttonSize = (12,2)
        textFont = 'Franklin 18'
        self.debugging = False
        self.layout = [[sg.Text("Welcome, Annie", font = textFont, size = (80,1)), sg.Button('Debugging', key = '-Debugging-')],
        [sg.Graph(
            canvas_size=(200, 200),
            graph_bottom_left=(0, 0),
            graph_top_right=(200, 200),
            key="graph"
        )],
            [sg.Text("Analogue signal: ", key = '-RawSignalTxt-', font = textFont),sg.Text("", key = '-RawSignal-', font = textFont)],
            [sg.Text("Normalized Signal: ", key = '-NormalizedSignalTxt-', font = textFont), sg.Text("", key = '-NormalizedSignal-', font = textFont)],
            [sg.Text("RGB: ", key = '-RGBTxt-',  font = textFont), sg.Text("", key = '-RGB-', font = textFont)],
            [sg.Text("Hex", key = '-HexTxt-', font = textFont), sg.Text("This is the signal", key = '-Hex-', font = textFont)],
            [sg.Text("Min: ", key = '-MinTxt-', font = textFont), sg.Text("", key = '-CurrentMin-', font = textFont), sg.InputText(key = '-MinInput-', font = textFont, size = (5,1)), sg.Text("Max: ", key = '-MaxTxt-', font = textFont), sg.Text("", key = '-CurrentMax-', font = textFont), sg.InputText(key = '-MaxInput-', font = textFont, size = (5,1)), sg.Button('Update Min-Max', key = '-UpdateMinMax-', size = buttonSize)]]
        
        self.window = sg.Window('Press-on', self.layout)
        self.window.Finalize()
        self.graph = self.window.Element("graph")
        self.graph.DrawCircle((100, 100), 100,fill_color="#FFFFFF")
        self.running = True

        self.queue = Queue.Queue()
        self.thread = SerialThread(self.queue, self.window, self.graph)
        self.thread.start()

        
        self.RunApp()

    def ToggleVisibility(self):
        self.window.Element('-RawSignalTxt-').Update(visible = self.debugging)
        self.window.Element('-RawSignal-').Update(visible = self.debugging)
        
        self.window.Element('-NormalizedSignalTxt-').Update(visible = self.debugging)
        self.window.Element('-NormalizedSignal-').Update(visible = self.debugging)
        
        self.window.Element('-RGBTxt-').Update(visible = self.debugging)
        self.window.Element('-RGB-').Update(visible = self.debugging)
        
        self.window.Element('-HexTxt-').Update(visible = self.debugging)
        self.window.Element('-Hex-').Update(visible = self.debugging)

        self.window.Element('-MinTxt-').Update(visible = self.debugging)
        self.window.Element('-CurrentMin-').Update(visible = self.debugging)
        self.window.Element('-MinInput-').Update(visible = self.debugging)

        self.window.Element('-MaxTxt-').Update(visible = self.debugging)
        self.window.Element('-CurrentMax-').Update(visible = self.debugging)
        self.window.Element('-MaxInput-').Update(visible = self.debugging)

        self.window.Element('-UpdateMinMax-').Update(visible = self.debugging)

    def RunApp(self):
        self.ToggleVisibility()

        while self.running:
            event, values = self.window.read()

            if event == '-Debugging-':
                self.debugging = not self.debugging
                self.ToggleVisibility()

            if event == '-UpdateMinMax-':
                min = values['-MinInput-']
                max = values['-MaxInput-']

                self.thread.UpdateMinMax(int(min), int(max))

            if event == sg.WIN_CLOSED:
                self.running = False
                self.thread.isRunning = False
                self.window.close()


PressOnApp = App()


