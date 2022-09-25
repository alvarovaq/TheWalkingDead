import pygame

class Frame :

	def __init__ (self,dim=(100,100),title="",color=(255,255,255),frames=60,cursor=None) :
		if not pygame.display.get_init() : pygame.display.init()
		self.window=pygame.display.set_mode(dim)
		self.COLOR=color
		self.FRAMES=frames
		self.setTitle (title)
		self.cursor=Cursor()
		self.setCursor(cursor)

	def setTitle (self,title) : pygame.display.set_caption(title)
	def getWindow(self) : return self.window
	def getDim (self) : return pygame.display.get_surface().get_size()
	def drawBackground (self) : self.window.fill(self.COLOR)
	def setCursor (self,image) : self.cursor.setImage(image)
	def getFrames (self) : return self.FRAMES
	def getPyEvents (self) : return self.pyEvents
	def exit (self) : self.runFrame=False

	def run (self) :
		self.load()
		self.runFrame=True
		clock=pygame.time.Clock()
		while self.runFrame :
			clock.tick(self.FRAMES)
			self.pyEvents=pygame.event.get()
			for event in self.pyEvents :
				if event.type == pygame.QUIT : self.exit()
			self.events()
			self.update()
			self.cursor.update()
			self.drawBackground()
			self.draw()
			self.cursor.draw(self.window)
			pygame.display.update()

	def load (self) : pass
	def events (self) : pass
	def update (self) : pass
	def draw (self) : pass

class Cursor :

	def __init__ (self,image=None,visible=True) :
		self.image=image
		if self.image : self.rect=self.image.get_rect()
		self.visible=visible

	def setImage (self,image) :
		if image :
			self.image=image
			self.rect=self.image.get_rect()
			pygame.mouse.set_visible(False)
		else :
			self.image=None
			if self.visible : pygame.mouse.set_visible(True)

	def setVisible (self,visible) :
		self.visible=visible
		if visible :
			if not self.image : pygame.mouse.set_visible(True)
			else : pygame.mouse.set_visible(False)
		else :  pygame.mouse.set_visible(False)

	def update (self) :
		if self.image and self.visible : self.rect.center=pygame.mouse.get_pos()

	def draw (self,window) :
		if self.image and self.visible : window.blit(self.image,self.rect)

class Icon :

	def __init__ (self,image,pos) :
		self.IMAGE=image
		self.image=image
		self.rect=self.image.get_rect()
		self.setPos(pos)

	def setPos (self,pos) : self.rect.left,self.rect.top=pos
	def getPos (self) : return self.rect.left,self.rect.top
	def setPosCenter (self,pos) : self.rect.center=pos
	def getPosCenter (self) : return self.rect.center
	def setDim (self,dim) :
		self.image=pygame.transform.scale(self.IMAGE,dim)
		aux=self.getPos(); self.rect=self.image.get_rect(); self.setPos(aux)
	def getDim (self) : return self.rect.width,self.rect.height
	def getTop (self) : return self.rect.top
	def getBottom (self) : return self.rect.bottom
	def getLeft (self) : return self.rect.left
	def getRight (self) : return self.rect.right

	def setImage (self,image) :
		aux=self.getPos()
		self.IMAGE=image
		self.image=image
		self.rect=self.image.get_rect()
		self.setPos(aux)

	def getMouse (self,mouse) :
		if mouse[0] >= self.getLeft() and mouse[0] <= self.getRight() :
			if mouse[1] >= self.getTop() and mouse[1] <= self.getBottom() : return True
		return False

	def draw (self,window) :
		window.blit(self.image,self.rect)

