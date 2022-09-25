import pygame
import math,random,copy,enum
from pygame.locals import *

pygame.mixer.init()
pygame.font.init()
pygame.display.init()

from constant import *

# Ventana
window=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('The Walking Dead')

from data import *
from functions import *
from resources import *
from interface import *
from objects import *

# Variables globales
#-----------------------------------------------------------------------------------------------------------------------

pyevents=pygame.event.get() # Eventos del pygame

resources=Resources()

camera=[0,0] # Posición con respecto el mapa de la camara
target=None # Objetivo de la camara

objectsGroups = {}
for obj in TypeObjects : objectsGroups[obj.name]=[]

# Funciones
#-----------------------------------------------------------------------------------------------------------------------

exit=False
pause=False
clickInGame=True
def setExit (value) :
	global exit
	exit=value
def getExit () : return exit
def setPause (value) :
	global pause
	pause=value
	for group in list(objectsGroups) :
		for obj in objectsGroups[group] : obj.pause(pause)
def getPause () : return pause
def setClickInGame (value) :
	global clickInGame
	clickInGame=value
def getClickInGame () : return clickInGame

def getImage (image) : return resources.getImage(image)
def getSound (sound) : return resources.getSound(sound)

def setTarget (t) :
	global target
	target=copy.copy(t)

def setCamera (target) :
	global camera
	if target :
		camera=list(copy.copy(target.pos))
	else :
		camera=[0,0]

def getRandomPos () : return (random.randint(0,WIDTH_FIELD),random.randint(0,HEIGHT_FIELD))

# Colisiones
def collisionRectSprite (class1,class2) : return pygame.sprite.collide_rect(class1,class2)
def collisionMaskSprite (class1,class2) :
	if not pygame.sprite.collide_mask(class1,class2) : return False
	return True
def collisionSprite (class1,class2) :
	if not collisionRectSprite(class1,class2) : return None
	return collisionMaskSprite(class1,class2)

def objectInList (objects) :
	for group in list(objectsGroups) :
		if objects in objectsGroups[group] : return True
	return False

ENEMYATTACK = [TypeObjects.PLAYERS.name,TypeObjects.ZOMBIES.name,TypeObjects.BUILDINGS.name,TypeObjects.OBJECTS.name]

# Obtiene todos los objetos dentro de un radio en un determinado punto
def objectInRadiusAttack (pos,radius) :
	objects=[]
	for group in ENEMYATTACK :
		for obj in objectsGroups[group] :
			if getLonPoints(pos,obj.pos) <= radius : objects.append(obj)
	return objects

def collisionAll (mask) :
	objects=[]
	for group in objectsGroups :
		for obj in objectsGroups[group] :
			if collisionSprite(mask,obj) : objects.append(obj)
	return objects

def collisionAttack (mask,character=None) :
	objects=[]
	enemy=copy.copy(ENEMYATTACK)
	if character : enemy=copy.copy(character.enemy)
	for group in enemy :
		if group in objectsGroups :
			for obj in objectsGroups[group] :
				if obj == mask : continue
				if collisionSprite(mask,obj) :
					objects.append(obj)
	return objects

def signo (numero) :
	if numero >= 0 : return 1
	else : return -1

def attack (mask,hurt,character=None,kill_everyone=False) :
	objects=[]
	obj=collisionAttack(mask,character)
	if not kill_everyone :
		if len(obj) > 0 : objects.append(obj[0])
	else : objects=obj
	for i in objects : i.wound(hurt)
	return objects

def getMask (image) : return pygame.mask.from_surface(image)

# A partir de la posicion con respecto al campo, devuelve la posición de la ventana
def getPosWindow (pos) :
	x=round(WIDTH/2-camera[0]+pos[0])
	y=round(HEIGHT/2-camera[1]+pos[1])
	return x,y

# Devuelve el texto y rect
def getText (txt,font,color,pos) :
	text = font.render(txt,0,color)
	rect_text = text.get_rect(center=pos)
	return text,rect_text

def makeArmory (armory) :
	if not armory in LISTARMORY : return None
	return copy.copy(LISTARMORY[armory])

# Devuelve la posición con respecto al campo de un status (un status es (radius,angle,direction) con respecto a un punto)
def getPosByStatus (pos_center,direction_center,status) :
	radius,angle,direction=status
	return pos_center[0]+radius*math.cos(angleToPolar(direction_center+angle)),pos_center[1]-radius*math.sin(angleToPolar(direction_center+angle))

# Devuelve la imagen con respecto un status y la imagen
def getImageByStatus (pos_center,direction_center,image,status) :
	radius,angle,direction=status
	img=rotateImage(image,direction+direction_center)
	rect=img.get_rect(center=getPosWindow(getPosByStatus(pos_center,direction_center,status)))
	return img,rect

# Desplaza a la izquierda un diccionario
def shiftLeftDict (dictt) :
	listt=[]
	for i in dictt :
		if dictt[i] != None : listt.append(copy.copy(dictt[i]))
	a,end=0,False
	for i in dictt :
		if not end : dictt[i]=listt[a]
		else : dictt[i]=None
		a+=1
		if a >= len(listt) : end=True
	return dictt

# Devuelve la distancia de un punto a la camara
def getLonPoints (pos1,pos2) : return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
def getRadiusOfCamera (pos) : return getLonPoints(camera,pos)

# Pasa de degrees a polas
def angleToPolar (angle) : return angle*math.pi/180
# Pasa de polar a degrees
def angleToDegrees(angle) : return angle*180/math.pi

# Obtiene sonido oido por la camara
def getSoundByCamera (sound,pos) :
	if getRadiusOfCamera(pos) <= SENSITIVITY_SOUND_CAMERA : return sound
	return None
# Escuchamos sonido
def playSound (sound,loop=0) : resources.playSound(sound,loop)
# Paramos sonido
def stopSound (sound) : resources.stopSound(sound)
def setMuteSound (value) : resources.setMuteSound(value)
def getMuteSound () : return resources.getMuteSound()
def setMuteMusic (value) : resources.setMuteMusic(value)
def getMuteMusic () : return resources.getMuteMusic()

def addList (obj) :
	global objectsGroups
	if obj == None : return
	if obj.getGroup() in objectsGroups : objectsGroups[obj.getGroup()].append(obj)

def delList (obj) :
	global objectsGroups
	if obj.getGroup() in objectsGroups :
		if obj in objectsGroups[obj.getGroup()] : objectsGroups[obj.getGroup()].remove(obj)

def addInterface (window) :
	objectsGroups[TypeObjects.INTERFACES.name].clear()
	addList(window)
def closeInterface () :
	for obj in objectsGroups[TypeObjects.INTERFACES.name] : obj.closeWindow()

# Obtenemos dimension de una imagen con respeto una dimension y una proporcion (sobre 100)
def getProportionDim (dim,proportion) : return round(proportion[0]*dim[0]/100),round(proportion[1]*dim[1]/100)

# Obtenemos en que diccionario pertenece
def getDictCode (d) :
	if d in ARMORY : return 'ARMORY'
	if d in MUNITION : return 'MUNITION'
	return None

# Obtenemos diccionario
def getDict (d) :
	if getDictCode(d) == 'ARMORY' : return ARMORY[d]
	if getDictCode(d) == 'MUNITION' : return MUNITION[d]
	return None

# Interfaz
#-----------------------------------------------------------------------------------------------------------------------

class Timer :

	def __init__ (self,colorArc,colorText,pos=(round(WIDTH/2),round(HEIGHT/2+150))) :
		self.image=Icon(scaleImage(getImage('circle50_black'),(70,70)),(0,0))
		self.rectArc=pygame.Rect((0,0),(60,60))
		self.colorArc=colorArc
		self.text=Text(CALIBRI_20,'',colorText,(0,0))
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.image.getPosCenter()
	def setPos (self,pos) :
		self.image.setPosCenter(pos)
		self.rectArc.center=pos
	
	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def draw (self,window,t,max_t) :
		if not self.visible : return
		self.image.draw(window)
		pygame.draw.arc(window,self.colorArc,self.rectArc,(max_t-t)*2*math.pi/max_t,2*math.pi,4)
		s = int(t/FRAMES); ms = round((t-s*FRAMES)*100/FRAMES)
		self.text.setText(str(s)+'.'+str(ms))
		self.text.setPosCenter(self.image.getPosCenter())
		self.text.draw(window)

class BulletMarker :

	def __init__ (self,player,pos=(25,HEIGHT-170)) :
		self.player=player
		self.pos=pos
		self.listMunition={}
		i=0
		for bullet in list(MUNITION) :
			if bullet == ENERGY : continue
			img1=Icon(scaleImage(getImage('square50'),(75,26)),(0,0))
			img2=Icon(scaleImage(rotateImage(getImage(MUNITION[bullet]['item']['icon_item']),MUNITION[bullet]['item']['direction_item']),(20,20)),(0,0))
			text=Text(ATWRITER_20,'',(255,255,255),(0,0))
			self.listMunition[bullet]=(img1,img2,text)
			i+=1
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.pos
	def setPos (self,pos) :
		self.pos=pos
		i=0
		for mun in list(self.listMunition) :
			munition=self.listMunition[mun]
			munition[0].setPos((pos[0]+i*85,pos[1]))
			munition[1].setPos((munition[0].getPos()[0]+5,munition[0].getPosCenter()[1]-munition[1].getDim()[1]/2))
			i+=1
	def getDim (self) :
		ult=self.listMunition[list(self.listMunition)[len(self.listMunition)-1]]
		return ult.getRight()-self.getPos()[0], ult.getDim()[1]

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def draw (self,window) :
		if not self.visible : return
		for mun in list(self.listMunition) :
			munition=self.listMunition[mun]
			munition[0].draw(window)
			munition[1].draw(window)
			munition[2].setText(str(self.player.listMunition[mun]))
			munition[2].setPos((munition[0].getRight()-5-munition[2].getDim()[0],munition[0].getPosCenter()[1]-munition[2].getDim()[1]/2))
			munition[2].draw(window)

class LifeMarker :

	def __init__ (self,player,pos=(20,HEIGHT-128)) :
		self.player=player
		self.markerLife=MarkerStick((440,10),(0,0),color=(203,76,76),colorEdge=(0,0,0),sizeEdge=1)
		self.markerShield=MarkerStick((440,10),(0,0),color=(42,159,117),colorEdge=(0,0,0),sizeEdge=1)
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.markerShield.getPos()
	def setPos (self,pos) :
		self.markerShield.setPos(pos)
		self.markerLife.setPos((pos[0],self.markerShield.getBottom()+5))

	def getDim (self) : return self.markerLife.getDim()[0],self.markerLife.getBottom()-self.markerShield.getTop()

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def draw (self,window) :
		if not self.visible : return
		self.markerLife.draw(window,self.player.getLife(),self.player.getMaxLife())
		self.markerShield.draw(window,self.player.getShield(),self.player.getMaxShield())

class ArmoryBoxes :

	colorBoxSelection,colorBox=(29,213,179),(101,117,114)

	def __init__ (self,player,pos=(20,HEIGHT-95)) :
		self.player=player
		self.pos=list(pos)
		self.listBoxes={}
		for i in range(len(self.player.listArmory)) : self.listBoxes[i]=Square((65,65),(0,0),self.colorBox,4)
		self.visible=True
		self.setPos(pos)

	def getPos (self) : return self.pos
	def setPos (self,pos) :
		self.pos=list(pos)
		for i in list(self.listBoxes) :
			box=self.listBoxes[i]
			box.setPos((pos[0]+i*box.getDim()[0]+i*10,pos[1]))

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible

	def draw (self,window) :
		if not self.visible : return
		for i in list(self.listBoxes) :
			box=self.listBoxes[i]
			armory=self.player.getArmory(i)
			if armory :
				imgIcon=armory.getItem().getImage(box.getDim())
				rectIcon=imgIcon.get_rect(center=box.getPosCenter())
				window.blit(imgIcon,rectIcon)
				text,rect=getText(str(armory.getMagazine()),COMIC_30,(255,255,255),(0,0))
				rect.right,rect.bottom=box.getRight()-5,box.getBottom()-5
				window.blit(text,rect)
			if i == self.player.getActualArmory() : box.setColor(self.colorBoxSelection)
			else : box.setColor(self.colorBox)
			box.draw(window) 

class TimerCadence :

	def __init__ (self,player) :
		self.player=player
		self.width,self.height=(80,10)
		self.center=(80,450)
		self.color=(80,80,80)
		self.rect=pygame.Rect(0,0,self.width,self.height)
		self.rect.center=self.center
		self.visible=True

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 
	
	def draw (self,window) :
		if not self.visible : return
		armory=self.player.listArmory[self.player.nArmory]
		if armory.function == 'weapon' :
			if armory.reloadTime <= 0 and armory.cadenceTime > 0 and armory.cadence > 0 and armory.magazine > 0 :
				w=round(armory.cadenceTime*self.width/armory.cadence)
				self.rect.width,self.rect.center=w,self.center
				pygame.draw.rect(window,self.color,self.rect)

