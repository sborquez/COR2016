import time
import serial
from cronometro.arduinoserial import Arduino
 
cronometro = Arduino(9600)
cronometro.gettime()