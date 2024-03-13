import serial
import os
import threading
serialPort = None
baud = 9600

# for signal analysis, not UI
min_signal = 23
max_signal = 1023
data_samples = 40
is_running = False
file_name = "Test"
current_file = 0

def set_serial_port(port):
    global serialPort 
    serialPort = port
    print(serialPort)

def get_serial_port():
    return serialPort

def get_baud():
    return baud


# This serial needs to be started with a default COM, which is COM3
# If it has nothing, it should handle the error

serialSignal = None

def startConnection(comName):
    global serialPort
    global serialSignal

    serialPort = comName
    try:
        serialSignal = serial.Serial(comName, baud)
        try:
            print("Waiting for data...")
            data = getSignalData()
            if data == None:
                print("COM tried to get data, but No data received.")
                return False
            print("Connection started on COM: ", serialPort)
            return True
        except:
            print("Error getting data.")
            return False
    except:
        print("Connection failed, no connection with COM", serialPort, ".")
        return False
    
def endConnection():
    saveData()
    print("Ended connection")
    serialSignal.close()

def getSignalData():
    def readSerial():
        nonlocal data
        rawData = str(serialSignal.readline())
        data = rawData[2:][:-5]

    data = None
    thread = threading.Thread(target=readSerial)
    thread.start()
    thread.join(timeout=5)

    if thread.is_alive():
        return None

    return data

def printFileName():
    print(file_name)

def saveData():
    file = open(file_name, "a")
    file.write(file_name)