class PropertiesWeapon :

	dim=(300,170)
	maxCadence,maxReload,maxHurt,maxLong=2*FRAMES,5*FRAMES,1000,1500

	def __init__ (self,player,pos=(10,10)) :
		self.player=player
		self.background=Icon(scaleImage(getImage('square50'),self.dim),pos)
		txt=Text(IMPACT_15,'texto',(255,255,255),(0,0))
		self.txtCadence=Text(IMPACT_15,'cadencia',(255,255,255),(0,0))
		self.txtReload=Text(IMPACT_15,'Recarga',(255,255,255),(0,0))
		self.txtHurt=Text(IMPACT_15,'Daño',(255,255,255),(0,0))
		self.txtLong=Text(IMPACT_15,'Distancia',(255,255,255),(0,0))
		self.txtCapacity=Text(IMPACT_15,'Capacidad :',(255,255,255),(0,0))
		self.txtCapacityWeapon=Text(COMIC_30,'',(150,150,250),(0,0))
		self.txtType=Text(IMPACT_15,'Tipo :',(255,255,255),(0,0))
		self.txtTypeWeapon=Text(COMIC_30,'',(255,218,69),(0,0))
		d,color,colorBackground=(175,self.txtCadence.getDim()[1]),(255,255,255),(200,100,100)
		self.stickCadence=MarkerStick(d,(0,0),color=color,colorBackground=colorBackground)
		self.stickReload=MarkerStick(d,(0,0),color=color,colorBackground=colorBackground)
		self.stickHurt=MarkerStick(d,(0,0),color=color,colorBackground=colorBackground)
		self.stickLong=MarkerStick(d,(0,0),color=color,colorBackground=colorBackground)
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.background.getPos()
	def setPos (self,pos) :
		self.background.setPos(pos)
		self.txtCadence.setPos((pos[0]+10,pos[1]+10))
		self.txtReload.setPos((pos[0]+10,self.txtCadence.getBottom()+10))
		self.txtHurt.setPos((pos[0]+10,self.txtReload.getBottom()+10))
		self.txtLong.setPos((pos[0]+10,self.txtHurt.getBottom()+10))
		self.txtCapacity.setPos((pos[0]+10,self.txtLong.getBottom()+15))
		self.txtCapacityWeapon.setPos((self.txtCapacity.getRight()+10,self.txtCapacity.getPosCenter()[1]-self.txtCapacityWeapon.getDim()[1]/2))
		self.txtType.setPos((pos[0]+140,self.txtCapacity.getTop()))
		self.txtTypeWeapon.setPos((self.txtType.getRight()+10,self.txtType.getPosCenter()[1]-self.txtTypeWeapon.getDim()[1]/2))
		self.stickCadence.setPos((pos[0]+100,pos[1]+10))
		self.stickReload.setPos((pos[0]+100,self.stickCadence.getBottom()+10))
		self.stickHurt.setPos((pos[0]+100,self.stickReload.getBottom()+10))
		self.stickLong.setPos((pos[0]+100,self.stickHurt.getBottom()+10))
	def getDim (self) : return self.background.getDim()
	def getPosCenter (self) : return self.background.getPosCenter()
	def setPosCenter (self,pos) : self.setPos((pos[0]-self.background.getDim()[0]/2,pos[1]-self.background.getDim()[1]/2))  

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def draw (self,window) :
		if not self.visible : return
		weapon=self.player.getArmory()
		if weapon.function != 'weapon' : return
		self.background.draw(window)
		self.txtCadence.draw(window)
		self.txtReload.draw(window)
		self.txtHurt.draw(window)
		self.txtLong.draw(window)
		self.txtCapacity.draw(window)
		self.txtCapacityWeapon.setText(str(weapon.capacity))
		self.txtCapacityWeapon.draw(window)
		self.txtType.draw(window)
		self.txtTypeWeapon.setText(weapon.type)
		self.txtTypeWeapon.draw(window)
		self.stickCadence.draw(window,value=self.maxCadence-weapon.cadence,maxValue=self.maxCadence)
		self.stickReload.draw(window,value=self.maxReload-weapon.reload,maxValue=self.maxReload)
		self.stickHurt.draw(window,value=weapon.nBullets*weapon.hurtBullet,maxValue=self.maxHurt)
		self.stickLong.draw(window,value=weapon.lonBullet,maxValue=self.maxLong)

class Map :

	def __init__ (self,pos=(WIDTH-240,HEIGHT-240),dim=(230,230)) :
		self.image=Icon(scaleImage(getImage('square50'),dim),(0,0))
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.image.getPos()
	def setPos (self,pos) : self.image.setPos(pos)

	def getDim (self) : return self.image.getDim()

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def getPosMap (self,pos) : return round(self.image.getLeft()+pos[0]*self.getDim()[0]/WIDTH_FIELD),round(self.image.getTop()+pos[1]*self.getDim()[1]/HEIGHT_FIELD)

	def update (self) : pass
	def draw (self,window) :
		if not self.visible : return
		self.image.draw(window)
		for zombie in objectsGroups[TypeObjects.ZOMBIES.name] : pygame.draw.rect(window,(200,100,100),(*self.getPosMap(zombie.pos),5,5))
		for player in objectsGroups[TypeObjects.PLAYERS.name] : pygame.draw.rect(window,(200,200,100),(*self.getPosMap(player.pos),5,5))

class MarkerMaterials :

	dimIcon=(35,35)
	dim=(150,150)
	sep=7

	def __init__ (self,player,pos=(10,10)) :
		self.player=player
		self.pos=pos
		self.iconEnergy=Icon(scaleImage(rotateImage(getImage(MUNITION[ENERGY]['item']['icon_item']),MUNITION[ENERGY]['item']['direction_item']),self.dimIcon),self.pos)
		self.stickEnergy=MarkerStick((100,30),(0,0),color=(100,200,200),colorEdge=(0,0,0),sizeEdge=2)
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.pos
	def setPos (self,pos) :
		self.pos=pos
		self.iconEnergy.setPos(pos)
		self.stickEnergy.setPos((self.iconEnergy.getRight()+15,self.iconEnergy.getPosCenter()[1]-self.stickEnergy.getDim()[1]/2))

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def draw (self,window) :
		if not self.visible : return
		self.iconEnergy.draw(window)
		self.stickEnergy.draw(window,value=self.player.getEnergy(),maxValue=self.player.energyMax)

class MarkerBombs :

	def __init__ (self,player,pos=(round(WIDTH/2-20),round(HEIGHT/2+80))) :
		self.player=player
		self.marker=MarkerStick((40,8),(0,0),color=(100,150,150))
		self.setPos(pos)
		self.visible=True

	def getPos (self) : return self.marker.getPos()
	def setPos (self,pos) : self.marker.setPos(pos)

	def setVisible (self,visible) : self.visible=visible
	def getVisible (self) : return self.visible 

	def update (self) : pass

	def draw (self,window) :
		if not self.visible : return
		armory=self.player.getArmory()
		if armory.function == 'bomb' :
			if armory.timeThrow > 0 : self.marker.draw(window,armory.timeThrow,armory.throw)

class Interface :

	def __init__ (self,player) :
		self.player=player
		self.timerReload=Timer((255,255,255),(255,255,255))
		self.armoryBoxes=ArmoryBoxes(self.player)
		self.lifeMarker=LifeMarker(self.player)
		self.bulletMarker=BulletMarker(self.player)
		self.timerDrug=Timer((200,100,100),(200,100,100))
		self.timerCadence=TimerCadence(self.player)
		self.propiertiesWeapon=PropertiesWeapon(self.player)
		self.map=Map()
		self.markerbombs=MarkerBombs(self.player)
		self.markermaterials=MarkerMaterials(self.player)
		self.buttonPause=Icon(scaleImage(getImage('pausa'),(40,40)),(WIDTH-60,20))
		self.imgSoundOn,self.imgSoundOff=scaleImage(getImage('soundOn'),(40,40)),scaleImage(getImage('soundOff'),(40,40))
		self.buttonSound=Icon(self.imgSoundOn,(WIDTH-60,80))
		self.imgMusicOn,self.imgMusicOff=scaleImage(getImage('musicOn'),(40,40)),scaleImage(getImage('musicOff'),(40,40))
		self.buttonMusic=Icon(self.imgMusicOn,(WIDTH-60,130))

		self.viewPropertiesWeapon=False
		self.visible=True

		self.cursor0=scaleImage(getImage('cursor0'),(30,30))
		self.cursor1=scaleImage(getImage('cursor1'),(35,35))
		self.setCursor(self.cursor0)
		self.soundButton=getSound('button0')

	def getCursor (self) : return self.cursor
	def setCursor (self,cursor) : self.cursor=cursor

	def getVisible (self) : return self.visible
	def setVisible (self,visible) : self.visible=visible

	def events (self,pyevents) :
		mouse=pygame.mouse.get_pos()
		self.setCursor(self.cursor0)
		if self.buttonPause.getMouse(mouse) or self.buttonSound.getMouse(mouse) or self.buttonMusic.getMouse(mouse) : self.setCursor(self.cursor1); setClickInGame(False)
		for event in pyevents :
			if event.type == pygame.MOUSEBUTTONDOWN :
				if event.button == 1 :
					if self.buttonPause.getMouse(mouse) : playSound(self.soundButton); setPause(True)
					if self.buttonSound.getMouse(mouse) :
						playSound(self.soundButton)
						if getMuteSound() : setMuteSound(False); self.buttonSound.setImage(self.imgSoundOff)
						else : setMuteSound(True); self.buttonSound.setImage(self.imgSoundOn)
					if self.buttonMusic.getMouse(mouse) :
						playSound(self.soundButton)
						if getMuteMusic() : setMuteMusic(False); self.buttonMusic.setImage(self.imgMusicOff)
						else : setMuteMusic(True); self.buttonMusic.setImage(self.imgMusicOn)
			if event.type == pygame.KEYDOWN :
				if event.key == PYKEYS['m'] : self.map.setVisible(self.map.getVisible()==False)
				if event.key == PYKEYS['n'] : self.setVisible(self.getVisible()==False)
		keys=pygame.key.get_pressed()
		if keys[PYKEYS['o']] : self.viewPropertiesWeapon=True
		else : self.viewPropertiesWeapon=False

	def update (self) : pass

	def draw (self,window) :
		if not self.visible : return
		armory=self.player.listArmory[self.player.nArmory]
		if armory.function == 'weapon' and armory.reloadTime > 0 : self.timerReload.draw(window,armory.reloadTime,armory.reload)
		if armory.function == 'drug' and armory.cureTime > 0 : self.timerDrug.draw(window,armory.cureTime,armory.cure)
		self.armoryBoxes.draw(window)
		self.lifeMarker.draw(window)
		self.bulletMarker.draw(window)
		self.timerCadence.draw(window)
		self.map.draw(window)
		self.markerbombs.draw(window)
		if not self.viewPropertiesWeapon : self.markermaterials.draw(window)
		else : self.propiertiesWeapon.draw(window)
		self.buttonPause.draw(window)
		self.buttonSound.draw(window)
		self.buttonMusic.draw(window)

# Windows
#-----------------------------------------------------------------------------------------------------------------------

class Window :

	def __init__ (self) :
		self.setCursor(None)
		self.character=None

	def getPos (self) : pass
	def setPos (self,pos) : pass
	def getDim (self) : pass

	def getGroup (self) : return TypeObjects.INTERFACES.name
	def restart (self) : pass
	def pause (self,pause) : pass

	def openWindow (self,character) : self.character=character; addList(self)
	def closeWindow (self) : self.character=None; delList(self)

	def getCursor (self) : return self.cursor
	def setCursor (self,cursor) : self.cursor=cursor 

	def events (self,pyevents) : pass
	def update (self) : pass
	def draw (self,window) : pass

class WindowPause (Window) :

	def __init__ (self,pos=(WIDTH/2-250,HEIGHT/2-150)) :
		super().__init__()
		self.image=Icon(scaleImage(getImage('square75'),(500,300)),(0,0))
		self.buttonContinue=Square((200,50),(0,0),(150,250,150))
		self.textContinue=Text(COMIC_30,'CONTINUAR',(250,250,250),(0,0))
		self.buttonExit=Square((200,50),(0,0),(250,150,150))
		self.textExit=Text(COMIC_30,'SALIR',(250,250,250),(0,0))
		self.setPos(pos)
		self.cursor3=scaleImage(getImage('cursor3'),(40,40))
		self.cursor1=scaleImage(getImage('cursor1'),(40,40))
		self.setCursor(self.cursor3)
		self.soundButton=getSound('button0')

	def openWindow (self,character) : super().openWindow(character); setPause(True)
	def closeWindow (self) : super().closeWindow(); setPause(False)

	def setPos (self,pos) :
		self.image.setPos(pos)
		self.buttonContinue.setPosCenter((self.image.getPosCenter()[0],self.image.getPosCenter()[1]-20))
		self.textContinue.setPosCenter(self.buttonContinue.getPosCenter())
		self.buttonExit.setPosCenter((self.image.getPosCenter()[0],self.image.getPosCenter()[1]+50))
		self.textExit.setPosCenter(self.buttonExit.getPosCenter())
	def getPos (self) : return self.image.getPos()
	def getDim (self) : return self.image.getDim()

	def events (self,pyevents) :
		mouse=pygame.mouse.get_pos()
		self.setCursor(self.cursor3)
		if self.buttonContinue.getMouse(mouse) or self.buttonExit.getMouse(mouse) : self.setCursor(self.cursor1)
		for event in pyevents :
			if event.type == pygame.MOUSEBUTTONUP :
				if event.button == 1 :
					if self.buttonContinue.getMouse(mouse) : playSound(self.soundButton); closeInterface()
					if self.buttonExit.getMouse(mouse) : playSound(self.soundButton); closeInterface(); setExit(True)
	def draw (self,window) :
		self.image.draw(window)
		self.buttonContinue.draw(window)
		self.textContinue.draw(window)
		self.buttonExit.draw(window)
		self.textExit.draw(window)

