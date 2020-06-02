# Serial Test
import serial

port = serial.Serial("COM13", 115200)
port.write(str.encode('bdb role'))
port.read(2)
print()
port.reset_input_buffer()
port.reset_output_buffer()
port.close()