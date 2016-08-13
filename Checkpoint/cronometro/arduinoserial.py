import serial
import time
import os


class Arduino():

    def __init__(self, port):
        self.conectado = self.conectar(port)

    def conectar(self, port):
        COM = {"nt": "COM",
               "posix": "/dev/ttyACM"}
        for num in xrange(10):
            try:
                self.arduinoPort = serial.Serial(COM[os.name]+str(num),
                                                 port, timeout=1)
                time.sleep(1.8)
                return True
            except:
                print COM[os.name] + str(num), "no encontrado."
        return False

    def gettime(self):
        if self.conectado:
            return self.arduinoPort.readline()
        return "No conectado"

    def close(self):
        if self.conectado:
            self.arduinoPort.close()

#nuevo = Arduino(9600)