class WindowItems (Window) :

	def __init__ (self) :
		super().__init__()
		self.listDict=[]
		self.itemMouse=None
		self.posItemMouse=[0,0]

		self.soundGrab=getSound('button0')
		self.soundExitItem=getSound('cartoon1')

		self.cursor1=scaleImage(getImage('cursor1'),(40,40))
		self.cursor2=scaleImage(getImage('cursor2'),(40,40))
		self.cursor3=scaleImage(getImage('cursor3'),(40,40))
		self.setCursor(self.cursor3)

		self.reward=Reward()

	def setItem (self,item,dictt,box) : pass
	def getItem (self,dictt,box) : pass
	def makeReward (self,item) :
		radius=random.randint(max(*self.character.getDim())+20,max(*self.character.getDim())+40)
		angle=random.randint(0,360)
		pos=getPosByStatus(self.character.pos,0,(radius,angle,0))
		rew=copy.copy(self.reward)
		rew.loadReward(item,pos)
		addList(rew)

	def grabItem (self,mouse,halfLot=False) :
		grab=False
		for dictt in self.listDict :
			for x in dictt :
				box=dictt[x]
				if not box.getMouse(mouse) : continue
				item=self.getItem(dictt,x)
				if item == None : return grab
				if not item.getItem() : return grab
				self.itemMouse=copy.copy(item)
				self.posItemMouse=[mouse[0]-box.getPosCenter()[0],mouse[1]-box.getPosCenter()[1]]
				lot=item.getLot()
				if halfLot and item.getMaxLot() != None :
					lot=int(item.getLot()/2)
					if lot <= 0 : lot=item.getLot()
				item.setLot(item.getLot()-lot)
				self.itemMouse.setLot(lot)
				if item.getLot() <= 0 : item=None
				self.setItem(item,dictt,x)
				grab=True
				break
			if grab : break
		return grab

	def dropItem (self,mouse,individualLot=False) :
		drop=False
		for dictt in self.listDict :
			for x in dictt :
				box=dictt[x]
				if not box.getMouse(mouse) : continue
				actualItem=self.getItem(dictt,x)
				if actualItem :
					if not actualItem.getItem() : return drop
					if actualItem.getMaxLot() != None and actualItem.getName() == self.itemMouse.getName() :
						lot=min(actualItem.getMaxLot()-actualItem.getLot(),self.itemMouse.getLot())
						if individualLot : lot=min(actualItem.getMaxLot()-actualItem.getLot(),1)
						self.itemMouse.setLot(self.itemMouse.getLot()-lot)
						if self.itemMouse.getLot() <= 0 : self.itemMouse=None
						actualItem.setLot(actualItem.getLot()+lot)
					else :
						aux=copy.copy(actualItem)
						actualItem=copy.copy(self.itemMouse)
						self.itemMouse=aux
				else :
					actualItem=copy.copy(self.itemMouse)
					if individualLot and actualItem.getMaxLot() != None :
						actualItem.setLot(1)
						self.itemMouse.setLot(self.itemMouse.getLot()-1)
						if self.itemMouse.getLot() <= 0 : self.itemMouse=None
					else : self.itemMouse=None
				self.setItem(actualItem,dictt,x)
				drop=True
				break
			if drop : break
		return drop

	def events (self,pyevents) :
		mouse=pygame.mouse.get_pos()
		if self.itemMouse == None :
			if self.image.getMouse(mouse) : self.setCursor(self.cursor3)
			else : self.setCursor(self.cursor1)
		else : self.setCursor(self.cursor2)
		for event in pyevents :
			if event.type == pygame.MOUSEBUTTONDOWN :
				if event.button == 1 :
					if self.itemMouse == None :
						grab=self.grabItem(mouse)
						if grab : playSound(self.soundGrab)
					else :
						drop=self.dropItem(mouse)
						if drop : playSound(self.soundGrab)
				if event.button == 3 :
					if not self.image.getMouse(mouse) :
						if self.itemMouse != None :
							playSound(self.soundExitItem)
							if self.itemMouse.getMaxLot() != None :
								item=copy.copy(self.itemMouse)
								item.setLot(1)
								self.makeReward(item)
								self.itemMouse.setLot(self.itemMouse.getLot()-1)
								if self.itemMouse.getLot() <= 0 : self.itemMouse=None
							else :
								self.makeReward(self.itemMouse); self.itemMouse=None
					if self.itemMouse == None :
						grab=self.grabItem(mouse,halfLot=True)
						if grab : playSound(self.soundGrab)
					else :
						drop=self.dropItem(mouse,individualLot=True)
						if drop : playSound(self.soundGrab)
			if event.type == pygame.MOUSEBUTTONUP :
				if event.button == 1 :
					if not self.image.getMouse(mouse) :
						if self.itemMouse == None : closeInterface()
						else : playSound(self.soundExitItem); self.makeReward(self.itemMouse); self.itemMouse=None

	def draw (self,window) :
		for dictt in self.listDict :
			for i in list(dictt) :
				box=dictt[i]
				box.draw(window)
				item=self.getItem(dictt,i)
				if item != None :
					img=item.getImage(self.boxDim)
					rect=img.get_rect(center=box.getPosCenter())
					window.blit(img,rect)
					if item.getMaxLot() != None :
						text,rect=getText(str(item.getLot()),COMIC_40,(40,40,40),(0,0))
						rect.right,rect.bottom=box.getRight()-5,box.getBottom()-5
						window.blit(text,rect)
		if self.itemMouse :
			mouse=pygame.mouse.get_pos()
			img=self.itemMouse.getImage(self.boxDim)
			rect=img.get_rect(center=(mouse[0]-self.posItemMouse[0],mouse[1]-self.posItemMouse[1]))
			window.blit(img,rect)
			if self.itemMouse.getMaxLot() != None :
				text,rect=getText(str(self.itemMouse.getLot()),COMIC_40,(40,40,40),(0,0))
				rect.right,rect.bottom=round(mouse[0]-self.posItemMouse[0]+self.boxDim[0]/2-5),round(mouse[1]-self.posItemMouse[1]+self.boxDim[1]/2-5)
				window.blit(text,rect)

class WindowInventory (WindowItems) :

	boxDim=(90,90)

	def __init__ (self,pos=(WIDTH/2-350,HEIGHT/2-225)) :
		super().__init__()
		self.image=Square((700,450),(0,0),(230,230,230))
		self.edge=Square(self.image.getDim(),self.image.getPos(),(50,50,50),sizeEdge=6)
		self.listInventory={}
		self.listArmory={}
		for i in range(12) : self.listInventory[i]=Square(self.boxDim,(0,0),(50,50,50),sizeEdge=4)
		for i in range(6) : self.listArmory[i]=Square(self.boxDim,(0,0),(200,120,120),sizeEdge=4)
		self.listDict=[self.listInventory,self.listArmory]
		self.setPos(pos)

	def getPos (self) : return self.image.getPos()
	def setPos (self,pos) :
		self.image.setPos(pos)
		self.edge.setPos(pos)
		x,y=round(self.getDim()[0]/2-3*self.boxDim[0]-2*7-7/2),70
		fil,col=0,0
		for i in list(self.listInventory) :
			if i == 6 : fil+=1; col=0
			box=self.listInventory[i]
			box.setPos((pos[0]+x+col*(self.boxDim[0]+7),pos[1]+y+fil*(self.boxDim[1]+10)))
			col+=1
		y=300
		for i in list(self.listArmory) :
			box=self.listArmory[i]
			box.setPos((pos[0]+x+i*(self.boxDim[0]+7),pos[1]+y))
	def getDim (self) : return self.image.getDim()

	def setItem (self,item,dictt,box) :
		if item != None :
			if item.getLot() <= 0 and item.getMaxLot() != None : item=None
		if dictt == self.listInventory : self.character.setItemInventory(item,box=box)
		elif dictt == self.listArmory :
			self.character.setItem(item,self.character.getListArmory(),box)
			self.character.shiftArmory()
	def getItem (self,dictt,box) :
		item=None
		if dictt == self.listInventory : item=self.character.getItemInventory(box)
		elif dictt == self.listArmory : item=self.character.getItem(self.character.getListArmory(),box)
		return item

	def draw (self,window) :
		self.image.draw(window)
		self.edge.draw(window)
		super().draw(window)

class WindowTrunk (WindowItems) :

	CAPACITY=16
	boxDim=(90,90)

	def __init__ (self,trunk,pos=(WIDTH/2-350,HEIGHT/2-225)) :
		super().__init__()
		self.image=Square((700,450),(0,0),(230,230,230))
		self.edge=Square(self.image.getDim(),self.image.getPos(),(50,50,50),sizeEdge=6)
		self.stickLife=MarkerStick((200,40),(0,0),color=(170,250,170),colorEdge=(20,20,20),sizeEdge=3)
		self.textLife=Text(SHERWOOD_20,'VIDA',(20,20,20),(0,0))
		self.listBox={}
		self.listArmory={}
		for box in range(self.CAPACITY) : self.listBox[box]=Square(self.boxDim,(0,0),(50,50,50),sizeEdge=4)
		for armory in range(6) : self.listArmory[armory]=Square(self.boxDim,(0,0),(200,120,120),sizeEdge=4)
		self.listDict=[self.listBox,self.listArmory]
		self.setPos(pos)

		self.trunk=trunk
		self.soundDoor=getSound('openTrunk')

	def openWindow (self,character) : playSound(self.soundDoor); super().openWindow(character); self.character.setActualArmory(0)
	def closeWindow (self) :
		if self.itemMouse : self.makeReward(self.itemMouse); self.itemMouse=None
		playSound(self.soundDoor)
		super().closeWindow()

	def getPos (self) : return self.image.getPos()
	def setPos (self,pos) :
		self.image.setPos(pos)
		self.edge.setPos(pos)
		self.stickLife.setPos((pos[0]+455,pos[1]+35))
		self.textLife.setPosCenter(self.stickLife.getPosCenter())
		fila=0
		columna=0
		for x in list(self.listBox) :
			box=self.listBox[x]
			box.setPos((pos[0]+20+(10+self.boxDim[0])*columna,pos[1]+30+(10+self.boxDim[1])*fila))
			columna+=1
			if columna >= 4 : columna=0; fila+=1
		fila=0
		columna=0
		for x in list(self.listArmory) :
			armory=self.listArmory[x]
			armory.setPos((pos[0] + 460 + (10+self.boxDim[0])*columna,pos[1]+110+(10+self.boxDim[1])*fila))
			fila+=1
			if fila >= 3 : columna+=1; fila=0
	def getDim (self) : return self.image.getDim()

	def setItem (self,item,dictt,box) :
		if item != None :
			if item.getLot() <= 0 and item.getMaxLot() != None : item=None
		if dictt == self.listBox : self.trunk.addItem(item,box=box)
		elif dictt == self.listArmory :
			self.character.setItem(item,self.character.getListArmory(),box)
			self.character.shiftArmory()

	def getItem (self,dictt,box) :
		item=None
		if dictt == self.listBox : item=self.trunk.getItem(box)
		elif dictt == self.listArmory : item=self.character.getItem(self.character.getListArmory(),box)
		return item

	def draw (self,window) :
		self.image.draw(window)
		self.edge.draw(window)
		self.stickLife.draw(window,value=self.trunk.getLife(),maxValue=self.trunk.getMaxLife())
		self.textLife.draw(window)
		super().draw(window)

# Clase Objeto
#-----------------------------------------------------------------------------------------------------------------------

class Object :

	# Constructor
	def __init__ (self,image,group=TypeObjects.LAYERTOP.name,pos=[0,0],direction=0) :
		self.image=image
		self.rect=self.image.get_rect()
		self.mask=getMask(self.image)
		self.group=group
		self.pos=list(pos)
		self.direction=direction
		self.active=True

	def kill (self) : self.active=False
	def wound (self,hurt) : pass
	def buzz (self) : pass
	def restart (self) : pass
	def pause (self,pause) : pass

	def getPos (self) : return self.pos
	def setPos (self,pos) : self.pos=pos
	def getDirection (self) : return self.direction
	def setDirection (self,direction) : self.direction=direction
	def getImage (self) : return self.image
	def setImage (self,image) : self.image=image 
	def getGroup (self) : return self.group
	def setGroup (self,group) : self.group=group
	def getActive (self) : return self.active
	def setActive (self,active) : self.active=active

	def getDim (self) : return self.rect.width,self.rect.height

	def events (self,pyevents) : pass
	def update (self) : pass
	def draw (self,window) :
		img=rotateImage(self.image,self.direction)
		self.rect=img.get_rect(center=getPosWindow(self.pos))
		self.mask=getMask(img)
		window.blit(img,self.rect)

# Recompensas
#-----------------------------------------------------------------------------------------------------------------------

class Item :

	def __init__ (self,name,lot) :
		self.name=name
		self.lot=lot
		self.reloadIcon()

	def getName (self) : return self.name
	def setName (self,name) : self.name=name; self.reloadIcon()
	def getLot (self) : return self.lot
	def setLot (self,lot) : self.lot=lot

	def getDict (self) :
		dictt=getDict(self.name)
		if dictt != None : return dictt['item']
		return None

	def initLot (self) :
		dictt=self.getDict()
		if dictt != None : self.setLot(dictt['lot'])

	def getItem (self) :
		dictt=self.getDict()
		if dictt != None : return dictt['item']
		return None
	def getMaxLot (self) :
		dictt=self.getDict()
		if dictt != None : return dictt['max_lot']
		return dictt
	def getIcon (self) :
		return self.icon
	def reloadIcon (self) :
		dictt=self.getDict()
		if dictt != None : self.icon=rotateImage(getImage(self.getDict()['icon_item']),self.getDict()['direction_item'])
	def getPropotionIcon (self) :
		dictt=self.getDict()
		if dictt != None : return dictt['proportion_item']
		return None
	def getDirection (self) :
		dictt=self.getDict()
		if dictt != None : return dictt['direction_item']
		return None
	def getColor (self) :
		dictt=self.getDict()
		if dictt != None : return dictt['color_item']
		return None
	def getImage (self,dim) : return scaleImage(self.getIcon(),getProportionDim(dim,self.getPropotionIcon()))

class Reward (Object) :

	dim=(75,75)
	dimCircle=(45,45)

	# Constructor
	def __init__ (self) : super().__init__(self.getCircleImage('black'),TypeObjects.REWARDS.name,(0,0),0)

	def loadReward (self,item,pos,direction=0) :
		self.item=copy.copy(item)
		self.setImage(self.getCircleImage(self.item.getColor()))
		self.setPos(pos)
		self.setDirection(direction)

	def getCircleImage (self,color) : return scaleImage(getImage('circle50_'+color),self.dimCircle)
	def getItem (self) : return self.item
	def setItem (self,item) : self.item=item

	def kill (self) : super().kill(); delList(self)

	def draw (self,window) :
		super().draw(window)
		img=scaleImage(self.item.getIcon(),getProportionDim(self.dim,self.item.getPropotionIcon()))
		rect=img.get_rect(center=getPosWindow(self.pos))
		window.blit(img,rect)

