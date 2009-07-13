try:
	import sys
	import random
	import pygame
	from pygame.locals import *
	from AnimatedSprite import *
	from profiling import *
	from utils import *
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)

class Mob:
		def __init__(self, frames, size):
			self.frames = frames
			self.living = True
			self.delay = 1000 / 3
			self.speed = 1
			self.boxes = pygame.sprite.RenderUpdates()
			self.Mobs = []
			self.mobsCount = 0
			
			for i in range(0, size):
				self.Spawn(self.frames)

		
		def Spawn(self, frames=''):

				sx = random.randrange(60, 600)
				sy = random.randrange(60, 360)
				location = (sx, sy)
				
				if frames == '':
					frames = self.frames
					
				Entity = AnimatedSprite(frames, random.randrange(5, 20))
				Entity.rect.move_ip(location[0], location[1])
				self.Mobs.append([Entity, location, pygame.time.get_ticks(), 'right'])
				print "Spawned 1 mob at tl %s %s" % (str(location), str(Entity.rect.topleft))
				self.boxes.add(Entity)
				self.mobsCount = self.mobsCount+1
		
		def setScreen(self, Screen):
			self.Screen = Screen
			
		def setBackground(self, Background):
			self.Background = Background
			
		def ChangeDirection(self, i):
			if self.Mobs[i][3] is 'right':
				self.Mobs[i][3] = 'left'
			else:
				self.Mobs[i][3] = 'right'
			self.Mobs[i][0].ChangeDirection(self.Mobs[i][3])
		
		def Animate(self, Screen, Background):
			for mob,location,lastMove,Direction in self.Mobs:
				if mob.update(pygame.time.get_ticks()) is True:
					mob.rect.move_ip(location[0], location[1])				





		def Move(self, i, location, lastMove):
			loc = [location[0], location[1]]
			ticks = pygame.time.get_ticks()
			#if ticks - lastMove > self.delay:
				
			self.Mobs[i][2] = ticks
			direction = random.randrange(0,4)
			distance = random.randrange(3,6)
			steping = (distance*self.speed)
			
			if direction is 0:
				if self.Mobs[i][3] is 'right':
					self.ChangeDirection(i)
				if loc[0] - steping >= 40 and loc[0] - steping < 620: 
					loc[0] = loc[0] - steping
		
			if direction is 2:
				if self.Mobs[i][3] is 'left':
					self.ChangeDirection(i)
				if loc[0] + steping >= 40 and loc[0] + steping < 620: 
					loc[0] = loc[0] + steping
				
			if direction is 1:
				if loc[1] - steping >= 40 and loc[1] - steping < 360: 
					loc[1] = loc[1] - steping
		
			if direction is 3:
				if loc[1] + steping >= 40 and loc[1] + steping < 360: 
					loc[1] = loc[1] + steping

				
			return loc
