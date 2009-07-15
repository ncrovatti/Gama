SCREEN_SIZE = (1024, 700)
NEST_POSITION = (320, 240)
ANT_COUNT = 20
NEST_SIZE = 200.

import os
import pygame
from pygame.locals import *
from math import sqrt
from random import randint, choice
from gameobjects.vector2 import Vector2

'''
def GameInit():
	zipnames = filter(isfile, glob.glob('*.gen'))
	for zipname in zipnames:
		zf = zipfile.ZipFile (zipname, 'r')
		for zfilename in zf.namelist(): # don't shadow the "file" builtin
			newFile = open ( zfilename, "wb")
			newFile.write (zf.read (zfilename))
			newFile.close() 
		zf.close()
'''
		
def run():
		#GameInit()
		pygame.init()
		screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
		#pygame.display.toggle_fullscreen()
		world = World()

		Background = world.ground_images[4]
		graphRect = world.ground_images[1].get_rect()

		w, h = SCREEN_SIZE
		
		columns = int(w/graphRect.width) + 1
		rows = int(h/graphRect.height) + 1
		# Loop and draw the background
		for y in xrange(rows):
			for x in xrange (columns):
				# Start a new row
				if x == 0 and y > 0:
					graphRect = graphRect.move([-(columns -1 ) * graphRect.width, graphRect.height])
				# Continue a row
				if x > 0:
					graphRect = graphRect.move([graphRect.width, 0])
				screen.blit(Background, graphRect)
				
		map = [
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   1,   2,   3,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   5,   6,   7,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   5,   6,   9,   3,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   10,  6,   6,   7,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   10,  11,  12,  4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   1,   2,   3,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   5,   6,   7,   4,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   5,   6,   9,   3,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   10,  6,   6,   7,   4],
			[4,   4,   4,   4,   4,   4,   4,   4,   4,   10,  11,  12,  4],
		];
		
		x = 0
		y = 0
		for row in map:
			for tile in row:
				screen.blit(world.ground_images[tile], (x, y))
				x += graphRect.width
			x = 0
			y += graphRect.width
			
		nest_location = Vector2(*NEST_POSITION)
		
		for i in xrange(10):	 
			wanted_x = randint(0, w)
			wanted_y = randint(0, h)
			while nest_location.get_distance_to((wanted_x, wanted_y)) < NEST_SIZE:
				wanted_x = randint(0, w)
				wanted_y = randint(0, h)
			screen.blit(world.map_images[randint(1, 4)], (wanted_x,wanted_y))
			
		# Convert Tiled background to Image
		bgStr = pygame.image.tostring(screen, 'RGB')

		world.background = pygame.image.fromstring(bgStr, SCREEN_SIZE, 'RGB')
		
		clock = pygame.time.Clock()
		
		ant_image = []
		ant_image.append(pygame.image.load(os.path.join('ressources', 'bad-1.png')).convert_alpha())
		ant_image.append(pygame.image.load(os.path.join('ressources', 'bad-2.png')).convert_alpha())
		ant_image.append(pygame.image.load(os.path.join('ressources', 'bad-3.png')).convert_alpha())
		
		leaf_image = []
		leaf_image.append(pygame.image.load(os.path.join('ressources', 'bad-child-1.png')).convert_alpha())
		spider_image = []
		spider_image.append(pygame.image.load(os.path.join('ressources', 'glow-1.png')).convert_alpha())

		ore_images = []
		ore_images.append([pygame.image.load(os.path.join('ressources', 'ore-1.png')).convert_alpha()]) 
		ore_images.append([pygame.image.load(os.path.join('ressources', 'ore-2.png')).convert_alpha()])
		ore_images.append([pygame.image.load(os.path.join('ressources', 'ore-3.png')).convert_alpha()])
		ore_images.append([pygame.image.load(os.path.join('ressources', 'ore-4.png')).convert_alpha()])
		ore_images.append([pygame.image.load(os.path.join('ressources', 'ore-5.png')).convert_alpha()])
		ore_images.append([pygame.image.load(os.path.join('ressources', 'ore-6.png')).convert_alpha()])

		for ant_no in xrange(ANT_COUNT):
				ant = Ant(world, ant_image)
				ant.location = Vector2(randint(0, w), randint(0, h))
				ant.brain.set_state("exploring")
				world.add_entity(ant)
		
		
		while True:
				
				for event in pygame.event.get():
				
						if event.type == KEYDOWN:
							if event.key == K_ESCAPE:
								return
						if event.type == QUIT:
								return				
						if event.type == MOUSEBUTTONDOWN:
								entity = world.get_clicked_entity(pygame.Rect(pygame.mouse.get_pos() + (4,4)))
								if entity is not None:
									entity.select()
								

				time_passed = clock.tick(30)
				
				if randint(1, 500) == 1:
						ore = Ore(world, ore_images[randint(0,5)])
						ore.location = Vector2(randint(0, w), randint(0, h))
						world.add_entity(ore)				
						
				'''
				if randint(1, 200) == 1:
					ant = Ant(world, ant_image)
					ant.location = Vector2(randint(0, w), randint(0, h))
					ant.brain.set_state("exploring")
					world.add_entity(ant)
				'''
															
				if randint(1, 10) == 1:
						leaf = Leaf(world, leaf_image)
						leaf.location = Vector2(randint(0, w), randint(0, h))
						world.add_entity(leaf)
						
				if randint(1, 50) == 1:
						spider = Spider(world, spider_image)
						spider.location = Vector2(-50, randint(0, h))
						spider.destination = Vector2(w+50, randint(0, h))						
						world.add_entity(spider)
				
				world.process(time_passed)
				world.render(screen)
				
				pygame.display.update()
		
if __name__ == "__main__":		
		run()
		