# Armas
#-----------------------------------------------------------------------------------------------------------------------

class Bullet (Object) :

	# Constructor
	def __init__ (self,name,speed,hurt,lon,pos=[0,0],direction=0,character=None,kill_everyone=False) :
		bullet=BULLETS[name]
		super().__init__(scaleImage(getImage(bullet['image']),bullet['dim']),TypeObjects.BULLETS.name,list(pos),direction)
		self.type=name
		self.character=character
		self.speed,self.hurt,self.lon=speed,hurt,lon
		self.lonBullet = 0 # Recorrido de la bala
		self.tail=scaleImage(getImage(bullet['tail']),bullet['dim_tail'])
		self.objects=[] # Objetos que ha dado
		self.kill_everyone=kill_everyone # Dar a varios o solo uno
		self.lonTail=bullet['lon_tail']
		self.dimTail=bullet['dim_tail']

	# Getter and Setter
	def setPos (self,pos) : self.pos=list(pos)
	def setDirection (self,direction) : self.direction=direction

	def attack (self) :
		self.objects=attack(self,self.hurt,self.character,kill_everyone=self.kill_everyone)
		if len(self.objects) > 0 : self.kill()

	def kill (self) : super().kill(); delList(self)

	def shot (self,character,pos,direction) :
		self.character=character
		self.pos=list(pos)
		self.direction=direction

	# Mover
	def move (self) :
		dx,dy=round(self.speed*math.cos(angleToPolar(self.direction))),round(-self.speed*math.sin(angleToPolar(self.direction)))
		self.lonBullet+=math.sqrt(dx**2+dy**2)
		self.pos[0]+=dx
		self.pos[1]+=dy

	# Actualizar
	def update (self) :
		self.attack()
		self.move()
		if self.lonBullet >= self.lon : self.kill()
		self.rect.center=getPosWindow(self.pos)

	# Dibujar
	def draw (self,window) :
		if self.tail and self.lonBullet >= self.lonTail :
			imgTail=rotateImage(self.tail,self.direction)
			rectTail=imgTail.get_rect()
			rectTail.center=(round(self.rect.centerx-(self.dimTail[0]/2+self.rect.width/2)*math.cos(angleToPolar(self.direction))),round(self.rect.centery+(self.dimTail[0]/2+self.rect.width/2)*math.sin(angleToPolar(self.direction))))
			window.blit(imgTail,rectTail)
		super().draw(window)

class ExplosionBullet (Bullet) :

	# Constructor
	def __init__ (self,name,speed,hurt,lon,pos=[0,0],direction=0,character=None,kill_everyone=False,radiusExplosion=100,hurtExplosion=15) :
		super().__init__(name,speed,hurt,lon,pos,direction,character,kill_everyone)
		self.explosion=Explosion(radiusExplosion,hurtExplosion)

	def action (self) :
		expl=copy.copy(self.explosion)
		expl.action(self.character,self.pos)
		addList(expl)

	def kill (self) :
		super().kill()
		self.action()

class RayBullet (Bullet) :

	def __init__ (self,name,speed,hurt,lon,pos=[0,0],direction=0,character=None,kill_everyone=False,hurtRay=10,rayTime=8,nRay=5) :
		super().__init__(name,speed,hurt,lon,pos,direction,character,kill_everyone)
		self.ray=Ray(hurtRay,rayTime,nRay)
		self.animationRay=AnimationRay(radius=100)

	def action (self) :
		for obj in self.objects :
			r=copy.copy(self.ray)
			r.action(self.character,obj)
			addList(r)
		if len(self.objects) <= 0 :
			ar=copy.copy(self.animationRay)
			ar.action(self.pos)
			addList(ar)

	def kill (self) :
		super().kill()
		self.action()

class Explosive (Object) :

	# Constructor
	def __init__ (self,bomb,pos=[0,0],direction=0) :
		bomb=ARMORY[bomb]['bomb'];
		super().__init__(scaleImage(getImage(bomb['image']),bomb['dim']),TypeObjects.BULLETS.name,list(pos),direction)
		self.type=bomb['type']
		self.radius=bomb['radius']
		self.hurt=bomb['hurt']
		self.counterExplosion=bomb['counter_explosion']
		self.character=None
		self.speed=0
		self.angle=0
		self.resistance=1 
		self.explosion=Explosion(self.radius,self.hurt)

	def shot (self,character,pos,angle,direction,force) :
		self.character=character
		self.pos=list(pos)
		self.angle=angle
		self.direction=direction
		self.speed=force

	def wound (self,hurt) : self.kill()
	def kill (self) : super().kill(); delList(self); self.action()

	def action (self) :
		expl=copy.copy(self.explosion)
		expl.action(self.character,self.pos)
		addList(expl)

	def counter (self) :
		self.counterExplosion-=1
		if self.counterExplosion <= 0 : self.kill()

	def brake (self) :
		if self.speed > 0 :
			self.speed-=self.resistance
			if self.speed < 0 : self.speed=0

	def hit (self) :
		for group in self.character.enemy :
			list_=objectsGroups[group]
			for enem in list_ :
				if collisionSprite(self,enem) : return enem
		return None

	def move (self) :
		self.pos[0]+=round(self.speed*math.cos(angleToPolar(self.angle)))
		self.pos[1]-=round(self.speed*math.sin(angleToPolar(self.angle)))

	def update (self) :
		self.move()
		self.brake()
		self.counter()

	def draw (self,window) :
		if int(self.counterExplosion/10) % 2 == 0 : pygame.draw.circle(window,(255,255,255),getPosWindow(self.pos),self.radius,2)
		super().draw(window)

class Grenade (Explosive) :

	# Constructor
	def __init__ (self,bomb) :
		super().__init__(bomb)

	def update (self) :
		super().update()
		if self.hit() : self.kill()

class StickyBomb (Explosive) :

	# Constructor
	def __init__ (self,bomb) :
		super().__init__(bomb)
		self.radiusPlayer=2000
		self.enemy=None
		self.dfAngle=0

	def paste (self) :
		if self.enemy :
			self.pos=copy.copy(self.enemy.pos)
			self.angle=self.enemy.direction-self.dfAngle
		else :
			if self.speed <= 0 : return
			self.enemy=self.hit()
			if self.enemy : self.dfAngle=self.enemy.direction-self.angle

	def update (self) :
		super().update()
		self.paste()
		if self.character :
			if self.radiusPlayer < getLonPoints(self.pos,self.character.pos) : self.kill()

class ElectricGrenade (Explosive) :

	def __init__ (self,bomb) :
		super().__init__(bomb)
		bomb=ARMORY[bomb]['bomb']
		self.ray=Ray(bomb['hurt_ray'],bomb['ray_time'],bomb['n_ray'])
		self.animationRay=AnimationRay(radius=self.radius)

	def action (self) :
		objects=objectInRadiusAttack(self.pos,self.radius)
		for obj in objects :
			obj.wound(self.hurt)
			r=copy.copy(self.ray)
			r.action(self.character,obj)
			addList(r)
		if len(objects) <= 0 :
			ar=copy.copy(self.animationRay)
			ar.action(self.pos)
			addList(ar)

	def update (self) :
		super().update()
		if self.hit() : self.kill()

class Explosion (Object) :

	# Constructor
	def __init__ (self,radius,hurt,pos=[0,0],direction=0) :
		self.dim=(2*radius,2*radius)
		super().__init__(self.getImage(0),TypeObjects.LAYERTOP.name,pos,direction)
		self.hurt=hurt
		self.character=None
		self.frame=0
		self.frameRate=0.1*FRAMES
		self.explosionTime=0
		self.soundAction=getSound('explosion0')

	def getImage (self,frame) : return scaleImage(getImage('explosion'+str(frame)),self.dim)

	def kill (self) : super().kill(); delList(self)

	def attack (self) : attack(self,self.hurt,self.character,kill_everyone=True)

	def action (self,character,pos) :
		playSound(getSoundByCamera(self.soundAction,pos))
		self.character=character
		self.pos=list(pos)
		self.frame=0
		self.explosionTime=0

	def update (self) :
		self.attack()
		self.explosionTime+=1
		if self.explosionTime >= self.frameRate : self.frame+=1; self.explosionTime=0
		if self.frame >= 9 : self.kill()

	def draw (self,window) :
		self.image=self.getImage(self.frame)
		super().draw(window)

class Ray (Object) :

	def __init__ (self,hurt,rayTime,nRay,pos=[0,0],direction=0) :
		self.IMAGE=getImage('ray')
		super().__init__(self.IMAGE,TypeObjects.LAYERTOP.name,pos,direction)
		self.character=None
		self.objects=None
		self.hurt=hurt # Daño
		self.rayTime,self.counterTime=rayTime,0 # Duración del rayo
		self.nRay,self.counterRay=nRay,0 # Número de rayos
		self.rangeDim=[20,50]
		self.radius,self.angle=0,0
		self.soundAction=getSound('buzz0')

	def action (self,character,objects) :
		self.character=character
		self.objects=objects
		self.rangeDim[0]=round(max(self.objects.rect.width/6,self.objects.rect.height/6))
		self.rangeDim[1]=round(max(self.objects.rect.width/2,self.objects.rect.height/2))

	def kill (self) : super().kill(); delList(self); stopSound(self.soundAction)

	def attack (self) :
		if self.objects.getActive() : self.objects.wound(self.hurt); self.objects.buzz()

	def loopRay (self) :
		if self.counterTime <= 0 :
			self.counterRay+=1
			if self.counterRay > self.nRay : self.kill(); return
			self.radius=random.randint(0,min(self.objects.rect.width,self.objects.rect.height))
			self.angle=random.randint(0,360)
			self.direction=random.randint(-60,60)
			dim=random.randint(self.rangeDim[0],self.rangeDim[1])
			self.image=scaleImage(self.IMAGE,(dim,dim))
			self.attack()
			stopSound(self.soundAction)
			playSound(getSoundByCamera(self.soundAction,self.objects.pos))
		self.counterTime+=1
		if self.counterTime >= self.rayTime : self.counterTime=0

	def update (self) :
		if not self.objects.getActive() : self.kill()
		self.loopRay()

	def draw (self,window) :
		self.pos=getPosByStatus(self.objects.pos,self.objects.direction,(self.radius,self.angle,self.direction))
		super().draw(window)

class Armory :

	# Constructor
	def __init__ (self,character,arm) :
		armory=ARMORY[arm]['armory']
		self.name=arm
		self.character=character
		self.function=armory['function']
		self.capacity,self.magazine=armory['capacity'],0
		self.leftHandStatus=armory['left_hand_status']
		self.rightHandStatus=armory['right_hand_status']
		self.soundAction=getSound(armory['sound_action'])
		self.soundSelectOn=getSound(armory['sound_select_on'])
		self.soundSelectOff=getSound(armory['sound_select_off'])
		self.item=Item(self.name,self.magazine)

	def getItem (self) :
		self.item.setLot(self.magazine)
		return self.item
	def setItem (self,item) : self.item=item
	def getName (self) : return self.name
	def setMagazine (self,magazine) : self.magazine=magazine
	def getMagazine (self) : return self.magazine
	def setCapacity (self,capacity) : self.capacity=capacity
	def getCapacity (self) : return self.capacity
	def getCharacter (self) : return self.character
	def setCharacter (self,character) : self.character=character

	# Eliminar armamento
	def delArmory (self,armory) :
		for i in list(self.character.listArmory) :
			if self.character.listArmory[i] == armory : self.character.delArmory(i); break

	# Acciones al dejar de ser seleccionado el armamento
	def selectOff (self) : playSound(getSoundByCamera(self.soundSelectOff,self.character.pos))
	# Acciones al ser seleccionado el armamento
	def selectOn (self) : playSound(getSoundByCamera(self.soundSelectOn,self.character.pos))

	# Fin del armamento
	def endArmory (self) : pass

	# Acción del armamento
	def action (self) : pass
	# Cancelar armamento
	def cancelAction (self) : pass
	# Reiniciar armamento
	def restart (self) : pass
	def pause (self,pause) : pass
	# Actualizar
	def update (self) : pass

	def kill (self) : stopSound(self.soundAction); stopSound(self.soundSelectOn); stopSound(self.soundSelectOff); self.restart()

	# Dibujar
	def draw (self,draw,handLeft=None,handRight=None) :
		leftHandStatus=self.leftHandStatus
		rightHandStatus=self.rightHandStatus
		if handLeft : leftHandStatus=handLeft
		if handRight : rightHandStatus=handRight
		# Mano izquierda
		imgLeftHand,rectLeftHand=getImageByStatus(self.character.pos,self.character.direction,self.character.hand,leftHandStatus)
		window.blit(imgLeftHand,rectLeftHand)
		# Mano derecha
		imgRightHand,rectRightHand=getImageByStatus(self.character.pos,self.character.direction,self.character.hand,rightHandStatus)
		window.blit(imgRightHand,rectRightHand)