class Text :

	def __init__ (self,font,txt,color,pos) :
		self.font,self.txt,self.color=font,txt,color
		self.text=self.font.render(self.txt,0,self.color)
		self.rect=self.text.get_rect()
		self.setPos(pos)

	def getPos (self) : return self.rect.left,self.rect.top
	def setPos (self,pos) : self.rect.left,self.rect.top=pos
	def getPosCenter (self) : return self.rect.center
	def setPosCenter (self,pos) : self.rect.center=pos 
	def getDim (self) : return self.rect.width,self.rect.height
	def getTop (self) : return self.rect.top
	def getBottom (self) : return self.rect.bottom
	def getLeft (self) : return self.rect.left
	def getRight (self) : return self.rect.right
	def setText (self,txt) : self.text=self.font.render(txt,0,self.color); self.reloadRect(); self.txt=txt
	def setColor (self,color) : self.text=self.font.render(self.txt,0,color); self.reloadRect(); self.color=color
	def setFont (self,font) : self.text=font.render(self.txt,0,self.color); self.reloadRect(); self.font=font
	def reloadRect (self) : aux=self.getPos(); self.rect=self.text.get_rect(); self.setPos(aux) 

	def getMouse (self,mouse) :
		if mouse[0] >= self.getLeft() and mouse[0] <= self.getRight() :
			if mouse[1] >= self.getTop() and mouse[1] <= self.getBottom() : return True
		return False

	def draw (self,window) : window.blit(self.text,self.rect)

class Square :

	def __init__ (self,dim,pos,color,sizeEdge=None) :
		self.rect=pygame.Rect(pos,dim)
		self.color=color
		self.sizeEdge=sizeEdge

	def setPos (self,pos) : self.rect.left,self.rect.top=pos
	def getPos (self) : return self.rect.left,self.rect.top
	def setPosCenter (self,pos) : self.rect.center=pos
	def getPosCenter (self) : return self.rect.center
	def setDim (self,dim) : self.rect=pygame.Rect(self.getPos(),dim)
	def getDim (self) : return self.rect.width,self.rect.height
	def getTop (self) : return self.rect.top
	def getBottom (self) : return self.rect.bottom
	def getLeft (self) : return self.rect.left
	def getRight (self) : return self.rect.right

	def setSizeEdge (self,sizeEdge) : self.sizeEdge=sizeEdge
	def getSizeEdge (self) : return self.sizeEdge
	def setColor (self,color) : self.color=color
	def getColor (self) : return self.color

	def getMouse (self,mouse) :
		if mouse[0] >= self.getLeft() and mouse[0] <= self.getRight() :
			if mouse[1] >= self.getTop() and mouse[1] <= self.getBottom() : return True
		return False

	def draw (self,window) :
		if self.sizeEdge : pygame.draw.rect(window,self.color,self.rect,self.sizeEdge)
		else : pygame.draw.rect(window,self.color,self.rect) 

class MarkerStick :

	def __init__ (self,dim,pos,color=(255,255,255),colorBackground=None,colorEdge=None,sizeEdge=4) :
		self.rect=pygame.Rect(pos,dim)
		self.colorBackground=colorBackground
		self.color=color
		self.colorEdge=colorEdge
		self.sizeEdge=sizeEdge

	def setPos (self,pos) : self.rect.left,self.rect.top=pos
	def getPos (self) : return self.rect.left,self.rect.top
	def setPosCenter (self,pos) : self.rect.center=pos
	def getPosCenter (self) : return self.rect.center 
	def setDim (self,dim) : aux=self.getPos(); self.rect.width,self.rect.height=dim; self.setPos(aux)
	def getDim (self) : return self.rect.width,self.rect.height
	def getTop (self) : return self.rect.top
	def getBottom (self) : return self.rect.bottom
	def getLeft (self) : return self.rect.left
	def getRight (self) : return self.rect.right

	def getMouse (self,mouse) :
		if mouse[0] >= self.getLeft() and mouse[0] <= self.getRight() :
			if mouse[1] >= self.getTop() and mouse[1] <= self.getBottom() : return True
		return False

	def draw (self,window,value=0,maxValue=100) :
		if self.colorBackground : pygame.draw.rect(window,self.colorBackground,self.rect)
		width=round(value*self.getDim()[0]/maxValue)
		if width > self.getDim()[0] : width=self.getDim()[0]
		pygame.draw.rect(window,self.color,(self.getPos(),(width,self.getDim()[1])))
		if self.colorEdge : pygame.draw.rect(window,self.colorEdge,self.rect,self.sizeEdge)