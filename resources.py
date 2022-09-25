import pygame
from functions import *

class Resources :

	routeImages='resources/images/'
	formatImages='.png'
	routeSounds='resources/sounds/'
	formatSounds='.aiff'

	IMAGES={}
	SOUNDS={}

	def __init__ (self) :
		self.muteSound=True
		self.muteMusic=True

	def getMuteSound (self) : return self.muteSound
	def setMuteSound (self,mute) : self.muteSound=mute
	def getMuteMusic (self) : return self.muteMusic
	def setMuteMusic (self,mute) : self.muteMusic=mute

	def getImage (self,image) :
		if not image in self.IMAGES : return None
		return self.IMAGES[image]

	def getSound (self,sound) :
		if not sound in self.SOUNDS : return None
		return self.SOUNDS[sound]

	def playSound (self,sound,loop=0) :
		if self.muteSound and sound : sound.play(loop)
	def stopSound (self,sound) :
		if sound : sound.stop()

	def restart (self) :
		self.setMuteSound(True)
		self.setMuteMusic(True)
		self.clear()

	def load (self) :
		sounds=getResource(route='./'+self.routeSounds,format=self.formatSounds)
		for sound in sounds :
			self.SOUNDS[sound.split('.')[0]]=loadSound(self.routeSounds+sound)
		images=getResource(route='./'+self.routeImages,format=self.formatImages)
		for image in images :
			self.IMAGES[image.split('.')[0]]=loadImage(self.routeImages+image)

	def clear (self) :
		sounds=list(self.SOUNDS)
		images=list(self.IMAGES)
		for sound in sounds : self.SOUNDS.pop(sound)
		for image in images : self.IMAGES.pop(image)