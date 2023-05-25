import PySimpleGUI as sg
import queue as Queue
import SerialThread

available_ports = ["COM3", "COM4", "COM5"]

sg.LOOK_AND_FEEL_TABLE['PressOnTheme'] = {'BACKGROUND': '#DAE0E6',
                                        'TEXT': '#0A002B',
                                        'INPUT': '#C8D6E4',
                                        'TEXT_INPUT': '#000000',
                                        'SCROLL': '#99CC99',
                                        'BUTTON': ('#FDF9F9', '#675E84'),
                                        'PROGRESS': ('#D1826B', '#CC8019'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0,
                                        'PROGRESS_DEPTH': 0, }
  
sg.theme('PressOnTheme')

button_size = (12,2)
text_font = 'Franklin 18'
debugging = False

layout = [[sg.Text("Welcome, Annie", font = text_font, size = (80,1)), sg.Button('Debugging', key = '-Debugging-'), sg.Button('Stop Thread', key = '-Test-'), sg.Listbox(list(available_ports), enable_events=True, size=(20,4), key='-COMSList-')],
          [sg.Text("Selected COM: ", font = text_font, size = (80,1), key = "-COM-")],
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


def change_com(new_com):
    print("Changing COM with: ", new_com)

def run_app():
    print("Started running app")

    ToggleVisibility()
    global running
    global debugging
    global serial_thread
    
    coms_listbox = window['-COMSList-']
    com_text = window["-COM-"]

    while running:
        event, values = window.read()

        if event == "-COMSList-":
            selection = values[event]
            if selection:
                item = selection[0] # The written name
                index = coms_listbox.get_indexes()[0] # The index of the line
                com_text.update(f'Selected COM: {item}')
                change_com(item)

        if event == "-Test-":
            serial_thread.stop_serial_thread()

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