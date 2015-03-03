import serial #comunicacion serial
import threading #hilos y locks
import time #para obtener sleep
from c_helper import char_parse_int

lock = threading.Lock()
dato = ''
valor = ''
info = None
leyendo = 0

class X(threading.Thread):
    '''hilo para la lectura de datos'''
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global leyendo
        while leyendo:
            lock.acquire()
            global dato
            global valor
            global info
            dato = cereal.read()
            valor += char_parse_int(dato)
            if len(valor) == 3:
                info = valor
                valor = ''
            lock.release()
            
x = X() #creacion del hilo
def init():
    global x
    global cereal
    cereal = serial.Serial(3)
    x.start() #ejecucion del hilo
    
def close():
    lock.acquire()
    global leyendo
    leyendo = 0
    lock.release()
    global x
    x.join()

if __name__ == '__main__':
    init()
    print valor
    time.sleep(1)
    close()