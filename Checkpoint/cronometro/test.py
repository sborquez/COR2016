from arduinoserial import *

cronometro = Arduino(57600)
  
while True:
    print cronometro.getdata()
