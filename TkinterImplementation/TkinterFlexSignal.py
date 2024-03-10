import serial
import os
serial_port = None
baud = 9600

# for signal analysis, not UI
min_signal = 23
max_signal = 1023
data_samples = 40
is_running = False
file_name = "Test"
current_file = 0

def set_serial_port(port):
    global serial_port 
    serial_port = port
    print(serial_port)

def get_serial_port():
    return serial_port

def get_baud():
    return baud


# This serial needs to be started with a default COM, which is COM3
# If it has nothing, it should handle the error

serial_signal = None

def start_connection(com_name):
    global serial_port
    global serial_signal

    serial_port = com_name
    try:
        serial_signal = serial.Serial(com_name, baud)
        print("Connection started on COM: ", serial_port)
        return True
    except:
        print("Connection failed, no connection with COM", serial_port, ".")
        return False
    
def end_connection():
    save_data()
    print("Ended connection")

def get_signal_data():
    #while self.isRuning: # I create an implicit listener: whenever I change this value oustide, the function will stop running
    get_data = str(serial_signal.readline())
    data = get_data[2:][:-5]
    return data

def print_file_name():
    print(file_name)

def save_data():
    file = open(file_name, "a")
    file.write(file_name)

