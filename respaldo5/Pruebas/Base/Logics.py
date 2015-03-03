## to do:
## mejorar las validaciones de como asignar nuevos elementos en ImageArray
## si hay tuplas iguales en ImageArray hay que eliminarlas o no admitirlas sin lanzar excepciones
## agregar mas documentacion

import pygame
from Patron import FlyWeight, Singleton
from os.path import exists as o_p_exists, abspath as o_p_abspath, join as o_p_join
from os import curdir, pardir

class Surface(object): #de ayuda al programa (gasta menos memoria y tiempo de creacion)
    __metaclass__ = FlyWeight
    def __init__(self, path):
        self.setSurface(path)

    def setSurface(self, p):
        self._surf = pygame.image.load(p) if p else None
        
    def getSurface(self):
        return self._surf

    surface = property(lambda self: self._surf, setSurface)

class Camara(object): #solo se necesita una (singleton)
    '''ayuda a saber la posicion absoluta (pantalla) de los objetos
    en base a sus posiciones relativas(sus posiciones de objeto)'''
    __metaclass__ = Singleton
    def __init__(self, localizacion = (0, 0), holgura = 90, canvas = None):
        object.__init__(self)
        self._setLocalizacion(localizacion)
        self._setHolgura(holgura)
        self._setTamCam(canvas)

    def _setLocalizacion(self, l):
        self._localizacion = l

    localizacion = property(lambda self: self._localizacion, _setLocalizacion)

    def _setHolgura(self, h):
        self._holgura = h

    holgura = property(lambda self: self._holgura)

    def _setTamCam(self, c):
        self._tamCam = c.get_size()
        
    tamCam = property(lambda self: self._tamCam)

    midLand = property(lambda self: (self._tamCam[0] / 2, self._tamCam[1] / 2))

    def update(self, objetivo, escenario):
        objetivox = objetivo.localizacion[0] + objetivo.tamano[0]/2
        objetivoy = objetivo.localizacion[1] + objetivo.tamano[1]/2
        camy = self._localizacion[1]
        camx = self._localizacion[0]
        if (camx + self.midLand[0]) - objetivox > self._holgura: #limite de la izquierda
            self._localizacion = objetivox + self._holgura - self.midLand[0], camy
            if self._localizacion[0] < 0:
                self._localizacion = (0, camy)
        elif objetivox - (camx + self.midLand[0]) > self._holgura: #limite de la derecha
            self._localizacion = objetivox - self._holgura - self.midLand[0], camy
            if self._localizacion[0] + self._tamCam[0] > escenario.size[0]:
                self._localizacion = (escenario.size[0] - self._tamCam[0], camy)
        camx = self._localizacion[0]
        if (camy + self.midLand[1]) - objetivoy > self._holgura: #limite de arriba
            self._localizacion = camx, objetivoy + self._holgura - self.midLand[1]
            if self._localizacion[1] < 0:
                self._localizacion = (camx, 0)
        elif objetivoy - (camy + self.midLand[1]) > self._holgura: #limite de abajo
            self._localizacion = camx, objetivoy - self._holgura - self.midLand[1]
            if self._localizacion[1] + self._tamCam[1] > escenario.size[1]:
                self._localizacion = (camx, escenario.size[1] - self._tamCam[1])

