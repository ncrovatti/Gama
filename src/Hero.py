try:
	import sys
	import pygame
	from pygame.locals import *
	from AnimatedSprite import *
	from utils import *
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)


class Hero:
		def __init__(self):
			self.living = True
			self.speed = 3
			self.score = 0
			self.position = [320,200]
			self.location = (self.position[0], self.position[1])
			self.Direction = 'left'
			self.frames = []
			self.frames.append(load_png('shroom-1.png'))
			self.frames.append(load_png('shroom-3.png'))
			self.frames.append(load_png('shroom-2.png'))
			self.frames.append(load_png('shroom-3.png'))
			self.boxes = pygame.sprite.RenderUpdates()
			self.Sprite =  AnimatedSprite(self.frames, self.location, 10)
			self.boxes.add(self.Sprite)
			

			
		def setFont(self, font):
			self.Font = font
			
		def setScreen(self, screen):
			self.Screen = screen
			
		def Score(self, score):
			self.score += score
			#print "New Score is %d" % self.score


			
		def ChangeDirection(self):
			if self.Direction is 'right':
				self.Direction = 'left'
			else:
				self.Direction = 'right'
			self.Sprite.ChangeDirection(self.Direction)
			
			
		def Animate(self):
			self.Sprite.position = self.location

			'''
			if self.Sprite.update(pygame.time.get_ticks()) is True:
				self.Sprite.position = self.location
				rectlist = self.boxes.draw(self.Screen)
				pygame.display.update(rectlist)
			'''
			
		def Move(self, key):
			step = (2*self.speed)							
			if key == K_LEFT:
				if self.Direction is 'right':
					self.ChangeDirection()

				if self.position[0] - step >= 20: 
					self.position[0] = self.position[0] - step
					
			if key == K_RIGHT:
				if self.Direction is 'left':
					self.ChangeDirection()
				
				if self.position[0] + step < 620:
					self.position[0] = self.position[0] + step
				
			if key == K_UP:
				if self.position[1] - step >= 40:
					self.position[1] = self.position[1] - step
			if key == K_DOWN:
					if self.position[1] + step <= 360:
						self.position[1] = self.position[1] + step
						
			self.location = (self.position[0], self.position[1])

			'''
			myRect = self._sprite.image.get_rect()
			badRect = self._bad_sprite.image.get_rect()
			if myRect.colliderect(badRect):
				self.bad_killed = True
				self.speed = 2
			'''
				
			pygame.event.pump()	
