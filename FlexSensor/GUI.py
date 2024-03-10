from dotenv import load_dotenv
import os
load_dotenv()
guiKey = os.getenv("GUIKey")
print("GUI Key:", guiKey)
# PySimpleGUI_License = guiKey
# PySimpleGUI_License = "eFyvJcM2ajW0NJldb1nQNsl1VtH5lfwMZlS3IN62INkdRllsdvmXVEs9bc3GBdltcZiIIZsZIakExOp6Yi2KVguYcS2RVqJdRbCtIV6XMzTjc7wgO0DQQu4RObTVAqwHMwiIwRisThGzlxjXZjWd55zJZuU6RmlQc9GWxsvUeTW71BlAbInpRvW5ZCX5JfzZaTW99RugIujEoVxuLoChJMOgYoWk1GlfREmJlPyBc83yQ8ibOQiCJTBSbhm6E5iJLSCsJJOiYrWp1klTTPGNF9z1drC5Ix6BIlk6Jlv2b9mYF62EakWhRxllcoyLBoBMZj3HVop3bYGHFPyVInirwBiBQN2A9mtlc1GeFqu5eUSuIp6AICinIasBIrkbNe1ic43dRRv3bTWwVuyySVU8QwiEObizIDz4Nbz7IUxhIZiRwlinR6GNFl0RZdUCl7zYc03uVplFZ7CrI16EIKjBAZy5LTzsIYxdLvzWIGwCMxjXQviWLwCkJ4EVY8XPRolxRiXOh8wDauXpJcl8cyyxIn6kIUjdA9yqLEz6IjxoLuzmIKw9MCjqUaiOLBCKJGFSbyWWFBpCbWEsFGkPZlHfJKlncf3nMwi8OaiMJ5hibZmd5kp6ZtWbJJvDbymHFM2iQqGT9b1Id3GIxLvtbG2PsAuoYW2d9VtgIWizwGixSPVYBABvZoGqRKy3ZFXwNVz5IrjZo4inM0TZgY3kLjj3EN4LO9SQ4pxYNuzgE4unMBzRUkiPfbQ6=n=Q12de9cb99fcfe37fe93f2a1a4b81eaf3b0d816d914cd0d105a24e09ff6261091e15bc65c55528b9beb2718cff424f529cb1e71afd0a177877bc596365f034af76a74bbc8e3aaac7fed09e578b373407cba87794428d1786606644b9e4aa95c24a1e98dd8a50e5a4176249e702f568b9a46e310e058c61a43ab40ccf5501ad3fe80f315ae9940d3155503ad930a1ec06895ea01327b8dc8621a5b98a8ef6bbb1bfdf5bf4fa4009db98e9775f366905bba11030beaca46d0c778764de26e55ad65d7b88266f72d42e533747786e7e362c0e16e49426f97348ed41a806290772dd7e0ee798bac40c669d4e7001c0835d3a8328fca06402cc2b56ae57e43969d865942e10433a05fe4104d8ab76795d97e9c1e3e21ad32f271caffc5477bb78fa8d2e6576b413e5e65c6ac310cc43a34f33f74898a2612bd09d746bffc4b9256ea3635ad618bf633de90d32cf2f531eb8f2c00cf97e325c471989f2d161f7d54d10c1acc17b8299eb4906e9f5cb2a8ec979b44337649b656b7dd4c14f04a12bde9f1f34d5d73d79208504dfec4cc3cc9340d5b400a0716b98c0ab3f720096acc5e9a0d32f1b9dc5489e28ef375eafbbc6e576a392c908aa36ad3b61bf005bab6b1d01d166480341b13f5d51499749c33ac1c6fef5491b610fb6845f477c47e20f03520b65daf65934c7aebccf1199957f8239a66a8b98cac322348c61f535d710736"

import PySimpleGUI as sg
import queue as Queue
import SerialThread
import FlexSignal as fs

available_ports = ["COM3", "COM4", "COM5"] # TODO: Change this to the actual available ports

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
    global window
    success = fs.start_connection(new_com)
    if success:
        print("The change was successful")
        window["-COM-"].update(f"Selected COM: {new_com}")
        serial_thread.resume()
    else:
        window["-COM-"].update(f"Invalid selected COM: {new_com}")
        serial_thread.pause()
        print("Change was unsuccessfull")

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
            print("This is a test")

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