class ImgLogic(object):
    def __init__(self, localizacion = (0, 0), pathImagen = None, tamano = (0, 0), rotacion = 0, zoom = (1, 1)):
        object.__init__(self)
        self._setLocalizacion(localizacion)
        self._setPathImagen(pathImagen)
        self._setTamano(tamano)
        self._setRotacion(rotacion)
        self._setZoom(zoom)

    def _setLocalizacion(self, l):
        self._localizacion = l

    localizacion = property(lambda self: self._localizacion, _setLocalizacion, doc='get/set posicion logica del objeto')

    def _setTamano(self, t):
        if not (t is None):
            if t[0] < 0 or t[1] < 0:
                raise StandardError, 'el tamano de la imagen debe ser mayor que cero'
        self._tamano = t

    tamano = property(lambda self: self._tamano, _setTamano, doc='get/set tamano del personaje')

    def _setPathImagen(self, p):
        x = p
        if not (p is None):
            x = o_p_abspath(p)
            if not o_p_exists(x):
                raise ValueError, 'la pathImagen debe tener una ruta valida'
        self._pathImagen = x

    pathImagen = property(lambda self: self._pathImagen, _setPathImagen, doc='set/get archivo de pathImagen')

    def _setRotacion(self, r):
        self._rotacion = r

    rotacion = property(lambda self: self._rotacion, _setRotacion, doc='set/get rotacion de la imagen')

    def _setZoom(self, z):
        if z[0] <= 0 or z[1] <= 0:
            raise StandardError, 'el zoom debe ser mayor que cero'
        self._zoom = z

    zoom = property(lambda self: self._zoom, _setZoom, doc='set/get zoom (efecto multiplicativo al tamano)')

class ImgInPyG(ImgLogic):
    def __init__(self, pathImagen = None, localizacion = (0, 0), tamano = (0, 0), rotacion=0, zoom =(1,1), colision = None, trans = 0):
        self._trans = trans
        ImgLogic.__init__(self, localizacion, pathImagen, tamano, rotacion, zoom)
        self._ant_tam = None
        self._ant_rot = None
        self._ant_zoo = None
        self._pyGImageTransform = None
        # self._setColisionArea(colision)

    def _setPathImagen(self, p): ## sobreescrito
        super(ImgInPyG, self)._setPathImagen(p)
        self._setPyGImage()

    def _setTamano(self, t): ## sobreescrito
        if t == (0,0):
            t = self._pyGImage.get_size() if self._pyGImage else None
        super(ImgInPyG, self)._setTamano(t)

    def _setPyGImage(self):
        x = Surface(self._pathImagen) if self._pathImagen else None
        x = x.getSurface() if x is not None else None
        self._pyGImage = x if x is None else (x.convert() if not self._trans else x.convert_alpha())

    surface = property(lambda self: self._pyGImage)

    def getDefaultPyGRect(self):
        rec = pygame.Rect(self._localizacion, self._tamano)
        if self._pathImagen:
            rec = self.getPyGImageTransform().get_rect()
            rec.x, rec.y = self._localizacion
        return rec

    defaultRect = property(getDefaultPyGRect)

    def _obtainPyGImageTransform(self):
        x = self._pyGImage
        equal_tam = self._tamano == (x.get_width(),x.get_height())
        rotada = self._rotacion != 0.0 or self._rotacion % 360.0 != 0.0
        zoomed = self._zoom != (1,1)
        if (not equal_tam) or zoomed:
            sc = int(self.tamano[0] * self.zoom[0]), int(self.tamano[1] * self.zoom[1])
            x = pygame.transform.scale(x, sc)
        if rotada:
            x = pygame.transform.rotate(x, self._rotacion)
        return x

    def getPyGImageTransform(self):
        if self._pyGImageTransform is None:
            self._pyGImageTransform = self._obtainPyGImageTransform()
        if self._ant_tam != self._tamano:
            self._pyGImageTransform = self._obtainPyGImageTransform()
            self._ant_tam = self._tamano
        if self._ant_rot != self._rotacion:
            self._pyGImageTransform = self._obtainPyGImageTransform()
            self._ant_rot = self._rotacion
        if self._ant_zoo != self._zoom:
            self._pyGImageTransform = self._obtainPyGImageTransform()
            self._ant_zoo = self._zoom
        return self._pyGImageTransform

    PyGImageTransform = property(getPyGImageTransform, doc = 'get pygame.transform.scale(img)')

    def _setColisionArea(self, c):
        self._colision = c

    colision = property(lambda self: self._colision, _setColisionArea)

    def __repr__(self):
        return '<{0}.{1}>'.format(__name__,'ImgInPyG')

