import PySimpleGUI as sg
import queue as Queue
import SerialThread

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

serial_thread = SerialThread.SerialThread(serial_queue, window, graph)
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