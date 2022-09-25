import pygame
import os

# Carga imagen
def loadImage (resource,dim=None) :
	if not resource : return None
	if not pygame.display.get_init() : pygame.display.init()
	img=pygame.image.load(resource).convert_alpha()
	if dim : img=pygame.transform.scale(img,dim)
	return img

# Escala imagen
def scaleImage (image,dim) :
	if not image : return None
	return pygame.transform.scale(image,dim)

# Rota imagen
def rotateImage(image,direction) :
	if not image : return None
	return pygame.transform.rotate(image,direction)

# Carga sonido
def loadSound (resource) :
	if not resource : return None
	return pygame.mixer.Sound(resource)

# Devuelve archivos con un determinado formato en una ruta específica
def getResource (route='.',format='.png') :
	doc=os.listdir(route)
	archive=[]
	for arch in doc :
		if os.path.isfile(os.path.join(route,arch)) and arch.endswith(format) : archive.append(arch)
	return archive