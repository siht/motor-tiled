from os import curdir, pardir
from os.path import join as o_p_join
import Base.Basics as bB
from Base.Basics import *
from Base.Logics import *
from Base.Dibujar_Sprites import *

def main():
    i = 0
    reloj = pygame.time.Clock()
    escenario = Escenario(size =(2000, 600))
    # limites de escena
    escenario.obstaculos.append(ImgInPyG(localizacion =(-1,-1),tamano=(2001,1)))
    escenario.obstaculos.append(ImgInPyG(localizacion =(-1,-1),tamano=(1,601)))
    escenario.obstaculos.append(ImgInPyG(localizacion =(2000,-1),tamano=(1,601)))
    escenario.obstaculos.append(ImgInPyG(localizacion =(600,-1),tamano=(2001,1)))
    # lugares para colision y actualizar mapa
    escenario.utileria.append(ImgInPyG(localizacion = (200,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (400,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (600,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (800,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (1000,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (1200,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (1400,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (1600,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (1800,0), tamano = (1, 600)))
    escenario.utileria.append(ImgInPyG(localizacion = (2000,0), tamano = (1, 600)))
    #agregar obstaculos
    canvas = iniciarPygame((800, 600), titulo='Carrera en Barco')
    # back de holas
    for i in range(10):
        escenario.background.append(ImgInPyG(o_p_join(curdir, 'data/img', 'hola1.png'), localizacion = (i * 100,0), trans = 1, zoom=(.2,.2)))
    for i in range(10):
        escenario.background.append(ImgInPyG(o_p_join(curdir, 'data/img', 'hola2.png'), localizacion = (i * 100,100), trans = 1, zoom=(.2, .2)))
    for i in range(10):
        escenario.background.append(ImgInPyG(o_p_join(curdir, 'data/img', 'hola1.png'), localizacion = (i * 100,200), trans = 1, zoom=(.2, .2)))
    for i in range(10):
        escenario.background.append(ImgInPyG(o_p_join(curdir, 'data/img', 'hola2.png'), localizacion = (i * 100,300), trans = 1, zoom=(.2, .2)))
    for i in range(10):
        escenario.background.append(ImgInPyG(o_p_join(curdir, 'data/img', 'hola1.png'), localizacion = (i * 100,400), trans = 1, zoom=(.2, .2)))
    for i in range(10):
        escenario.background.append(ImgInPyG(o_p_join(curdir, 'data/img', 'hola2.png'), localizacion = (i * 100,500), trans = 1, zoom=(.2, .2)))
    # obstaculos matan al personaje
    escenario.obstaculos.append(ImgInPyG(o_p_join(curdir, 'data/img', 'ajthrud.png'), localizacion = (700,400), zoom = (.2,.2), trans = 1))
    escenario.obstaculos.append(ImgInPyG(o_p_join(curdir, 'data/img', 'ajthrud.png'), localizacion = (680,500), zoom = (.2,.2), trans = 1))
    escenario.obstaculos.append(ImgInPyG(o_p_join(curdir, 'data/img', 'ajthrud.png'), localizacion = (320,33), zoom = (.2,.2), trans = 1))
    escenario.obstaculos.append(ImgInPyG(o_p_join(curdir, 'data/img', 'ajthrud.png'), localizacion = (450,20), zoom = (.2,.2), trans = 1))
    camara = Camara(canvas = canvas)
    barco = ImgInPyG(o_p_join(curdir, 'data/img', 'barco - copia.png'), trans = 1, zoom = (2,2))
    escenario.personajes.append(barco)
    while True:
        cacha_teclas()
        # capturar teclas activas y demas cosas
        lo = escenario.personajes[0].localizacion
        if not bB.key_unpress:
            for code in bB.active_keys:
                # lo = escenario.personajes.localizacion
                if code == K_RIGHT:
                    escenario.personajes.localizacion = lo[0] + 5, lo[1]
                if code == K_LEFT:
                    escenario.personajes.localizacion = lo[0] - 5, lo[1]
                if code == K_DOWN:
                    escenario.personajes.localizacion = lo[0], lo[1] + 5
                if code == K_UP:
                    escenario.personajes.localizacion = lo[0], lo[1] - 5
        # agregar movimientos del personaje (coordenadas) y npc si los hay
        # agregar codigo de colisiones aqui
        # agregar update de la camara con el objeto principal en esta linea
        canvas.fill(AQUA) #para limpiar pantalla antes de redibujar
        for b in escenario.background:
            cargarImgInPyG2(canvas, b, camara)
        for o in escenario.obstaculos:
            if o.surface:
                cargarImgInPyG2(canvas, o, camara)
        for e in escenario.enemigos:
            cargarImgInPyG2(canvas, e, camara)
        for i in escenario.items:
            cargarImgInPyG2(canvas, i, camara)
        for u in escenario.usableItems:
            cargarImgInPyG2(canvas, u, camara)
        for u in escenario.utileria:
            if u.surface:
                cargarImgInPyG2(canvas, u, camara)
        pygame.display.update() #redibujar
        reloj.tick(40)
    
if __name__ == '__main__':
    main()