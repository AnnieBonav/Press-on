import serial
import os

#arduino_port = "/dev/cu.usbmodem141301"
arduino_port = "COM4"

baud = 9600
fileName = "analog-data6.csv"
samples = 100
print_labels = False


ser = serial.Serial(arduino_port, baud)
print("Connected to arduino port: " + arduino_port)
file = open(fileName, "a")
print("Created file")

line = 0

def printStuff():
  while line <= samples:
    if print_labels:
      if line == 0:
        print("Printing column headers")
      else:
        print("Line: " + str(line) + ": writing...")
    getData = str(ser.readline())
    data = getData[2:][:-5]
    print(data)

    file = open(fileName, "a")
    file.write(data + "\n")
    line = line +1

def MinMaxSignal():
  minSignal = 400
  maxSignal = 600
  fileName = "minMax.csv"

  if os.path.exists(fileName):
    os.remove(fileName)

  minMaxSamples = 100
  minMaxLine = 0

  while minMaxLine < minMaxSamples:
    data = str(ser.readline())
    signal = data[2:][:-5]
    signal = signal.split(',')[0]
    print(signal)

    file = open(fileName, "a")
    file.write(signal + "\n")
    minMaxLine = minMaxLine + 1

    signal = int(signal)
    if signal > maxSignal:
      maxSignal = signal
    
    if signal < minSignal:
      minSignal = signal
  
  file.write("Min signal: " + str(minSignal) + "\nMax signal: " + str(maxSignal))
  return 0


  
def Main():
  MinMaxSignal()
  print("Data colletion complete!")
  return 0

Main()


