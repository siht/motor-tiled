from os import curdir, pardir
from os.path import join as o_p_join
import Base.Basics as bB # para llamar a las variables
from Base.Basics import *
from Base.Logics import *
from Base.Dibujar_Sprites import *
import comepapas #juego de prueba

juego1 = False
    
def main():
    global juego1
    i = 0
    reloj = pygame.time.Clock()
    escenario = Escenario(size =(900, 600))
    escenario.obstaculos.append(ImgInPyG(localizacion = (-1, 95),tamano = (901, 1)))
    escenario.obstaculos.append(ImgInPyG(localizacion = (95, -1),tamano = (1, 601)))
    escenario.obstaculos.append(ImgInPyG(localizacion = (900 - 95,-1),tamano = (1, 601)))
    escenario.obstaculos.append(ImgInPyG(localizacion = (-1, 601 - 95),tamano = (901, 1)))
    canvas = iniciarPygame((800, 600), titulo='HUELLAS CON HISTORIA')
    wf = ImgInPyG(o_p_join(curdir, 'data/img', 'alejandrafrente.png'), trans = 1)
    wb = ImgInPyG(o_p_join(curdir, 'data/img', 'alejandratras.png'), trans = 1)
    wr = ImgInPyG(o_p_join(curdir, 'data/img', 'alejandraizq.png'), trans = 1)
    wl = ImgInPyG(o_p_join(curdir, 'data/img', 'alejandrader.png'), trans = 1)
    st = ImgInPyG(o_p_join(curdir, 'data/img', 'a_w_stand.png'), trans = 1)
    awf = ImageArray(wf,(1,3))
    awb = ImageArray(wb,(1,3))
    awr = ImageArray(wr,(1,3))
    awl = ImageArray(wl,(1,3))
    ast = ImageArray(st)
    print awl.setGlobalZoom()
    alejandra = Personaje(ast, awf, awb, awr, awl)
    fondo = ImgInPyG(o_p_join(curdir, 'data/img', 'HALL1.png'))
    escenario.personajes = alejandra
    escenario.background.append(fondo)
    im = ImgInPyG(localizacion = (340, 95), tamano = (80, 20))
    print im.defaultRect
    escenario.utileria.append(im)
    esc2 = ImgInPyG(o_p_join(curdir, 'data/img', 'todo (2).png'), localizacion = (400,400))
    del(wf,wb,wr,wl,st)
    del(awf,awb,awr,awl,ast)
    del(alejandra)
    del(fondo)
    del(im)
    escenario.personajes.localizacion = (100,200)
    camara = Camara(canvas = canvas)
    pygame.mixer.music.load(o_p_join(curdir, 'data/sound' ,'gooback.wav'))
    pygame.mixer.music.play(-1, 0.0)
    while True:
        cacha_teclas()
        # movimientos del personaje (coordenadas)
        lo = escenario.personajes.localizacion
        # global lo
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
        #agregar codigo de colisiones aqui
        # print escenario.personajes.getPyGRect()
        if escenario.personajes.getPyGRect().colliderect(escenario.utileria[0].defaultRect):
            juego1 = True
        for o in escenario.obstaculos:
            if escenario.personajes.getPyGRect().colliderect(o.defaultRect):
                escenario.personajes.localizacion = lo
        #terminar el codigo de colisiones aqui
        camara.update(escenario.personajes, escenario) #necesario aqui
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
        # movimientos del personaje (sprites)
        if i == 0:
            if not bB.key_unpress and bB.last_key == K_RIGHT:
                x = escenario.personajes[3].currentImgInPyG
                y = escenario.personajes.localizacion
            if not bB.key_unpress and bB.last_key == K_LEFT:
                x = escenario.personajes[4].currentImgInPyG
                y = escenario.personajes.localizacion
            if not bB.key_unpress and bB.last_key == K_UP:
                x = escenario.personajes[2].currentImgInPyG
                y = escenario.personajes.localizacion
            if not bB.key_unpress and bB.last_key == K_DOWN:
                x = escenario.personajes[1].currentImgInPyG
                y = escenario.personajes.localizacion
            if bB.key_unpress:
                x = escenario.personajes[0].currentImgInPyG
                y = escenario.personajes.localizacion
        i += 1
        if i >= 3:
            i = 0
        z = (y[0] - camara.localizacion[0], y[1] - camara.localizacion[1])
        canvas.blit(x, z)
        pygame.display.update() #redibujar
        if juego1:
            comepapas.main()
        reloj.tick(40)
                    
if __name__ == '__main__':
    main()