class ArmoryFists (Armory) :

	# Constructor
	def __init__ (self,character,arm) :
		super().__init__(character,arm)
		armory=ARMORY[arm]['fists']
		self.leftHandAnimationAction=armory['left_hand_animation_action']
		self.rightHandAnimationAction=armory['right_hand_animation_action']
		self.animationAction,self.animationActionTime=armory['animation_action'],0
		self.hlAnimation,hrAnimation=None,None
		self.sumAnimationAction=sum(self.animationAction)

	# Acciones al dejar de ser seleccionado el armamento
	def selectOff (self) :
		super().selectOff()
		self.restart()

	# Reiniciar
	def restart (self) : super().restart(); self.animationActionTime=0; stopSound(self.soundAction)
	# Fin del armamento
	def endArmory (self) : super().endArmory(); self.restart()
	def pause (self,pause) :
		if pause :
			stopSound(self.soundAction)
		else :
			if self.animationActionTime > 0 : playSound(getSoundByCamera(self.soundAction,self.character.pos),loop=-1)

	# Pegar
	def action (self) :
		if self.animationActionTime <= 0 :
			self.animationActionTime=self.sumAnimationAction
			playSound(getSoundByCamera(self.soundAction,self.character.pos),loop=-1)

	# Bucle de la animación
	def loopAnimationAction (self) :
		if self.animationActionTime > 0 :
			self.animationActionTime-=1
			s=0
			for i in range(len(self.animationAction)) :
				s+=self.animationAction[i]
				if self.animationActionTime < s :
					self.hlAnimation,self.hrAnimation=self.leftHandAnimationAction[i],self.rightHandAnimationAction[i]
					break
			if self.animationActionTime == 0 : self.restart()
		else:
			self.hlAnimation,self.hrAnimation=None,None

	# Actualizar
	def update (self) : self.loopAnimationAction()

	# Dibujar
	def draw (self,window) : super().draw(window,self.hlAnimation,self.hrAnimation)

class ArmoryDrug (Armory) :

	# Constructor
	def __init__ (self,character,arm) :
		super().__init__(character,arm)
		armory=ARMORY[arm]['drug']
		self.name=arm
		self.image=scaleImage(getImage(armory['image']),armory['dim'])
		self.imgStatus=armory['img_status']
		self.rect=self.image.get_rect()
		self.type=armory['type']
		self.setMagazine(self.getCapacity())
		self.lifeAdded=armory['life_added']
		self.cure,self.cureTime=armory['cure'],0
		self.leftHandAnimationAction=armory['left_hand_animation_action']
		self.rightHandAnimationAction=armory['right_hand_animation_action']
		self.imgAnimationAction=armory['img_animation_action']
		self.animationAction,self.animationActionTime=armory['animation_action'],0
		self.hlAnimation,self.hrAnimation,self.imAnimation=None,None,None
		self.sumAnimationAction=sum(self.animationAction)
		self.soundCure=getSound(armory['sound_cure'])

		self.bubble=EfectObject(armory['bubble'],(15,15),1,100)
		self.timeRangeBubble=30

	# Acciones al dejar de ser seleccionado el armamento
	def selectOff (self) :
		super().selectOff()
		self.restart()

	# Curar personaje
	def cureAction (self) :
		playSound(getSoundByCamera(self.soundCure,self.character.pos))
		if self.type == 'potion' :
			if self.character.shield+self.lifeAdded <= self.character.maxShield : self.character.shield+=self.lifeAdded
			else : self.character.shield=self.character.maxShield
		if self.type == 'drug' :
			if self.character.life+self.lifeAdded <= self.character.maxLife : self.character.life+=self.lifeAdded
			else : self.character.life=self.character.maxLife
		self.magazine-=1
		self.restart()

	# Curar
	def action (self) :
		if self.type == 'potion' and self.character.shield >= self.character.maxShield : return
		elif self.type == 'drug' and self.character.life >= self.character.maxLife : return
		if self.magazine > 0 :
			if self.cureTime <= 0 : self.cureTime=self.cure; self.animationActionTime=self.sumAnimationAction; playSound(getSoundByCamera(self.soundAction,self.character.getPos()),loop=-1)
			self.cureTime-=1
			if self.cureTime <= 0 : self.cureAction()

	# Cancelar cura
	def cancelAction (self) : self.restart()
	# Reiniciar
	def restart (self) : super().restart(); self.cureTime=0; self.animationActionTime=0; stopSound(self.soundAction)
	def pause (self,pause) :
		if pause :
			stopSound(self.soundAction)
		else :
			if self.cureTime > 0 : playSound(getSoundByCamera(self.soundAction,self.character.getPos()),loop=-1)
	# Fin del armamento
	def endArmory (self) : super().endArmory(); self.restart()

	def addBubble (self) :
		bubble=copy.copy(self.bubble)
		bubble.setPos(getPosByStatus(self.character.pos,self.character.direction,self.imgStatus))
		bubble.setDirection(self.character.direction+random.randint(-45,45))
		addList(bubble)

	def loopAnimactionBubble (self) :
		if (self.sumAnimationAction-self.animationActionTime) % self.timeRangeBubble == 0 and self.animationActionTime > 0 : self.addBubble()

	# Bucle de la animacion
	def loopAnimationAction (self) :
		if self.cureTime > 0 :
			self.animationActionTime-=1
			s=0
			for i in range(len(self.animationAction)) :
				s+=self.animationAction[i]
				if self.animationActionTime < s :
					self.hlAnimation,self.hrAnimation,self.imAnimation=self.leftHandAnimationAction[i],self.rightHandAnimationAction[i],self.imgAnimationAction[i]
					break
			if self.animationActionTime <= 0 : self.animationActionTime=self.sumAnimationAction
		else :
			self.hlAnimation,self.hrAnimation,self.imAnimation=None,None,None

	# Actualizar
	def update (self) :
		self.loopAnimationAction()
		self.loopAnimactionBubble()
		if self.magazine <= 0 : self.delArmory(self)

	# Dibujar
	def draw (self,window) :
		super().draw(window,self.hlAnimation,self.hrAnimation)
		imgStatus=self.imgStatus
		if self.imAnimation : imgStatus=self.imAnimation
		img,self.rect=getImageByStatus(self.character.pos,self.character.direction,self.image,imgStatus)
		window.blit(img,self.rect)

class ArmoryBomb (Armory) :

	# Constructor
	def __init__ (self,character,arm) :
		super().__init__(character,arm)
		bomb=ARMORY[arm]['bomb']
		self.image=scaleImage(getImage(bomb['image']),bomb['dim'])
		self.rect=self.image.get_rect()
		self.imgStatus=bomb['img_status']
		self.type=bomb['type']
		self.setMagazine(self.getCapacity())
		self.cadence,self.cadenceTime=bomb['cadence'],0
		self.throw,self.timeThrow=0.75*FRAMES,0
		self.maxForce=30
		self.explosive=None
		if self.type == 'grenade' : self.explosive=Grenade(arm)
		elif self.type == 'sticky' : self.explosive=StickyBomb(arm)
		elif self.type == 'electricGrenade' : self.explosive=ElectricGrenade(arm)

	def restart (self) :
		super().restart();
		self.cadenceTime=self.cadence
		self.timeThrow=0

	def selectOff (self) :
		super().selectOff();
		self.restart();

	def endArmory (self) : super().endArmory(); self.restart();

	def shot (self,force) :
		expl=copy.copy(self.explosive)
		expl.shot(self.character,getPosByStatus(self.character.pos,self.character.direction,self.imgStatus),self.character.direction,self.character.direction+self.imgStatus[2],force)
		addList(expl)
		self.cadenceTime=self.cadence
		self.timeThrow=0
		self.magazine-=1

	def cancelAction (self) :
		playSound(getSoundByCamera(self.soundAction,self.character.pos))
		self.shot(self.timeThrow*self.maxForce/self.throw)

	def action (self) :
		if self.cadenceTime > 0 : return
		if self.magazine > 0 :
			if self.timeThrow < self.throw : self.timeThrow+=1

	def loopCadence (self) :
		if self.cadenceTime > 0 : self.cadenceTime-=1

	def update (self) :
		super().update()
		self.loopCadence()
		if self.magazine <= 0 : self.delArmory(self)

	def draw (self,window) :
		super().draw(window)
		if self.cadenceTime > 0 : return
		img,rect=getImageByStatus(self.character.pos,self.character.direction,self.image,self.imgStatus)
		window.blit(img,rect)

class ArmoryMaterial (Armory) :

	def __init__ (self,character,arm) :
		super().__init__(character,arm)
		armory=ARMORY[arm]['material']
		self.magazine=self.capacity

class ArmoryBuilding (Armory) :

	def __init__ (self,character,arm) :
		super().__init__(character,arm)
		armory=ARMORY[arm]['building']
		self.image=scaleImage(getImage(armory['image']),armory['dim'])
		self.rect=self.image.get_rect()
		self.imgStatus=armory['img_status']
		self.building=LISTBUILDINGS[armory['building']]
		self.magazine=self.capacity
		self.cadence,self.cadenceTime=0.3*FRAMES,0

	def restart (self) : self.cadenceTime=self.cadence
	def selectOff (self) : super().selectOff(); self.restart()
	def endArmory (self) : super().endArmory(); self.restart()

	def cancelAction (self) :
		if self.cadenceTime <= 0 and self.magazine > 0 :
			playSound(self.soundAction)
			build=copy.copy(self.building)
			build.setPos(self.character.getPos())
			addList(build)
			self.magazine-=1
			self.cadenceTime=self.cadence

	def loopCadence (self) :
		if self.cadenceTime > 0 : self.cadenceTime-=1

	def update (self) :
		self.loopCadence()
		if self.magazine <= 0 : self.delArmory(self)

	def draw (self,window) :
		super().draw(window)
		if self.cadenceTime > 0 : return
		img,self.rect=getImageByStatus(self.character.getPos(),self.character.getDirection(),self.image,self.imgStatus)
		window.blit(img,self.rect)

class ArmoryWeapon (Armory) :

	# Constructor
	def __init__ (self,character,arm) :
		super().__init__(character,arm)
		armory=ARMORY[arm]['weapon']
		self.image=scaleImage(getImage(armory['image']),armory['dim'])
		self.rect=self.image.get_rect()
		self.imgStatus=armory['img_status']
		self.type=armory['type']
		self.nameBullet=armory['bullet']
		self.munition=BULLETS[self.nameBullet]['munition']
		self.cadence,self.cadenceTime=armory['cadence'],armory['cadence']
		self.reload,self.reloadTime=armory['reload'],0
		self.speedBullet,self.lonBullet,self.hurtBullet=armory['speed_bullet'],armory['lon_bullet'],armory['hurt_bullet']
		self.nBullets,self.rangeBullets=armory['n_bullets'],armory['range_bullets']
		self.shotStatus=armory['shot_status']
		if BULLETS[self.nameBullet]['type'] == 'explosion' :
			self.bullet=ExplosionBullet(self.nameBullet,self.speedBullet,self.hurtBullet,self.lonBullet,radiusExplosion=armory['radius_explosion'],hurtExplosion=armory['hurt_explosion'])
		elif BULLETS[self.nameBullet]['type'] == 'ray' :
			self.bullet=RayBullet(self.nameBullet,self.speedBullet,self.hurtBullet,self.lonBullet,hurtRay=armory['hurt_ray'],rayTime=armory['ray_time'],nRay=armory['n_ray'])
		else :
			self.bullet=Bullet(self.nameBullet,self.speedBullet,self.hurtBullet,self.lonBullet)
		self.fire=scaleImage(getImage(armory['fire']),armory['fire_dim'])
		self.fireAnimation,self.fireAnimationTime=armory['fire_animation'],0
		self.fireStatus=armory['fire_status']
		self.soundReload=getSound(armory['sound_reload'])

	# Acciones al dejar de ser seleccionado el armamento
	def selectOff (self) :
		super().selectOff()
		self.restart()

	# Reiniciar
	def restart (self) :
		self.reloadTime=0
		self.cadenceTime=self.cadence
		if self.fire : self.fireAnimationTime=0
		stopSound(self.soundReload)

	def pause (self,pause) :
		if pause :
			stopSound(self.soundReload)
		else :
			if self.reloadTime > 0 : playSound(getSoundByCamera(self.soundReload,self.character.getPos()),loop=-1)

	# Fin del armamento
	def endArmory (self) : super().endArmory(); self.restart()

	# Disparar
	def action (self) :
		if self.reloadTime <= 0 and self.magazine > 0 and self.cadenceTime <= 0 :
			for i in range(self.nBullets) :
				rang=random.randint(self.rangeBullets[0],self.rangeBullets[1])
				bull=copy.copy(self.bullet)
				bull.shot(self.character,getPosByStatus(self.character.pos,self.character.direction,self.shotStatus),self.character.direction+self.shotStatus[2]+rang)
				addList(bull)
			self.magazine-=1
			self.cadenceTime=self.cadence
			playSound(getSoundByCamera(self.soundAction,getPosByStatus(self.character.pos,self.character.direction,self.shotStatus)))
			if self.fire : self.fireAnimationTime=self.fireAnimation

	# Iniciar recarga
	def initReload (self) :
		if self.magazine < self.capacity and self.character.listMunition[self.munition] >= BULLETS[self.nameBullet]['price'] and self.reloadTime <= 0 :
			self.reloadTime=self.reload
			playSound(getSoundByCamera(self.soundReload,self.character.pos),loop=-1)

	# Recargar cargador
	def reloadMagazine (self) :
		for i in range(self.capacity-self.magazine) :
			if self.character.listMunition[self.munition] >= BULLETS[self.nameBullet]['price'] :
				self.magazine+=1
				self.character.listMunition[self.munition]-=BULLETS[self.nameBullet]['price']

	# Bucle de la recarga
	def loopReload (self) :
		if self.magazine <= 0 :
			self.initReload()
		if self.reloadTime > 0 :
			self.reloadTime-=1
			if self.reloadTime == 0 : self.reloadMagazine(); self.restart()
		if self.reload <= 0 and self.magazine <= 0 : self.reloadMagazine()

	# Bucle de la cadencia
	def loopCadence (self) :
		if self.cadenceTime > 0 : self.cadenceTime-=1

	# Bucle de la animación
	def loopAnimation (self) :
		if self.fire :
			if self.fireAnimationTime > 0 : self.fireAnimationTime-=1

	# Actualizar
	def update (self) :
		super().update()
		self.loopReload()
		self.loopCadence()
		self.loopAnimation()

	# Dibujar
	def draw (self,window) :
		super().draw(window)
		# Animacion Fuego
		if self.fire :
			if self.fireAnimationTime > 0 :
				imgFire,rectFire=getImageByStatus(self.character.pos,self.character.direction,self.fire,self.fireStatus)
				window.blit(imgFire,rectFire)
		# Arma
		img,self.rect=getImageByStatus(self.character.pos,self.character.direction,self.image,self.imgStatus)
		window.blit(img,self.rect)

