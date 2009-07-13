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
			self.speed = 2
			self.Mobs = pygame.sprite.RenderUpdates()
			self.Glows = pygame.sprite.RenderUpdates()
			self.mobsCount = 0
			
			for i in range(0, size):
				self.Spawn(self.frames)

		def Spawn(self, frames=''):
				sx = random.randrange(60, 600)
				sy = random.randrange(60, 360)
				location = (sx, sy)
				
				if frames == '': frames = self.frames
				
				Entity = AnimatedSprite(frames, location)
				Entity.Glow()
				self.Mobs.add(Entity)
				
		
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
		
		def Animate(self):
			for mob in self.Mobs:
				if mob.image is None:
					return
				self.Move(mob, mob.position)
			
				
		def Move(self, mob, currentLocation):
			loc = [currentLocation[0], currentLocation[1]]
			direction = random.randrange(0,4)
			distance = random.randrange(2,4)
			steping = (distance*self.speed)
			
			for step in xrange(steping):
				if direction is 0:
					if loc[0] - step >= 40 and loc[0] - step < 620: 
						loc[0] = loc[0] - step
			
				if direction is 2:
					if loc[0] + step >= 40 and loc[0] + step < 620: 
						loc[0] = loc[0] + step
					
				if direction is 1:
					if loc[1] - step >= 40 and loc[1] - step < 360: 
						loc[1] = loc[1] - step
			
				if direction is 3:
					if loc[1] + step >= 40 and loc[1] + step < 360: 
						loc[1] = loc[1] + step
						
				mob.position = loc
