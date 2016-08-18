"""
[arduinoserial.py]
Autor: Sebastian Borquez G - COR2016
Fecha: 08/2016
Descripcion:  Comunicacion entre python y arduino a travez de serial
    
"""

import serial
import time
import os

TEST = True


class Arduino:
    """Representa a una placa arduino.

    Se encarga de conectar y tomar datos de este por serial.

    """

    def __init__(self, port):
        self.arduinoPort = None
        self.conectado = self.conectar(port)

    def conectar(self, port):
        """Prueba conectarse a una placa."""
        
        if TEST:
            self.arduinoPort = open("test.txt","r")
            return True
        # END TEST

        # Diferenciacion entre sistemas windows y linux
        COM = {"nt": "COM",
               "posix": "/dev/ttyUSB"}

        # Prueba conectarse con cualquera de los puertos
        for num in xrange(10):
            try:
                self.arduinoPort = serial.Serial(COM[os.name]+str(num),
                                                 port, timeout=1)
                time.sleep(1.8)
                print COM[os.name] + str(num), "- OK."
                return True
            except:
                pass
        print "Arduino no conectado."
        return False

    def getdata(self):
        """Lee los datos mandados por serial."""
        if self.conectado:
            return self.arduinoPort.readline().strip()
        return "No conectado"

    def kill(self):
        """Termina la conexion por serial."""
        if self.conectado:
            self.conectado = False
            self.arduinoPort.close()