# Obstaculos
#-----------------------------------------------------------------------------------------------------------------------

class Box (Object) :

	dim=(75,75)

	def __init__ (self,box,pos=[0,0],direction=0) :
		box=BOXES[box]
		super().__init__(scaleImage(getImage(box['image']),self.dim),TypeObjects.OBJECTS.name,list(pos),direction)
		self.maxLife,self.life=box['life'],box['life']
		self.reward_armory,self.reward_bullets,self.reward_materials=box['reward_armory'],box['reward_bullets'],box['reward_materials']
		self.soundWound=getSound(box['sound_wound'])
		self.animation=0
		self.direction_animation=(5,-5)
		self.time_animation=(3,3)
		self.sum_animation=sum(self.time_animation)
		self.item=Item('',0)
		self.reward=Reward()

	def makeReward (self) :
		rewards=[]
		for i in [(list(ARMORY),self.reward_armory),(list(MUNITION),self.reward_bullets)] :
			for j in range(i[1]) :
				item=None
				while True :
					rand=random.choice(i[0])
					item=copy.copy(self.item)
					item.setName(rand)
					if item.getItem() : break
				item.initLot()
				radius,angle=random.randint(0,175),random.randint(0,360)
				rew=copy.copy(self.reward)
				rew.loadReward(copy.copy(item),getPosByStatus(self.pos,0,(radius,angle,0)))
				addList(rew)

	def wound (self,hurt) :
		if self.animation <= 0 : self.animation=self.sum_animation; stopSound(self.soundWound); playSound(getSoundByCamera(self.soundWound,self.pos))
		self.life-=hurt
		if self.life <= 0 : self.life=0; self.kill() 
	def kill (self) : super().kill(); delList(self); self.makeReward()

	def loopAnimation (self) :
		if self.animation > 0 :
			self.animation-=1
			summ=0
			for i in range(len(self.time_animation)) :
				summ+=self.time_animation[i]
				if self.time_animation[i]-self.animation < summ : self.direction=self.direction_animation[i]; break
		else : self.direction=0

	def setPos (self,pos) : self.pos=list(pos)
	def setDirection (self,direction) : self.direction=direction

	def update (self) : self.loopAnimation()

	def draw (self,window) : super().draw(window)

class Nature (Object) :

	def __init__ (self,nature,pos=[0,0],direction=0) :
		nature=NATURE[nature]
		super().__init__(scaleImage(getImage(nature['image']),nature['dim']),TypeObjects.OBJECTS.name,list(pos),direction)
		self.maxLife,self.life=nature['life'],nature['life']
		self.materials=nature['materials']
		self.soundWound=getSound(nature['sound_wound'])
		self.reward=Reward()
		self.item=Item('',0)
		self.animation=0
		self.pos_animation=((-5,0),(5,0))
		self.time_animation=(5,5)
		self.sum_animation=sum(self.time_animation)
		self.dpos=None

	def wound (self,hurt) :
		if self.animation <= 0 : self.animation=self.sum_animation; stopSound(self.soundWound); playSound(getSoundByCamera(self.soundWound,self.pos))
		self.life-=hurt
		if self.life <= 0 : self.kill()
	def kill (self) : super().kill(); delList(self); self.makeReward()

	def makeReward (self) :
		for material in list(self.materials) :
			for i in range(self.materials[material]) :
				radius=random.randint(0,self.rect.width)
				angle=random.randint(0,360)
				item=copy.copy(self.item)
				item.setName(material)
				if not item.getItem() : continue
				item.initLot()
				rew=copy.copy(self.reward)
				rew.loadReward(item,getPosByStatus(self.pos,0,(radius,angle,0)))
				addList(rew)

	def loopAnimation (self) :
		if self.animation > 0 :
			self.animation-=1
			summ=0
			for i in range(len(self.time_animation)) :
				summ+=self.time_animation[i]
				if self.sum_animation-self.animation < summ : self.dpos=self.pos_animation[i]; break
		else : self.dpos=None

	def update (self) : self.loopAnimation()

	def draw (self,window) :
		aux=copy.copy(self.pos)
		if self.dpos :
			self.pos[0]+=self.dpos[0]
			self.pos[1]+=self.dpos[1]
		super().draw(window)
		self.pos=copy.copy(aux)

class Gasoline (Object) :

	# Constructor
	def __init__ (self,pos=[0,0],direction=0,dim=(80,80),maxLife=400,radius=120,hurt=25, nReward=3) :
		super().__init__(scaleImage(getImage('gasoline'),dim),TypeObjects.OBJECTS.name,list(pos),direction)
		self.maxLife,self.life=maxLife,maxLife
		self.nReward=nReward
		self.reward=Reward()
		self.item=Item(ENERGY,0)
		self.item.initLot()
		self.soundWound=getSound('metal0')
		self.explosion=Explosion(radius,hurt)
		self.animation=0
		self.pos_animation=((-5,0),(5,0))
		self.time_animation=(5,5)
		self.sum_animation=sum(self.time_animation)
		self.dpos=None

	def wound (self,hurt) :
		if self.animation <= 0 : self.animation=self.sum_animation; stopSound(self.soundWound); playSound(getSoundByCamera(self.soundWound,self.pos))
		self.life-=hurt
		if self.life <= 0 : self.life=0; self.kill()
	def kill (self) : super().kill(); delList(self); self.action(); self.makeReward()

	def action (self) :
		expl=copy.copy(self.explosion)
		expl.action(None,self.pos)
		addList(expl)

	def makeReward (self) :
		nReward=random.randint(0,self.nReward)
		for i in range(nReward) :
			rew=copy.copy(self.reward)
			status=random.randint(0,min(*self.getDim())),random.randint(0,360),0
			rew.loadReward(copy.copy(self.item),getPosByStatus(self.pos,0,status))
			addList(rew)

	def loopAnimation (self) :
		if self.animation > 0 :
			self.animation-=1
			summ=0
			for i in range(len(self.time_animation)) :
				summ+=self.time_animation[i]
				if self.sum_animation-self.animation < summ : self.dpos=self.pos_animation[i]; break
		else : self.dpos=None

	def update (self) : super().update(); self.loopAnimation()

	def draw (self,window) :
		aux=copy.copy(self.pos)
		if self.dpos :
			self.pos[0]+=self.dpos[0]
			self.pos[1]+=self.dpos[1]
		super().draw(window)
		self.pos=copy.copy(aux)

class ElectricBox (Object) :
	

	def __init__ (self,pos=[0,0],direction=0,dim=(80,80),maxLife=500,radius=180,hurtRay=15,rayTime=0.1*FRAMES,nRay=20,nReward=3) :
		super().__init__(scaleImage(getImage('electricbox'),dim),TypeObjects.OBJECTS.name,list(pos),direction)
		self.maxLife,self.life=maxLife,maxLife
		self.radius=radius
		self.nReward=nReward
		self.soundWound=getSound('metal0')
		self.ray=Ray(hurtRay,rayTime,nRay)
		self.animationRay=AnimationRay(0.1*FRAMES,5)
		self.animation=0
		self.pos_animation=((-5,0),(5,0))
		self.time_animation=(5,5)
		self.sum_animation=sum(self.time_animation)
		self.dpos=None
		self.counter=0
		self.reward=Reward()
		self.item=Item(ENERGY,0)
		self.item.initLot()

	def wound (self,hurt) :
		if self.animation <= 0 : self.animation=self.sum_animation; stopSound(self.soundWound); playSound(getSoundByCamera(self.soundWound,self.pos))
		self.life-=hurt
		if self.life <= 0 : self.life=0; self.kill()

	def action (self) :
		objects=objectInRadiusAttack(self.pos,self.radius)
		for obj in objects :
			if obj == self : continue
			r=copy.copy(self.ray)
			r.action(None,obj)
			addList(r)
		if len(objects) <= 0 :
			ar=copy.copy(self.animationRay)
			ar.action(self.pos,self.radius)
			addList(ar)

	def makeReward (self) :
		nReward=random.randint(0,self.nReward)
		for i in range(nReward) :
			rew=copy.copy(self.reward)
			status=random.randint(0,min(*self.getDim())),random.randint(0,360),0
			rew.loadReward(copy.copy(self.item),getPosByStatus(self.pos,0,status))
			addList(rew)

	def loopAnimation (self) :
		if self.animation > 0 :
			self.animation-=1
			summ=0
			for i in range(len(self.time_animation)) :
				summ+=self.time_animation[i]
				if self.sum_animation-self.animation < summ : self.dpos=self.pos_animation[i]; break
		else : self.dpos=None

	def update (self) : self.counter+=1; super().update(); self.loopAnimation()

	def kill (self) : super().kill(); delList(self); self.action(); self.makeReward()

	def draw (self,window) :
		aux=copy.copy(self.pos)
		if self.dpos :
			self.pos[0]+=self.dpos[0]
			self.pos[1]+=self.dpos[1]
		super().draw(window)
		self.pos=copy.copy(aux)
		if int(self.counter/20) % 2 == 0 and self.life < self.maxLife : pygame.draw.circle(window,(69, 255, 204 ),getPosWindow(self.pos),self.radius,2)

# Objetos auxiliares
#-----------------------------------------------------------------------------------------------------------------------

class ObjectAux (Object) :

	def __init__ (self,image,group=TypeObjects.LAYERTOP.name,pos=[0,0],direction=0) :
		super().__init__(image,group,list(pos),direction)
	def kill (self) : super().kill(); delList(self)
	def update (self) : super().update()
	def draw (self,window) : super().draw(window)

class EfectObject (ObjectAux) :

	def __init__ (self,resource,dim,vel,maxLon,pos=[0,0],direction=0) :
		super().__init__(scaleImage(getImage(resource),dim),TypeObjects.LAYERTOP.name,list(pos),direction)
		self.vel,self.maxLon,self.lon=vel,maxLon,0
		self.direction=direction

	def setPos (self,pos) : self.pos=list(pos)
	def setDirection (self,direction) : self.direction=direction

	def update (self) :
		super().update()
		self.pos[0]+=self.vel*math.cos(angleToPolar(self.direction))
		self.pos[1]-=self.vel*math.sin(angleToPolar(self.direction))
		self.lon+=self.vel
		if self.lon > self.maxLon : self.kill()

	def draw (self,window) : super().draw(window)

class AnimationRay (ObjectAux) :

	def __init__ (self,rayTime=0.1*FRAMES,nRay=5,radius=0,originPos=[0,0],pos=[0,0],direction=0) :
		self.IMAGE=getImage('ray')
		super().__init__(self.IMAGE,pos=list(pos),direction=0)
		self.originPos=originPos
		self.rayTime,self.counterTime=rayTime,0
		self.nRay,self.counterRay=nRay,0
		self.radius=radius
		self.soundAction=getSound('')
		self.rangeDim=[20,50]
		self.rad,self.angle=0,0
		self.soundAction=getSound('buzz0')

	def action (self,originPos,radius=None) :
		self.originPos=originPos
		if radius : self.radius=radius
		self.rangeDim[0]=round(self.radius/6)
		self.rangeDim[1]=round(self.radius/2)

	def loopRay (self) :
		if self.counterTime <= 0 :
			self.counterRay+=1
			if self.counterRay > self.nRay : self.kill(); return
			self.rad=random.randint(0,self.radius)
			self.angle=random.randint(0,360)
			self.direction=random.randint(-60,60)
			dim=random.randint(self.rangeDim[0],self.rangeDim[1])
			self.image=scaleImage(self.IMAGE,(dim,dim))
			stopSound(self.soundAction)
			playSound(getSoundByCamera(self.soundAction,self.originPos))
		self.counterTime+=1
		if self.counterTime >= self.rayTime : self.counterTime=0

	def update (self) : self.loopRay()

	def draw (self,window) :
		self.pos=getPosByStatus(self.originPos,0,(self.rad,self.angle,self.direction))
		super().draw(window)

# Construcciones
#-----------------------------------------------------------------------------------------------------------------------

class Building (Object) :

	def __init__ (self,building,pos=[0,0],direction=0) :
		building=BUILDINGS[building]['building']
		super().__init__(scaleImage(getImage(building['image']),building['dim']),TypeObjects.BUILDINGS.name,list(pos),direction)
		self.function=building['function']
		self.maxLife,self.life=building['life'],building['life']
		self.soundWound=getSound(building['sound_wound'])
		self.window=None
		self.animation=0
		self.pos_animation=((-5,0),(5,0))
		self.time_animation=(5,5)
		self.sum_animation=sum(self.time_animation)
		self.dpos=None

	def openWindow (self,*args,**kwargs) :
		if self.window : self.window.openWindow(*args,**kwargs)
	def closeWindow (self,*args,**kwargs) :
		if self.window : self.window.closeWindow(*args,**kwargs)

	def getLife (self) : return self.life
	def setLife (self,life) : self.life=life
	def getMaxLife (self) : return self.maxLife
	def setMaxLife (self,maxLife) : self.maxLife=maxLife

	def wound (self,hurt) :
		if self.animation <= 0 : self.animation=self.sum_animation
		super().wound(hurt)
		stopSound(self.soundWound)
		playSound(getSoundByCamera(self.soundWound,self.pos))
		if self.life > 0 :
			self.life-=hurt
			if self.life <=0 : self.life=0; self.kill()
	def kill (self) : super().kill(); delList(self)

	def loopAnimation (self) :
		if self.animation > 0 :
			self.animation-=1
			summ=0
			for i in range(len(self.time_animation)) :
				summ+=self.time_animation[i]
				if self.sum_animation-self.animation < summ : self.dpos=self.pos_animation[i]; break
		else : self.dpos=None

	def update (self) : self.loopAnimation()

	def draw (self,window) :
		aux=copy.copy(self.pos)
		if self.dpos :
			self.pos[0]+=self.dpos[0]
			self.pos[1]+=self.dpos[1]
		super().draw(window)
		self.pos=copy.copy(aux)

