serial_port = "COM3"
baud = 9600

def set_serial_port(port):
    global serial_port 
    serial_port = port
    print(serial_port)

def get_serial_port():
    return serial_port

def get_baud():
    return baud