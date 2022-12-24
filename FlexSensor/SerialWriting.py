import serial

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
while line <= samples:
  if print_labels:
    if line == 0:
      print("Printing column headers")
    else:
      print("Line: " + str(line) + ": writing...")
  getData = str(ser.readline())
  data = getData[2:][:-5]
  #data = getData
  print(data)

  file = open(fileName, "a")
  file.write(data + "\n")
  line = line +1

print("Data colletion complete!")