class ImageArray(list):
    def __init__(self, iipg = ImgInPyG(None), subDivision = (1,1), trueLen = 0, frame = 0):
        '''para inicializar el objeto necesitamos listas o tuplas de dos elementos
        el primer elemento es de tipo ImgInPyG
        el segundo una lista con las partes a dividir la imagen (y posiblemente el orden que tomaran)'''
        list.__init__(self)
        self._setImgInPyG(iipg)
        self._setTrueLen(trueLen)
        self._setSubDivision(subDivision)
        self._setFrame(frame)
        self._setImgs()

    def _getSubSize(self):
        return self._iipg.surface.get_size()[0] / float(self._subDivision[0]), self._iipg.surface.get_size()[1] / float(self._subDivision[1])

    subSize = property(_getSubSize)

    def _setImgInPyG(self, i):
        self._iipg = i
        
    iipg = property(lambda self: self._iipg, _setImgInPyG, doc='regresa el objeto ImgInPyG')

    def _setSubDivision(self, s):
        if (not type(s) is tuple) and len(s) != 2:
            raise Exception, 'subD no es adecuado'
        try:
            if self._subDivision != s:
                while len(self):
                    del(self[0])
        except:
            pass
        finally:
            self._subDivision = s
        self._setImgs()

    subDivision = property(lambda self: self._subDivision,_setSubDivision)

    def _setTrueLen(self, l):
        if l < 0:
            raise Exception, 'ese valor no es aceptable'
        self._trueLen = l
        if len(self) > 0:
            while(len(self)):
                del(self[0])
        try:
            self._setImgs()
        except:
            pass
        try:
            if self._frame > self._trueLen:
                self._setFrame(0)
        except:
            pass

    trueLen = property(lambda self: self._trueLen, _setTrueLen)

    def _setFrame(self, f):
        if f > self._trueLen:
            raise Exception, 'el numero es mayor a la longitud '
        self._frame = f

    frame = property(lambda self: self._frame, _setFrame)

    def __add__(self, arg):
        raise TypeError, 'operacion no implementada'

    def __iadd__(self, arg):
        raise TypeError, 'operacion no implementada'

    def __mul__(self, arg):
        raise TypeError, 'operacion no implementada'

    def __rmul__(self, arg):
        raise TypeError, 'operacion no implementada'

    def __imul__(self, arg):
        raise TypeError, 'operacion no implementada'

    def __setitem__(self, *arg):
        raise TypeError, 'operacion no implementada'

    def __setslice__(self, *args):
        raise TypeError, 'operacion no implementada'

    def __repr__(self):
        return '<ImageArray {0}>'.format(super(ImageArray,self).__repr__())

    def append(self, arg):
        raise TypeError, 'operacion no implementada'

    def extend(self, *args):
        raise TypeError, 'operacion no implementada'

    def insert(self, *arg):
        raise TypeError, 'operacion no implementada'

    def _setImgs(self):
        # if self:
            # super(ImageArray,self).__delslice__(0,len(self) -1)
        if not self:
            count = [0,0]
            tam = self._getSubSize()
            verdad = True
            while count[0] < self._subDivision[0] and verdad:
                count[1] = 0
                while count[1] < self._subDivision[1]:
                    subRect = (count[0] * tam[0], count[1] * tam[1], tam[0], tam[1])
                    super(ImageArray,self).append(self._iipg.PyGImageTransform.subsurface(subRect))
                    count[1] += 1
                    if self._trueLen and (count[0]+1)*(count[1]+1) > self._trueLen:
                        verdad = False
                        break
                count[0] += 1
                
    def getPyGRect(self):
        return pygame.Rect(self._iipg.localizacion, self._getSubSize())

    PyGRect = property(getPyGRect)

    def getCurrentImgInPyG(self):
        self._frame += 1
        if self._frame >= len(self):
            self._frame = 0
        return self[self._frame - 1]

    currentImgInPyG = property(getCurrentImgInPyG)
    
    def setGlobalZoom(self):
        for i in self:
            print i, 'hey'

class Obstaculo(object):
    def __init__(self, iipg):
        object.__init__(self)
        self._setImgInPyG(iipg)

    def _setImgInPyG(self, i):
        self._iipg = i

    iipg = property(lambda self: self._iipg, _setImgInPyG)

