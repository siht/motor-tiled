from Logics import *
try:
    pygame
except:
    import pygame

def cargarImgInPyG(canvas, p = ImgInPyG(None)):
    canvas.blit(p.PyGImageTransform, p.localizacion)
    
def cargarImgInPyG2(canvas, p = ImgInPyG(None), camara = None):
    loc = (p.localizacion[0] - camara.localizacion[0], p.localizacion[1] - camara.localizacion[1])
    canvas.blit(p.PyGImageTransform, loc)

def chargeImgInPyG(canvas, p = ImgInPyG(None)):
    canvas.blit(p.pyGImage, p.localizacion)

def zoomImgInPyG(p, zoom = (0,0)):
    p.tamano = (p.tamano[0]+zoom[0],p.tamano[1]+zoom[1])
    p.localizacion = (p.localizacion[0]-zoom[0]/2.0, p.localizacion[1]-zoom[1]/2.0)

def cargarArr(canvas, arr):
    canvas.blit(arr.currentImgInPyG, arr.PyGRect)
    
def cargarImagenRelativa(canvas, imagen, camara):
    loc = (imagen.localizacion[0] - camara.localizacion[0], imagen.localizacion[1] - camara.localizacion[1])
    canvas.blit(imagen.pyGImage, loc)