class TownHall (Building) :

	def __init__ (self,building,pos=[WIDTH_FIELD/2,HEIGHT_FIELD/2]) :
		super().__init__(building,pos)
		self.direction_animation=(2,-2)
		self.time_animation=(10,10)

class Trunk (Building) :

	CAPACITY=16

	def __init__ (self,building,pos=[0,0]) :
		super().__init__(building,pos)
		self.listItems={}
		self.clear()
		self.window=WindowTrunk(self)
		self.reward=Reward()

	def makeReward (self,item,pos=None) :
		if pos == None :
			radius=random.randint(0,max(*self.getDim())+20)
			angle=random.randint(0,360)
			pos=getPosByStatus(self.getPos(),0,(radius,angle,0))
		rew=copy.copy(self.reward)
		rew.loadReward(item,pos)
		addList(rew)

	def kill (self) :
		super().kill()
		for i in list(self.listItems) :
			if self.listItems[i] != None : self.makeReward(self.getItem(i))
		if self.window in objectsGroups[TypeObjects.INTERFACES.name] : closeInterface()

	def clear (self) :
		for i in range(self.CAPACITY) : self.listItems[i]=None

	def addItem (self,item,box=None) :
		if box == None :
			for i in list(self.listItems) :
				item=self.listItems[i]
				if item == None : box=i; break
		if box in self.listItems : self.listItems[box]=item
	def delItem (self,box) : self.addItem(None,box)
	def getItem (self,box) :
		if box in self.listItems : return self.listItems[box]
		return None

# Objetos
#-----------------------------------------------------------------------------------------------------------------------

class Field :

	def __init__ (self,skin) :
		global WIDTH_FIELD,HEIGHT_FIELD
		WIDTH_FIELD,HEIGHT_FIELD = FIELDS[skin]['dim']
		self.image=scaleImage(getImage(FIELDS[skin]['image']),(WIDTH_FIELD,HEIGHT_FIELD))
		self.rect=self.image.get_rect()

	def events (self,pyevents) : pass
	def update (self) : self.rect.left,self.rect.top=getPosWindow([0,0])
	def draw (self,window) : window.blit(self.image,self.rect)

class Character (Object) :

	dim=(75,75)

	# Constructor
	def __init__ (self,group,skin,pos=[0,0],direction=0) :
		character=None
		if group == TypeObjects.PLAYERS.name : character=PLAYERS[skin]
		if group == TypeObjects.ZOMBIES.name : character=ZOMBIES[skin]
		super().__init__(scaleImage(getImage(character['image']),self.dim),group,list(pos),direction)
		self.hand=scaleImage(getImage(character['hand']),(30,30))
		self.speed=character['speed']
		self.maxLife,self.life=character['life'],character['life']
		self.maxShield,self.shield=character['shield'],0
		self.hurt=character['hurt']
		self.enemy=copy.copy(character['enemy'])
		self.energyMax=0
		self.speedEnergy=0.01
		if ENERGY in character : self.energyMax=character[ENERGY]
		self.reward=Reward()
		self.item=Item('',0)
		self.soundKill=getSound(character['sound_kill'])
		self.soundWound=getSound(character['sound_wound'])
		self.soundReward=getSound('get_reward')

		self.listMunition={}
		self.listArmory={}
		self.listInventory={}

		for i in list(MUNITION) : self.listMunition[i]=MUNITION[i]['item']['lot']
		for i in range(6) : self.listArmory[i]=None
		for i in range(12) : self.listInventory[i]=None
		self.listMunition[ENERGY]=self.energyMax
		self.nArmory=0

		self.buzzTime,self.counterBuzz=15,0
		self.force,self.strength=[0,0],1

		self.p_move=True
		self.p_rotate=True
		self.p_action=True
		self.p_armory=True
		self.p_update=True

	def getReward (self,reward) :
		item=reward.getItem()
		code=getDictCode(item.getName())
		aux=False
		if code == 'ARMORY' :
			if item.getMaxLot() != None :
				for dictt in [self.listArmory,self.listInventory] :
					for i in list(dictt) :
						armory=dictt[i]
						if armory == None : continue
						if armory.getName() == item.getName() :
							inc=0
							if dictt == self.listArmory : inc=min(item.getLot(),item.getMaxLot()-armory.getMagazine()); armory.setMagazine(armory.getMagazine()+inc)
							elif dictt == self.listInventory : inc=min(item.getLot(),item.getMaxLot()-armory.getLot()); armory.setLot(armory.getLot()+inc)
							item.setLot(item.getLot()-inc)
							if inc > 0 : aux=True
				if item.getLot() <= 0 : reward.kill()
				else :
					enc=False
					for dictt in [self.listArmory,self.listInventory] :
						for i in list(dictt) :
							armory=dictt[i]
							if armory == None : self.setItem(item,dictt,i); reward.kill(); aux=True; enc=True; break
						if enc : break
			else :
				enc=False
				for dictt in [self.listArmory,self.listInventory] :
					for i in list(dictt) :
						armory=dictt[i]
						if armory == None : self.setItem(item,dictt,i); reward.kill(); aux=True; enc=True; break
					if enc : break
		elif code == 'MUNITION' : item.setLot(item.getLot()+self.getMunition(item.getName())); self.setItem(item,self.getListMunition(),item.getName()); reward.kill(); aux=True
		if aux : playSound(getSoundByCamera(self.soundReward,self.getPos()))

	def setReward (self,armory=None,shift=True) :
		if armory == None : armory=self.nArmory # Numero de la casilla del armamento
		radius=130
		pos=(self.pos[0]+radius*math.cos(angleToPolar(self.direction)),self.pos[1]-radius*math.sin(angleToPolar(self.direction)))
		reward=self.makeReward(armory,pos)
		if reward != None :
			addList(reward)
			self.delArmory(armory,shift)

	def makeReward (self,armory,pos=(0,0)) :
		item=self.getItem(self.getListArmory(),armory)
		if item != None :
			if item.getItem() :
				rew=copy.copy(self.reward)
				rew.loadReward(copy.copy(item),pos)
				return rew
		return None

	def delArmory (self,armory,shift=True) :
		self.getArmory(armory).endArmory()
		self.setArmory(armory,None)
		if shift : self.shiftArmory()
		if not self.getArmory() : self.changeArmory(self.nArmory-1)
		else : self.changeArmory(self.nArmory)

	def addArmory (self,arm,position=None) :
		if position == None :
			for i in list(self.listArmory) :
				if not self.listArmory[i] : position=i; break
		if position in self.listArmory :
			armory=makeArmory(arm)
			if armory : armory.setCharacter(self)
			self.setArmory(position,armory)

	def getItem (self,dictt,name) :
		if dictt[name] == None : return None
		item=copy.copy(self.item)
		if dictt == self.listArmory : item=copy.copy(self.getArmory(name).getItem())
		elif dictt == self.listInventory : item=copy.copy(self.getItemInventory(name))
		elif dictt == self.listMunition : item.setName(name); item.setLot(self.getMunition(name))
		return item

	def setItem (self,item,dictt,name) :
		if dictt == self.listArmory :
			if item == None : self.setArmory(name,None); return
			armory=makeArmory(item.getName())
			armory.setCharacter(self)
			armory.setMagazine(item.getLot())
			self.setArmory(name,armory)
		elif dictt == self.listInventory : self.setItemInventory(item,box=name)
		elif dictt == self.listMunition : self.setMunition(name,item.getLot())

	def swapArmory (self) :
		for reward in objectsGroups[TypeObjects.REWARDS.name] :
			if collisionSprite(self,reward) : aux=self.nArmory; self.setReward(shift=False); self.getReward(reward); self.changeArmory(aux)

	def getItemInventory (self,box) :
		if not box in self.getListInventory() : return
		return self.getListInventory()[box]

	def setItemInventory (self,value,box=None) :
		if box == None :
			for i in list(self.listInventory) :
				if self.listInventory[i] == None : box=i; break
		if not box in self.getListInventory(): return
		self.listInventory[box]=value

	# Cambair la selección del armamento
	def changeArmory (self,newArmory) :
		if newArmory == self.getActualArmory() : return
		if self.getArmory() : self.getArmory().selectOff()
		self.setActualArmory(newArmory)
		self.getArmory().selectOn()

	def getActualArmory (self) : return self.nArmory
	def setActualArmory (self,armory) : self.nArmory=armory
	def getArmory (self,armory=None) :
		if armory == None : armory=self.getActualArmory()
		if not armory in self.listArmory : return None
		return self.listArmory[armory]
	def getListArmory(self) : return self.listArmory
	def getListInventory(self) : return self.listInventory
	def getListMunition (self) : return self.listMunition
	def shiftArmory (self) : self.listArmory=shiftLeftDict(self.listArmory)
	def setArmory (self,armory,value) :
		if armory in self.listArmory : self.listArmory[armory]=value
	def getMunition (self,munition) :
		if not munition in self.listMunition : return None
		return self.listMunition[munition]
	def setMunition (self,munition,value) :
		if munition in self.listMunition : self.listMunition[munition]=value

	def getEnergy (self) : return self.getMunition(ENERGY)
	def setEnergy (self,energy) : self.listMunition[ENERGY]=energy 
	def getLife (self) : return self.life
	def setLife (self,life) : self.life=life
	def getMaxLife (self) : return self.maxLife
	def setMaxLife (self,maxLife) : self.maxLife=maxLife
	def getShield (self) : return self.shield
	def setShield (self,shield) : self.shield=shield
	def getMaxShield (self) : return self.maxShield
	def setMaxShield (self,maxShield) : self.maxShield=maxShield

	def kill (self) : super().kill(); delList(self); playSound(getSoundByCamera(self.soundKill,self.pos)); self.getArmory().kill()
	
	def wound (self,hurt) :
		super().wound(hurt)
		stopSound(self.soundWound)
		playSound(getSoundByCamera(self.soundWound,self.pos))
		if self.shield > 0 :
			if hurt <= self.shield : self.shield-=hurt; return
			else : hurt-=self.shield; self.shield=0;
		if self.life > hurt : self.life-=hurt
		else : self.life=0; self.kill()

	def buzz (self) :
		super().buzz()
		self.counterBuzz=self.buzzTime
		self.getArmory().restart()

	def loopBuzz (self) :
		if self.counterBuzz > 0 :
			self.counterBuzz-=1
			self.p_move=False
			self.p_rotate=False
			self.p_action=False
			self.p_armory=False

	# Explotar bombas adesivas
	def explosionStickyBombs (self) :
		aux=True
		while aux :
			aux=False
			for obj in objectsGroups[TypeObjects.BULLETS.name] :
				if obj.type == 'sticky' :
					if obj.character == self : aux=True; obj.kill(); break

	def restart (self) :
		armory=self.getArmory()
		if armory : armory.restart()

	def pause (self,pause) : self.getArmory().pause(pause)

	# Bucle de recompensas
	def loopRewards (self) :
		for reward in objectsGroups[TypeObjects.REWARDS.name] :
			if collisionSprite(self,reward) : self.getReward(reward)

	# Bucle de la energía
	def loopEnergy (self) :
		if self.getEnergy() > self.energyMax : self.setEnergy(self.energyMax)
		if self.getEnergy() < self.energyMax : self.setEnergy(self.getEnergy()+self.speedEnergy)

	# Actualizar
	def update (self) :
		super().update()
		if self.life > self.maxLife : self.life=self.maxLife
		if self.shield > self.maxShield : self.shield=self.maxShield
		if self.p_armory : self.getArmory().update()
		self.p_armory=True
		self.loopEnergy()
		self.loopBuzz()
		self.loopRewards()

	# Dibujar
	def draw (self,window) :
		if self.getArmory() == None : self.setActualArmory(0)
		self.getArmory().draw(window)
		super().draw(window)