class Item(object):
    def __init__(self, iipg, valor = 0, cura = 0):
        object.__init__(self)
        self._setImgInPyG(iipg)
        self._setValor(valor)
        self._setCura(cura)

    def _setImgInPyG(self, i):
        self._iipg = i

    iipg = property(lambda self: self._iipg, _setImgInPyG)

    def _setValor(self, v):
        self._valor = v

    valor = property(lambda self: self._valor, _setValor)

    def _setCura(self, c):
        self._cura = c

    cura = property(lambda self: self._cura, _setCura)

class ItemUsable(Item):
    def __init__(self, iipg, valor = 0, cura = 0, tipo = 0, fuerza = 0, retraso = 0, cantidad = 0):
        Item.__init__(self, iipg, valor, cura)
        self._setTipo(tipo)
        self._setFuerza(fuerza)
        self._setRetraso(retraso)
        self._setCantidad(cantidad)

    def _setTipo(self, t):
        self._tipo = t

    tipo = property(lambda self: self._tipo, _setTipo)

    def _setFuerza(self, f):
        self._fuerza = f

    fuerza = property(lambda self: self._fuerza, _setFuerza)

    def _setRetraso(self, r):
        self._retraso = r

    retraso = property(lambda self: self._retraso, _setRetraso)

    def _setCantidad(self, c):
        self._cantidad = c

    cantidad = property(lambda self: self._cantidad, _setCantidad)

class Npc(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, args)
        self._setTexto(kwargs['dialogo'] if 'dialogo' in kwargs else [])
        self._setLocalizacion(kwargs['localizacion'] if 'localizacion' in kwargs else (0,0))
        self._init0()

    def _setTexto(self, t):
        '''formato [[dialogo0_0, dialogo0_1],[dialogo1],[dialogo2_0,dialogo2_1]]'''
        self._texto = t

    texto = property(lambda self: self._texto, _setTexto)

    def _init0(self):
        if not self:
            self._anterior = None
        else:
            self._anterior = 0

    indice = property(lambda self: self._anterior)

    def _setLocalizacion(self, l):
        for i in range(len(self)):
            getattr(super(Npc, self).__getitem__(i),'iipg').localizacion = l

    def _getLocalizacion(self):
        return getattr(super(Npc, self).__getitem__(0),'iipg').localizacion

    localizacion = property(_getLocalizacion, _setLocalizacion)
    
    def _getTamano(self):
        return getattr(super(Npc, self).__getitem__(0),'iipg').tamano
        
    tamano = property(_getTamano)

    def getPyGRect(self, i = 0):
        return getattr(super(Npc, self),'__getitem__')(i).PyGRect

    def __getitem__(self, i):
        if self._anterior != i:
            getattr(super(Npc, self),'__getitem__')(i).frame = 0
        self._anterior = i
        return super(Npc, self).__getitem__(i)

class Personaje(Npc):
    def __init__(self, *args, **kwargs):
        Npc.__init__(self, *args)
        self._setUsable(kwargs['usable'] if 'usable' in kwargs else None)
        self._setFuerza(kwargs['fuerza'] if 'fuerza' in kwargs else 0)
        self._setVelocidad(kwargs['velocidad'] if 'velocidad' in kwargs else 0)
        self._setV_Ataque(kwargs['v_ataque'] if 'v_ataque' in kwargs else 0)
        self._setVida(kwargs['vida'] if 'vida' in kwargs else 0)
        self._setLocalizacion(kwargs['localizacion'] if 'localizacion' in kwargs else (0,0))
        self._init0()

    def _setFuerza(self, f):
        self._fuerza = f

    def _getFuerza(self):
        if self._usable:
            return self._usable.fuerza + self._fuerza
        return self._fuerza

    fuerza = property(_getFuerza, _setFuerza)

    def _setVelocidad(self, v):
        self._velocidad = v

    velocidad = property(lambda self: self._velocidad, _setVelocidad)

    def _setV_Ataque(self, v):
        self._v_ataque = v

    v_ataque = property(lambda self: self._v_ataque, _setV_Ataque)

    def _setVida(self, v):
        self._vida = v

    vida = property(lambda self: self._vida, _setVida)

    def _setUsable(self, u):
        self._usable = u

    usable = property(lambda self: self._usable, _setUsable)

    # def setSize(self, t):
        # for 

