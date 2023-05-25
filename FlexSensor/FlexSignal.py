import serial
import os
import SerialConnection as sc

file_name = "TestData.txt"
print(sc.get_serial_port())

min_signal = 23
max_signal = 1023
data_samples = 40
is_running = False

ser = serial.Serial(sc.get_serial_port(), sc.get_baud())

def start_connection():
    print("Connection started")

def get_signal_data():
    #while self.isRuning: # I create an implicit listener: whenever I change this value oustide, the function will stop running
    get_data = str(ser.readline())
    data = get_data[2:][:-5]
    return data

def rrite_to_file():
    data = 0 #Data should be equal to something gotten from the port
    file = open(file_name, "a")
    file.write(data + "\n")

def print_file_name():
    print(file_name)