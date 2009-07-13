try:
	import sys
	import random
	import pygame
	from pygame.locals import *
	from Hero import *
	from Mob2 import *
	from AnimatedSprite import *
	from utils import *
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)

class CApp:
		def __init__(self):
				self._running = True
				
			
		def OnInit(self):
				pygame.init()
				pygame.font.init()
				self._running = True
				self.Clock = pygame.time.Clock()
				self.Screen = pygame.display.set_mode((640,400))
				#pygame.display.toggle_fullscreen()
				self.Background	= load_png('bg.png')
				self.Interface	= load_png('interface.png')
				self.Font = pygame.font.Font('fonts/BlueStone.ttf', 14)
				self.bigFont = pygame.font.Font('fonts/BlueStone.ttf', 60)
				self.Font.set_bold(True)
				self.BadAlpaSpawned = False
				self.maxPopulation = 50
				
				self.World = pygame.sprite.RenderUpdates()
				
				# Create a rectangle based on the image
				graphRect = self.Background.get_rect()

				# Determine the number of rows and columns of tiles
				rows = int(400/graphRect.height) + 1
				columns = int(640/graphRect.width) + 1

				# Loop and draw the background
				for y in xrange(rows):
					for x in xrange (columns):
						# Start a new row
						if x == 0 and y > 0:
							graphRect = graphRect.move([-(columns -1 ) * graphRect.width, graphRect.height])
						# Continue a row
						if x > 0:
							graphRect = graphRect.move([graphRect.width, 0])
						self.Screen.blit(self.Background, graphRect)

				# Convert Tiled background to Image
				bgStr = pygame.image.tostring(self.Screen, 'RGB')
				self.Background = pygame.image.fromstring(bgStr, (640,400), 'RGB')
      	
      
				#self.Screen.blit(self.Background, (0,0) , pygame.Rect(0, 0, 640, 480))

				
				self._bad_sprites = []
				self._bad_sprites.append(load_png('bad-1.png'))
				self._bad_sprites.append(load_png('bad-2.png'))
				self._bad_sprites.append(load_png('bad-2.png'))
				self._bad_sprites.append(load_png('bad-3.png'))
				
				self._bad_child_sprites = []
				self._bad_child_sprites.append(load_png('bad-child-1.png'))
				self._bad_child_sprites.append(load_png('bad-child-2.png'))
				self._bad_child_sprites.append(load_png('bad-child-2.png'))
				self._bad_child_sprites.append(load_png('bad-child-3.png'))

				self.alphaFrames = []
				self.alphaFrames.append(load_png('alphabad-1.png'))
				self.alphaFrames.append(load_png('alphabad-2.png'))
				self.alphaFrames.append(load_png('alphabad-2.png'))
				self.alphaFrames.append(load_png('alphabad-3.png'))
				
				
				self.BadBoys = Mob(self._bad_sprites, 20)
				self.BadBoys.setScreen(self.Screen)
				self.BadBoys.setBackground(self.Background)

				self.BadGirls = Mob(self._bad_child_sprites, 20)
				self.BadGirls.setScreen(self.Screen)
				self.BadGirls.setBackground(self.Background)
				
				self.Shroom = Hero()
				self.Shroom.setScreen(self.Screen)
				self.Shroom.setFont(self.Font)
				
				self.World.add(self.BadBoys.Mobs)
				self.World.add(self.BadGirls.Mobs)
				self.World.add(self.Shroom.boxes)
				
				
				self.population = len(self.World)		
				
				
				self.updateInterface()
				
				pygame.display.flip()
				
		def SpawnAlpha(self) :
				self.BadAlpaSpawned = True
				self.BadAlphaMale = Mob(self.alphaFrames, 1)
				self.BadAlphaMale.speed = 4
				self.BadAlphaMale.setScreen(self.Screen)
				self.BadAlphaMale.setBackground(self.Background)
				
				self.World.add(self.BadAlphaMale.Mobs)
				
				self.bigFont = pygame.font.Font('fonts/BlueStone.ttf', 40)	
				tempLabel = self.bigFont.render("Alpha Male Spawned!", 1, (255, 180, 0))
				tempLabelShade = self.bigFont.render("Alpha Male Spawned!", 1, (80, 80, 80))
				textpos = tempLabel.get_rect()
				textpos.centerx = self.Screen.get_rect().centerx
				textpos.centery = self.Screen.get_rect().centery
				
				shadepos = tempLabel.get_rect()
				shadepos.centerx = self.Screen.get_rect().centerx-5
				shadepos.centery = self.Screen.get_rect().centery-5
				self.Screen.blit(tempLabelShade, shadepos)
				self.Screen.blit(tempLabel, textpos)
				pygame.display.update(shadepos)
				pygame.display.update(textpos)
				pygame.time.delay(3000)
				self.Screen.blit(self.Background, textpos)
				self.Screen.blit(self.Background, shadepos)
				pygame.display.update(shadepos)
				pygame.display.update(textpos)
					
				
		def OnEvent(self, event):
				pygame.event.pump()
				if event.type == QUIT:
						self._running = False
				
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self._running = False
						
					self.Shroom.Move(event.key);
		

		def updateInterface(self):
			self.Screen.blit(self.Interface, (0,0))

			tempLabel = []
			tempLabel.append(self.Font.render("Score: %d" % self.Shroom.score, 1, (0, 0, 0)))
			tempLabel.append(self.Font.render("FPS: %0.2f" % self.Clock.get_fps(), 1, (0, 0, 0)))
			tempLabel.append(self.Font.render("Pop: %d/%d" % (self.population,self.maxPopulation), 1, (0, 0, 0)))
			i = 1
			lastPrint = 12
			for line in tempLabel:
				i += 1
				self.Screen.blit(line, (lastPrint, 12))
				lastPrint = lastPrint + 640/i - 20
								
			pygame.display.update((12, 12, 640, 30));


		def OnLoop(self):
			pass
		
		def OnRender(self):
			self.Screen.blit(self.Background, (0,0))
			self.updateInterface()
						
			self.BadBoys.Animate()
			if self.BadAlpaSpawned is True : self.BadAlphaMale.Animate()
			self.BadGirls.Animate()
			self.Shroom.Animate()
			
			self.population = len(self.World)

			self.World.update(pygame.time.get_ticks())
			updatedSprites = self.World.draw(self.Screen)
			pygame.display.update(updatedSprites)
			
			
			hitList = pygame.sprite.groupcollide(self.Shroom.boxes, self.BadBoys.Mobs, False, True) 
			self.Shroom.Score(10*len(hitList))
			
			hitList = pygame.sprite.groupcollide(self.Shroom.boxes, self.BadGirls.Mobs, False, True) 
			self.Shroom.Score(10*len(hitList))
			
			if self.population < self.maxPopulation:
				hitList = pygame.sprite.groupcollide(self.BadBoys.Mobs, self.BadGirls.Mobs, False, False) 
				for hit in hitList:
					luckFactor = random.randrange(0,100)
					if self.population < 10:
						luckFactor = luckFactor / 2
					if luckFactor < 2:
						print "2 Mates with a luckFactor of %d!" % luckFactor
						print "Population needs a raise."
						SuperHero = random.randrange(0,500) 
						if SuperHero < 2 and self.BadAlpaSpawned is False :
							self.SpawnAlpha()
						if random.randrange(0,100) < 50:
							print "It's a Girl!"
							self.BadGirls.Spawn(self._bad_child_sprites)
							self.World.add(self.BadGirls.Mobs)
							Gender = 'Girl'
						else: 
							print "It's a Boy!"
							self.BadBoys.Spawn(self._bad_sprites)
							self.World.add(self.BadBoys.Mobs)
							Gender = 'Boy'
														
							'''
							self.bigFont = pygame.font.Font('fonts/BlueStone.ttf', 16)	
							tempLabel = self.bigFont.render("A %s is born!" % Gender, 1, (255, 180, 0))

							textpos = tempLabel.get_rect()
							textpos.topleft = (40, 40)

							self.Screen.blit(tempLabel, textpos)
							pygame.display.update(textpos)
							pygame.time.wait(500)
							self.Screen.blit(self.Background, textpos)
							pygame.display.update(textpos)
							'''
						self.Shroom.Score(-10)
					
			

			
			
		def OnCleanup(self):
				pygame.quit()
 
		def OnExecute(self):
				if self.OnInit() == False:
						self._running = False
				pygame.key.set_repeat(10,10)
				'''
				self.bigFont = pygame.font.Font('fonts/BlueStone.ttf', 60)
				
				countDown = 4
				for i in range(1,4):
					tempLabel = self.bigFont.render("%s" % str(countDown-i), 1, (255, 180, 0))
					textpos = tempLabel.get_rect()
										
					for size in range(1, 60):
						textpos.inflate_ip(1, 0)
						textpos.centerx = self.Screen.get_rect().centerx
						textpos.centery = self.Screen.get_rect().centery
						self.Screen.blit(self.Background, (50,50) , pygame.Rect(50,50, 600, 600))
						self.Screen.blit(tempLabel, textpos)
						pygame.display.update(textpos)
						pygame.time.wait(500/60)

					self.Screen.blit(self.Background, (50,50) , pygame.Rect(50,50, 600, 600))
					pygame.display.update()
					
				self.Screen.blit(self.Background, (50,50) , pygame.Rect(50,50, 600, 600))
				pygame.display.update()
				
				self.bigFont = pygame.font.Font('fonts/BlueStone.ttf', 120)		
				tempLabel = self.bigFont.render("GO!", 1, (255, 180, 0))
				self.bigFont.set_italic(True)
				
				textpos = tempLabel.get_rect()
				textpos.centerx = self.Screen.get_rect().centerx
				textpos.centery = self.Screen.get_rect().centery
				self.Screen.blit(tempLabel, textpos)
				pygame.display.flip()
				pygame.time.delay(500)
				self.Screen.blit(self.Background, (50,50) , (50,50, 600, 600))
				pygame.display.update(textpos)
				'''
				
				while( self._running ):
						#pygame.event.pump()
						self.Clock.tick(60)
						for event in pygame.event.get():
								self.OnEvent(event)
						self.OnLoop()
						self.OnRender()
						
				self.OnCleanup()
 
if __name__ == "__main__" :
		Game = CApp()
		Game.OnExecute()


