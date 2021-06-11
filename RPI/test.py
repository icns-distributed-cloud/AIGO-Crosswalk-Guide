import serial
ser = serial.Serial('/dev/ttyAMA0',115200)
if(ser.isOpen()):
	print("open")

#key = '1' # stop
#key = '2' # forward
#key = '3' # detect start
#key = '4' # detect green light

key = str(input())
ser.write(serial.to_bytes([int(key, 16)]))

ser.close()
