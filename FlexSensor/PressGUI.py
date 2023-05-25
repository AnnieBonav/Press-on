import PySimpleGUI as sg
import FlexSignal as fs
import queue as Queue
import threading
import time

class SerialThread(threading.Thread, sg.Window, sg.Graph):
    def __init__(self, queue, window, graph):
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

        
    def update_min_max(self, min, max):
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


button_size = (12,2)
text_font = 'Franklin 18'
debugging = False

layout = [[sg.Text("Welcome, Annie", font = text_font, size = (80,1)), sg.Button('Debugging', key = '-Debugging-')],
        [sg.Graph(
            canvas_size=(200, 200),
            graph_bottom_left=(0, 0),
            graph_top_right=(200, 200),
            key="graph"
        )],
            [sg.Text("Analogue signal: ", key = '-RawSignalTxt-', font = text_font),sg.Text("", key = '-RawSignal-', font = text_font)],
            [sg.Text("Normalized Signal: ", key = '-NormalizedSignalTxt-', font = text_font), sg.Text("", key = '-NormalizedSignal-', font = text_font)],
            [sg.Text("RGB: ", key = '-RGBTxt-',  font = text_font), sg.Text("", key = '-RGB-', font = text_font)],
            [sg.Text("Hex", key = '-HexTxt-', font = text_font), sg.Text("This is the signal", key = '-Hex-', font = text_font)],
            [sg.Text("Min: ", key = '-MinTxt-', font = text_font), sg.Text("", key = '-CurrentMin-', font = text_font), 
            sg.InputText(key = '-MinInput-', font = text_font, size = (5,1)), sg.Text("Max: ", key = '-MaxTxt-', font = text_font), 
            sg.Text("", key = '-CurrentMax-', font = text_font), sg.InputText(key = '-MaxInput-', font = text_font, size = (5,1)), 
            sg.Button('Update Min-Max', key = '-UpdateMinMax-', size = button_size)]]

window = sg.Window('Press-on', layout)
window.Finalize()
graph = window.Element("graph")
graph.DrawCircle((100, 100), 100,fill_color="#FFFFFF")
running = True
serial_queue = Queue.Queue()

serial_thread = SerialThread(serial_queue, window, graph)
serial_thread.start()

def ToggleVisibility():
    window.Element('-RawSignalTxt-').Update(visible = debugging)
    window.Element('-RawSignal-').Update(visible = debugging)
    
    window.Element('-NormalizedSignalTxt-').Update(visible = debugging)
    window.Element('-NormalizedSignal-').Update(visible = debugging)
    
    window.Element('-RGBTxt-').Update(visible = debugging)
    window.Element('-RGB-').Update(visible = debugging)
    
    window.Element('-HexTxt-').Update(visible = debugging)
    window.Element('-Hex-').Update(visible = debugging)

    window.Element('-MinTxt-').Update(visible = debugging)
    window.Element('-CurrentMin-').Update(visible = debugging)
    window.Element('-MinInput-').Update(visible = debugging)

    window.Element('-MaxTxt-').Update(visible = debugging)
    window.Element('-CurrentMax-').Update(visible = debugging)
    window.Element('-MaxInput-').Update(visible = debugging)

    window.Element('-UpdateMinMax-').Update(visible = debugging)

def run_app():
    print("Started running app")

    ToggleVisibility()
    global running
    global debugging
    
    while running:
        print("running")
        event, values = window.read()

        if event == '-Debugging-':
            debugging = not debugging
            ToggleVisibility()

        if event == '-UpdateMinMax-':
            min = values['-MinInput-']
            max = values['-MaxInput-']

            serial_thread.update_min_max(int(min), int(max))

        if event == sg.WIN_CLOSED:
            running = False
            serial_thread.isRunning = False
            window.close()