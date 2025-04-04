import serial
import time

# Open grbl serial port
s = serial.Serial('/dev/tty.usbserial-10',115200)

fileName = 'recenter.gcode'
# Open g-code file
f = open('Files/'+fileName,'r');

# Wake up grbl
s.write(b"\r\n\r\n")  # Prefix the string with 'b' for bytes
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl
for line in f:
    l = line.strip() # Strip all EOL characters for consistency
    print('Sending: ' + l)
    s.write((l + '\n').encode())  # Encode G-code lines as bytes
    grbl_out = s.readline().decode().strip()
    print(' : ' + grbl_out.strip())

# Close file and serial port
f.close()
s.close()