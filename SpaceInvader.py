import pygame

import random
import os
import sys

SCREEN_WIDTH=1000
SCREEN_HEIGHT=800

def resource_path(relative_path):
    """ Gestion ultra-fiable des chemins pour PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # On est dans l'EXE : PyInstaller décompresse dans ce dossier temporaire
        return os.path.join(sys._MEIPASS, relative_path)
    
    # On est en développement : on utilise le chemin réel du fichier .py
    # C'est ici que ça change : on part du dossier du SCRIPT, pas du dossier de CMD
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class MechanteBouleDeNeige(pygame.sprite.Sprite):
	speed=4
	def __init__(self,x,y):
		super().__init__()
		self.x=x
		self.y=y
		self.image=pygame.image.load(resource_path("assets/boule_de_neige.png")).convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.topleft=(self.x,self.y)

	def update(self):
		self.rect.y -= self.speed

		if self.y<0:
			return False
		return True

class Pave(pygame.sprite.Sprite):
	x = random.randint(40,800)
	y = 130
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load(resource_path("assets/giftWall.png")).convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.topleft=(self.x-4,self.y)







class Lutin(pygame.sprite.Sprite):
	speed=5
	compteur = 0
	
	x = random.randint(200,800)
	y = random.randint(SCREEN_HEIGHT//2,744)
	def __init__(self):

		 
		super().__init__()
		self.cd = random.randint(1,1000)
		self.x = random.randint(200,800)
		self.y = random.randint(SCREEN_HEIGHT//2,744)
		self.image=pygame.image.load(resource_path("assets/lutin1.png")).convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.topleft=(self.x,self.y)

	def update(self):
		self.rect.x +=self.speed	
		if self.rect.x +29>SCREEN_WIDTH or self.rect.x<0:
			self.speed=-self.speed
		self.compteur += 1

	def tirer(self):
		if self.compteur >= self.cd: 
			self.compteur = 0
			self.cd = random.randint(1,1000)
			return MechanteBouleDeNeige(self.rect.x-4,self.rect.y-4)
		return None



class BouleDeNeige(pygame.sprite.Sprite):
	speed=4
	def __init__(self,x,y):
		super().__init__()
		self.x=x
		self.y=y
		self.image=pygame.image.load(resource_path("assets/boule_de_neige.png")).convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.topleft=(self.x,self.y)

	def update(self):
		self.rect.y += self.speed

		if self.y>SCREEN_HEIGHT:
			return False
		return True



class PereNoel(pygame.sprite.Sprite):
	x=SCREEN_WIDTH//2
	y=75
	compteur = 20
	cd = 20
	def __init__(self):
		super().__init__()
		self.image=pygame.image.load(resource_path("assets/pereNoel.png")).convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.topleft=(self.x,self.y)

	def moveRight(self):
		if self.rect.x<SCREEN_WIDTH-24:
			self.rect.x +=4

	def moveLeft(self):
		if self.rect.x >0:
			self.rect.x -=4
	def tirer(self):
		
		if self.compteur >= self.cd: 
			self.compteur = 0
			return BouleDeNeige(self.rect.x-4,self.rect.y+15)
		return None
			

	def update(self):
		self.compteur = self.compteur + 1

class SpaceInvaders:
	
	def __init__(self):
			pygame.init()
			self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
			self.clock=pygame.time.Clock()
			self.running=True
			self.pereNoelSprite=pygame.sprite.Group()
			self.pereNoel=PereNoel()
			self.pereNoelSprite.add(self.pereNoel)
			self.lutin=[]
			self.lutinSprite=pygame.sprite.Group()
			for i in range(100):
				newLutin = Lutin()
				self.lutin.append(newLutin)
				self.lutinSprite.add(newLutin)

			self.boulesDeNeigeSprite=pygame.sprite.Group()
			self.boulesDeNeige=[]
			self.paveSprite = pygame.sprite.Group()
			self.pave = Pave()
			self.paveSprite.add(self.pave)
			self.mechanteBoulesDeNeigeSprite=pygame.sprite.Group()
			self.mechanteBoulesDeNeige=[]



	def run (self):
		while self.running:
			self.clock.tick(60)
			self.events()
			self.update()
			self.draw()
	def events(self):
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				self.running=False
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					self.running=False	
		k=pygame.key.get_pressed()
		self.z = 10
		if k[pygame.K_RIGHT]:
			self.pereNoel.moveRight()

		if k[pygame.K_LEFT]:
			self.pereNoel.moveLeft()

		if k[pygame.K_SPACE]:
			newSnowBall=self.pereNoel.tirer()
			if newSnowBall:
				self.boulesDeNeige.append(newSnowBall)
				self.boulesDeNeigeSprite.add(self.boulesDeNeige[-1])


	def update(self):
		for s in self.boulesDeNeige:
			if not s.update():
				self.boulesDeNeige.remove(s)
				self.boulesDeNeigeSprite.remove(s)

		for s in self.mechanteBoulesDeNeige:
			if not s.update():
				self.mechanteBoulesDeNeige.remove(s)
				self.MechanteBoulesDeNeigeSprite.remove(s)

		self.pereNoel.update()

		self.lutinMorts= pygame.sprite.groupcollide(
			self.boulesDeNeigeSprite,
			self.lutinSprite,
			True,
			True)

		for lM in self.lutinMorts.values():
			for l in lM:
				if l in self.lutin:
					self.lutin.remove(l)
		
		self.pereNoelMorts= pygame.sprite.groupcollide(
		 	self.mechanteBoulesDeNeigeSprite,
		 	self.pereNoelSprite,
		 	True,
		 	True)

		for pM in self.pereNoelMorts.values():
			for p in pM:
				if p in self.pereNoel:
					self.pereNoel.remove(p)	
		self.mur = pygame.sprite.groupcollide(
			self.paveSprite,
			self.mechanteBoulesDeNeigeSprite,
			False,
			True)
		self.mur = pygame.sprite.groupcollide(
			self.paveSprite,
			self.boulesDeNeigeSprite,
			False,
			True)
		self.eclat = pygame.sprite.groupcollide(
			self.boulesDeNeigeSprite,
			self.mechanteBoulesDeNeigeSprite,
			True,
			True)

		# for l in self.lutinMorts:
		# 	self.lutin.remove(l[1])

		for l in self.lutin:
			l.update()
			newMechanteSnowBall=l.tirer()
			if newMechanteSnowBall:
				self.mechanteBoulesDeNeige.append(newMechanteSnowBall)
				self.mechanteBoulesDeNeigeSprite.add(newMechanteSnowBall)
		
	def draw(self):
		self.screen.fill((0,0,0))
		self.pereNoelSprite.draw(self.screen)
		self.boulesDeNeigeSprite.draw(self.screen)
		self.pereNoelSprite.draw(self.screen)
		self.lutinSprite.draw(self.screen)
		self.paveSprite.draw(self.screen)
		self.mechanteBoulesDeNeigeSprite.draw(self.screen)
			
		

		pygame.display.flip()
		
SpaceInvaders().run()


		


