import time
import serial
 
PORT = 9600
COM = '/dev/ttyACM1'


# Iniciando conexión serial
arduinoPort = serial.Serial(COM, PORT, timeout=1)
 
# Retardo para establecer la conexión serial
time.sleep(1.8) 
getSerialValue = arduinoPort.readline()
#getSerialValue = arduinoPort.read()
#getSerialValue = arduinoPort.read(6)
print '\nValor retornado de Arduino: %s' % (getSerialValue)
 
# Cerrando puerto serial
arduinoPort.close()