import serial #comunicacion serial
import threading #hilos y locks
import time #para obtener sleep
from os import system as o_system # para ejecutar programas de consola nativos
from c_helper import char_parse_int

lock = threading.Lock()
valor = -1

class X(threading.Thread):
    '''hilo para la deteccion de un enter'''
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        if not raw_input():
            lock.acquire()
            global s
            s = True
            lock.release()

def main():
    o_system('cls')
    raw_input('la coneccion con el puerto serial (COM4) se iniciara con enter')
    x = X() #creacion del hilo
    x.start() #ejecucion del hilo
    global s
    s = False #variable de control (salida del programa)
    cereal = serial.Serial(3)
    while not s:
        o_system('cls')
        dato = cereal.read() #recepcion de dato (tipo char en c -- o str en python)
        global valor
        valor = char_parse_int(dato)
        print 'dato leido', valor
        print 'presione enter para terminar la comunicacion serial'
    cereal.close()
    x.join()

if __name__ == '__main__':
    main()