class Player (Character) :

	# Constructor
	def __init__ (self,skin,pos=[0,0],direction=0) :
		super().__init__(TypeObjects.PLAYERS.name,skin,pos,direction)
		self.addArmory('hands')
		self.windowInventory=WindowInventory()

		self.addArmory('EscopetaJTJ')
		self.addArmory('SubfusilUTP')
		self.addArmory('MisilesHJH')
		self.addArmory('TaserNBV')
		self.addArmory('trunk')

	# Mover
	def move (self) :
		keys=pygame.key.get_pressed()
		dx,dy=0,0
		if keys[PYKEYS['a']] or keys[PYKEYS['LEFT']] : dx-=1
		if keys[PYKEYS['d']] or keys[PYKEYS['RIGHT']] : dx+=1
		if keys[PYKEYS['w']] or keys[PYKEYS['UP']] : dy-=1
		if keys[PYKEYS['s']] or keys[PYKEYS['DOWN']] : dy+=1
		if dx != 0 and dy != 0 : dx*=math.sqrt((self.speed**2)/math.sqrt(2)); dy*=math.sqrt((self.speed**2)/math.sqrt(2))
		else : dx*=self.speed;dy*=self.speed
		if self.pos[0]+dx >= 0 and self.pos[0]+dx <= WIDTH_FIELD : self.pos[0]+=round(dx)
		if self.pos[1]+dy >= 0 and self.pos[1]+dy <= HEIGHT_FIELD : self.pos[1]+=round(dy)

	# Rotar
	def rotate (self) :
		mouse=pygame.mouse.get_pos()
		x,y=getPosWindow(self.pos)
		dx,dy=mouse[0]-x,mouse[1]-y
		radius=math.sqrt(dx**2+dy**2)
		if radius != 0 : self.direction=round(angleToDegrees(math.acos(dx/radius)))
		if dy > 0 : self.direction*=-1

	def kill (self) :
		super().kill()
		self.life=self.maxLife
		self.shield=0
		self.pos[0],self.pos[1]=WIDTH_FIELD/2,HEIGHT_FIELD/2
		addList(self)
		self.setActive(True)

	# Bucle de la acción (disparo,curar,...)
	def loopAction (self) :
		button=pygame.mouse.get_pressed()
		if button[0] and getClickInGame() :
			self.getArmory().action()
			if self.getArmory().function == 'drug' : self.p_move=False
			if self.getArmory().function == 'fists' : attack(self,self.hurt,self)

	# Bucle del cambio de selección del armamento
	def loopChangeArmory (self,pyevents) :
		newArmory=-1
		for event in pyevents :
			if event.type == pygame.KEYDOWN :
				for i in range(len(self.listArmory)) :
					if event.key == PYKEYS[str(i)] : newArmory=i
			if event.type == pygame.MOUSEBUTTONDOWN :
				if event.button == 4 :
					if self.nArmory >= len(self.listArmory)-1 : newArmory=0
					else :
						if not self.listArmory[self.nArmory+1] : newArmory=0
						else : newArmory=self.nArmory+1
				if event.button == 5 :
					if self.nArmory == 0 :
						for i in self.listArmory :
							if self.listArmory[i] : newArmory=i
							else : break
					else : newArmory=self.nArmory-1
		if newArmory >= 0 and newArmory != self.nArmory and self.listArmory[newArmory] : self.changeArmory(newArmory)

	def events (self,pyevents) :
		for event in pyevents :
			if event.type == pygame.KEYDOWN :
				if event.key == PYKEYS['q'] and self.p_update : self.setReward()
				if event.key == PYKEYS['r'] and self.p_update :
					if self.getArmory().function == 'weapon' : self.getArmory().initReload()
				if event.key == PYKEYS['e'] and self.p_update : self.swapArmory()
				if event.key == PYKEYS['g'] and self.p_update : self.explosionStickyBombs()
				if event.key == PYKEYS['e'] :
					if len(objectsGroups[TypeObjects.INTERFACES.name]) <= 0 :
						for obj in objectsGroups[TypeObjects.BUILDINGS.name] :
							if collisionSprite(self,obj) :
								self.restart()
								if not obj.window in objectsGroups[TypeObjects.INTERFACES.name]: obj.openWindow(self)
								else : closeInterface()
								break
				if event.key == PYKEYS['i'] :
					self.restart()
					if not self.windowInventory in objectsGroups[TypeObjects.INTERFACES.name] : closeInterface(); self.windowInventory.openWindow(self)
					else : closeInterface()
			if event.type == pygame.MOUSEBUTTONUP and self.p_update :
				if event.button == 1 : self.listArmory[self.nArmory].cancelAction()
		keys=pygame.key.get_pressed()
		if self.p_update : self.loopChangeArmory(pyevents)

	# Actualizar
	def update (self) :
		self.p_update=True
		if len(objectsGroups[TypeObjects.INTERFACES.name]) > 0 : self.p_update=False;
		if self.p_update :
			if self.p_rotate : self.rotate()
			self.p_rotate=True
			if self.p_move : self.move()
			self.p_move=True
			if self.p_action : self.loopAction()
			self.p_action=True
			super().update()

class Zombie (Character) :

	def __init__ (self,skin,pos=[1000,1000],direction=0) :
		character=ZOMBIES[skin]
		super().__init__(TypeObjects.ZOMBIES.name,skin,pos,direction)
		self.radiusSearch=character['radius_search']
		self.radiusShot=character['radius_shot']
		self.probabilityArmory=character['probability_armory']
		self.speed=random.uniform(3.5*self.speed/4,4.5*self.speed/4)
		self.addArmory('hands1')
		self.haveArmory()

	def expelReward (self) :
		for name in list(self.getListArmory()) :
			obj=self.listArmory[name]
			if obj == None : continue
			if random.random() > 0.4 : continue
			item=self.getItem(self.getListArmory(),name)
			if not item.getItem() : continue
			radius,angle=random.randint(0,max(*self.getDim())+20),random.randint(0,360)
			pos=getPosByStatus(self.getPos(),0,(radius,angle,0))
			rew=copy.copy(self.reward)
			rew.loadReward(item,pos)
			addList(rew)
		for i in [(self.listMunition,0.1),] :
			dictt,prob=i
			for name in list(dictt) :
				obj=dictt[name]
				if obj == None : continue
				item=self.getItem(dictt,name)
				if not item.getItem() : continue
				lot=item.getLot()
				item.initLot()
				n=int(lot/item.getLot())
				for i in range(n) :
					if random.random() > prob : continue
					radius,angle=random.randint(0,max(*self.getDim())+20),random.randint(0,360)
					pos=getPosByStatus(self.getPos(),0,(radius,angle,0))
					rew=copy.copy(self.reward)
					rew.loadReward(item,pos)
					addList(rew)

	def haveArmory (self) :
		for prob in self.probabilityArmory :
			rand=random.random()
			if rand > prob : break
			while True :
				rand=random.choice(list(ARMORY))
				if ARMORY[rand]['item']['item'] and ARMORY[rand]['armory']['function'] != 'bomb' : self.addArmory(rand); break
		for mun in list(self.listMunition) : self.listMunition[mun]=random.randint(0,5)*MUNITION[mun]['item']['lot']

	def kill (self) : super().kill(); self.expelReward(); stopSound(self.soundWound)

	def searchEnemy (self) :
		enemy=None
		lon=0
		for group in self.enemy :
			list_=objectsGroups[group]
			if len(list_) > 0 : lon=getLonPoints(self.pos,list_[0].pos); break
		for group in self.enemy :
			for obj in objectsGroups[group] :
				l=getLonPoints(self.pos,obj.pos)
				if l <= lon and l <= self.radiusSearch : lon=l; enemy=obj
		return enemy

	def loopAction (self,enemy) :
		if self.getArmory().function == 'fists' and enemy :
			if collisionSprite(self,enemy) : enemy.wound(self.hurt); self.getArmory().action(); self.p_move=False
		if self.getArmory().function == 'weapon' and enemy :
			if getLonPoints(self.pos,enemy.pos) <= self.radiusShot : self.getArmory().action(); self.p_move=False
		if self.getArmory().function == 'drug' :
			self.getArmory().action(); self.p_move=False

	def loopChangeArmory (self,enemy) :
		if enemy :
			r=None
			for armory in list(self.listArmory) :
				if self.listArmory[armory] == None : continue
				if self.listArmory[armory].function == 'weapon' : 
					if self.listMunition[self.listArmory[armory].munition] >= BULLETS[self.getArmory(armory).nameBullet]['price'] or self.listArmory[armory].magazine > 0 : r=armory; break
			if r != None :
				lon=getLonPoints(enemy.pos,self.pos)
				if lon >= self.radiusShot/3 : self.changeArmory(r)
				else : self.changeArmory(0)
			else : self.changeArmory(0)
		else :
			r=None
			for armory in list(self.listArmory) :
				if self.listArmory[armory] == None : continue
				if self.listArmory[armory].function == 'drug' : r=armory; break
			if r != None :
				if self.listArmory[r].type == 'drug' :
					if self.life < self.maxLife : self.changeArmory(r)
				if self.listArmory[r].type == 'potion' :
					if self.shield < self.maxShield : self.changeArmory(r)

	def move (self,enemy) :
		if enemy :
			self.pos[0]+=self.speed*math.cos(angleToPolar(self.direction))
			self.pos[1]-=self.speed*math.sin(angleToPolar(self.direction))

	def rotate (self,enemy) :
		if enemy :
			dx,dy=enemy.pos[0]-self.pos[0],enemy.pos[1]-self.pos[1]
			lon=getLonPoints(self.pos,enemy.pos)
			if lon != 0 :
				self.direction=angleToDegrees(math.acos(dx/lon))
				if dy > 0 : self.direction*=-1
		else : self.direction+=5

	def update (self) :
		if self.p_update :
			enemy=self.searchEnemy()
			if self.p_rotate : self.rotate(enemy)
			self.p_rotate=True
			if self.p_move : self.move(enemy)
			self.p_move=True
			if self.p_action : self.loopAction(enemy)
			self.p_action=True
			self.loopChangeArmory(enemy)
			super().update()
		self.p_update=True

	def draw (self,window) :
		super().draw(window)
		d=(3*self.dim[0]/4,7)
		if self.shield > 0 :
			pygame.draw.rect(window,(100,100,200),(round(self.rect.centerx-d[0]/21),self.rect.bottom+5,round(self.shield*d[0]/self.maxShield),d[1]))
		else :
			pygame.draw.rect(window,(200,100,100),(round(self.rect.centerx-d[0]/2),self.rect.bottom+5,round(self.life*d[0]/self.maxLife),d[1]))
	
# Otras Variables
#-----------------------------------------------------------------------------------------------------------------------

LISTARMORY = {}
LISTBUILDINGS = {}

def loadArmory () :
	for armory in ARMORY :
		function=ARMORY[armory]['armory']['function']
		if function == 'fists' : LISTARMORY[armory]=ArmoryFists(None,armory)
		elif function == 'drug' : LISTARMORY[armory]=ArmoryDrug(None,armory)
		elif function == 'bomb' : LISTARMORY[armory]=ArmoryBomb(None,armory)
		elif function == 'material' : LISTARMORY[armory]=ArmoryMaterial(None,armory)
		elif function == 'building' : LISTARMORY[armory]=ArmoryBuilding(None,armory)
		elif function == 'weapon' : LISTARMORY[armory]=ArmoryWeapon(None,armory)

def loadBuildings () :
	for building in BUILDINGS :
		function=BUILDINGS[building]['building']['function']
		if function == 'townhall' : LISTBUILDINGS[building]=TownHall(building)
		elif function == 'trunk' : LISTBUILDINGS[building]=Trunk(building)

# Función principal del juego
#-----------------------------------------------------------------------------------------------------------------------

class Game (Frame) :

	def __init__ (self) :
		super().__init__(dim=(1100,650),title='The Walking Dead',color=(50,50,50),frames=60)
		self.pauseGame=False

	def load (self) :
		self.p_click=True
		setExit(False)
		resources.load()
		loadBuildings()
		loadArmory()
		self.setCursor(scaleImage(getImage('cursor0'),(30,30)))
		self.windowPause=WindowPause()
		self.field=Field(skin=0)
		self.protagonist=Player(skin=3,pos=[WIDTH_FIELD/2,HEIGHT_FIELD/2],direction=0)
		addList(self.protagonist)
		setTarget(self.protagonist)
		self.interface=Interface(self.protagonist)
		addList(copy.copy(LISTBUILDINGS['townhall']))
		for i in range(10) : addList(Zombie(0,pos=getRandomPos()))
		for i in range(6) : addList(Zombie(1,pos=getRandomPos()))
		for i in range(10) : addList(Box(0,getRandomPos()))
		for i in range(4) : addList(Box(1,getRandomPos()))
		for i in range(2) : addList(Box(2,getRandomPos()))
		for i in range(2) : addList(Box(3,getRandomPos()))
		addList(Box(4,getRandomPos()))
		addList(Box(5,getRandomPos()))
		addList(Box(6,getRandomPos()))
		for i in range(5) : addList(Nature('stone0',getRandomPos()))
		for i in range(8) : addList(Nature('stone1',getRandomPos()))
		for i in range(5) : addList(Nature('tree1',getRandomPos()))
		for i in range(8) : addList(Nature('tree2',getRandomPos()))
		for i in range(10) : addList(Gasoline(pos=getRandomPos(),direction=random.randint(0,360)))
		for i in range(10) : addList(ElectricBox(pos=getRandomPos()))

	def restart (self) :
		for group in list(objectsGroups) :
			for obj in objectsGroups[group] : obj.restart()

	def events (self) :
		self.setCursor(self.interface.getCursor())
		if len(objectsGroups[TypeObjects.INTERFACES.name]) > 0 : self.setCursor(objectsGroups[TypeObjects.INTERFACES.name][0].getCursor())
		for event in self.getPyEvents() :
			if event.type == pygame.KEYDOWN :
				if event.key == PYKEYS['ESC'] :
					if self.pauseGame : self.windowPause.closeWindow()
					else : closeInterface(); self.windowPause.openWindow(self.protagonist)
			if event.type == pygame.MOUSEBUTTONDOWN :
				if event.button == 1 :
					if not getClickInGame() : self.p_click=False
			if event.type == pygame.MOUSEBUTTONUP :
				if event.button == 1 :
					if not getClickInGame() and not self.p_click : setClickInGame(True); self.p_click=True
		if not self.pauseGame : self.field.events(self.getPyEvents())
		for group in list(objectsGroups) :
			if not self.pauseGame or group == TypeObjects.INTERFACES.name :
				for obj in objectsGroups[group] : obj.events(self.getPyEvents())
		if not self.pauseGame : self.interface.events(self.getPyEvents())
	def update (self) :
		if getExit() : self.exit()
		if not self.pauseGame : self.field.update()
		for group in list(objectsGroups) :
			if not self.pauseGame or group == TypeObjects.INTERFACES.name :
				for obj in objectsGroups[group] : obj.update()
		if not self.pauseGame : self.interface.update()
		self.pauseGame=getPause()
		if self.pauseGame and not self.windowPause in objectsGroups[TypeObjects.INTERFACES.name] : self.windowPause.openWindow(self.protagonist)
		setCamera(target)
		if self.p_click : setClickInGame(True)
	def draw (self) :
		self.field.draw(self.getWindow())
		for group in list(objectsGroups) :
			for obj in objectsGroups[group] : obj.draw(self.getWindow())
		if len(objectsGroups[TypeObjects.INTERFACES.name]) <= 0 : self.interface.draw(self.getWindow())

# Main
#-----------------------------------------------------------------------------------------------------------------------

def main () :
	game=Game()
	game.run()

if __name__ == '__main__' :
	main()