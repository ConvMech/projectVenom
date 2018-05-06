import serial

ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

while True:
	byte = ser.read();
	print(byte)
ser.close();
