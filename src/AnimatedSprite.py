try:
	import sys
	import pygame
	from utils import *
	from pygame.locals import *
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)
	
class AnimatedSprite(pygame.sprite.Sprite):
		def __init__(self, images, initial_position, fps = 30):
			pygame.sprite.Sprite.__init__(self)
			self._images = images
			self._original_images = images
			self._flipped_images = self.flip()
			self._stop = False
			# Track the time we started, and the time between updates.
			# Then we can figure out when we have to switch the image.
			self._start = pygame.time.get_ticks()
			self._delay = 1000 / fps
			self._last_update = 0
			self._frame = 0
			self.position = initial_position
			self.Glowing = False
			
			self.glowFrames = []
			self.glowFrames.append(load_png('glow-1.png'))
			self.glowFrames.append(load_png('glow-2.png'))
			self.glowFrames.append(load_png('glow-2.png'))
			self.glowFrames.append(load_png('glow-3.png'))
			# Call update to set our first image.
			self.update(pygame.time.get_ticks())

		def update(self, t):
			# Note that this doesn't work if it's been more that self._delay
			# time between calls to update(); we only update the image once
			# then, but it really should be updated twice.
			if self._stop is True: 
				return False
				
			if t - self._last_update > self._delay:
				self._frame += 1
				if self._frame >= len(self._images):
					if self.Glowing is True:
						self.Glowing = False
						self._images = self._original_images
					self._frame = 0
				self.image = self._images[self._frame]
				self._last_update = t
				self.rect = self.image.get_rect()
				self.rect.topleft = self.position
				self.mask = pygame.mask.from_surface(self.image)
				return True
			return False
					
					
		def stop(self):
			self._stop = True

		def Glow(self):
			self._original_images = self._images
			self._images = self.glowFrames
			self._frame = -1
			self.Glowing = True
			
			
		def flip(self):
			fliped_frames = []
			for frame in self._images:			
				fliped_frames.append(pygame.transform.flip(frame, True, False))
			return fliped_frames
			
		def ChangeDirection(self, direction):
			if direction is 'left':
				self._images = self._original_images
			else:
				self._images = self._flipped_images
				
