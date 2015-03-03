import pygame
import sys
from pygame.locals import *

AQUA = (0,130,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
key_down = False  #indica si alguna tecla ha sido presionada (independientemente si alguna esta previamente presionada)
key_up = True #indica si alguna tecla ha sido levantada (independientemente si alguna esta previamente presionada)
key_unpress = True #indica si no hay alguna tecla presionada
active_keys = [] #indica que teclas estan siendo presionadas
last_keys = [] #historial de las ultimas teclas presionadas
last_key = -1 #ultima tecla presionada
available_buttons = (K_UP, K_DOWN, K_RIGHT, K_LEFT, K_a)
#############################################################################
## funciones basicas
def iniciarPygame(size = (500, 400), opt1 = 0, colorDepth = 32, titulo = 'sin titulo'):
    '''inicia pygame y regresa un espacio de trabajo generalmente llamado canvas
size: tipo tuple(x,y). Tamano de la pantalla
opt1: tipo int. funcion desconocida (dejar en cero)
colorDepth: tipo int. colores con los que puede trabajar
titulo: tipo str. titulo de la ventana
'''
    pygame.init()
    canvas = pygame.display.set_mode(size, opt1, colorDepth)
    pygame.display.set_caption(titulo)
    return canvas

def salirPygame():
    '''sale del juego'''
    pygame.quit()
    sys.exit(0)
    
def cacha_teclas():
    global key_down, key_up, key_unpress, active_keys, last_keys, last_key, available_buttons
    for event in pygame.event.get(): #va de cajon
        if event.type == QUIT:
            salirPygame()
        if event.type == KEYUP:
            key_down = False
            key_up = True
            aux = pygame.key.get_pressed()
            still = [i for i in available_buttons if aux[i] == 1]
            for c in active_keys:
                if not c in still:
                    del(active_keys[active_keys.index(c)])
            if not 1 in aux:
                key_unpress = True
        if event.type == KEYDOWN:
            aux = pygame.key.get_pressed()
            active_keys = [i for i in available_buttons if aux[i] == 1]
            if aux[event.key] and event.key in available_buttons:
                key_down = True
                key_up = False
                key_unpress = False
                last_keys.append(event.key)
                last_key = event.key
                if len(last_keys) > 10:
                    del(last_keys[0])