class Escenario(object):
    def __init__(self, size = (800,600), background = [], personajes = [], obstaculos = [], enemigos = [], items = [], usable = [], utileria = []):
        object.__init__(self)
        self._setSize(size)
        self._setBackGround(background)
        self._setPersonajes(personajes)
        self._setObstaculos(obstaculos)
        self._setEnemigos(enemigos)
        self._setItems(items)
        self._setUsableItems(usable)
        self._setUtileria(utileria)

    def _setSize(self, s):
        self._size = s

    size = property(lambda self: self._size, _setSize)

    def _setBackGround(self, b):
        if not type(b) is list:
            raise Exception, 'debe ser una lista'
        self._background = b

    background = property(lambda self: self._background, _setBackGround, doc='lista de elementos que no se necesita saber su colision')

    def _setPersonajes(self, p):
        # if not type(p) is list:
            # raise Exception, 'debe ser una lista'
        self._personajes = p

    personajes = property(lambda self: self._personajes, _setPersonajes, doc = 'lista de personajes en un juego (tentativamente seria uno :[), incluye sus propios atributos de rect para saber colision')

    def _setObstaculos(self, o):
        if not type(o) is list:
            raise Exception, 'debe ser una lista'
        self._obstaculos = o

    obstaculos = property(lambda self: self._obstaculos, _setObstaculos, doc = 'lista de objetos que se requiere saber su colision para bloquear el paso de un personaje, enemigo, etc')

    def _setEnemigos(self, e):
        if not type(e) is list:
            raise Exception, 'debe ser una lista'
        self._enemigos = e

    enemigos = property(lambda self: self._enemigos, _setEnemigos, doc = 'lista de Personajes que hacen danyo al o los Personajes')

    def _setItems(self, i):
        if not type(i) is list:
            raise Exception, 'debe ser una lista'
        self._items = i

    items = property(lambda self: self._items, _setItems, doc = 'lista de objetos que se pueden coleccionar y/o dar puntos')

    def _setUsableItems(self, ui):
        if not type(ui) is list:
            raise Exception, 'debe ser una lista'
        self._usableItems = ui

    usableItems = property(lambda self: self._usableItems, _setUsableItems, doc = 'sirven para dar mas fuerza, velocidad u algun atributo a un personaje')

    def _setUtileria(self, u):
        if not type(u) is list:
            raise Exception, 'debe ser una lista'
        self._utileria = u

    utileria = property(lambda self: self._utileria, _setUtileria, doc = 'lisat de objetos que sirven para cosas utiles, pero tal vez con poco sentido al juego')

    # def choca(self):
        # return self._personajes[0].collidelist(self._obstaculos)

if __name__ == '__main__':
    # class Help:
        # def get_size(self):
            # return (800,600)

    # c = Camara(canvas = Help())
    # print c.midLand, c.localizacion, c.tamCam
    # p = ImgLogic()
    # e = Escenario(size = (1000,1000))
    # p.localizacion = c.midLand[0] - 20, c.midLand[1] - 20
    # p.tamano = (40,40)
    # c.update(p, e)
    # print c.midLand, c.localizacion, c.tamCam
    # print c.localizacion
    # p.localizacion = (p.localizacion[0],p.localizacion[1]+100)
    # c.update(p, e)
    # print c.localizacion
    # p.localizacion = (p.localizacion[0],p.localizacion[1]+ 1000)
    # c.update(p, e)
    # print c.localizacion
    # print type(c), c.__metaclass__
    a = ImgInPyG(None)
    al = a.localizacion[0] + 20, a.localizacion[1] + 20
    at = a.tamano[0] - 10, a.tamano[1] - 10
    a.colision = pygame.Rect(al,at)
    print a, a.colision
