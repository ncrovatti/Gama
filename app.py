SCREEN_SIZE = (1024, 700)
NEST_POSITION = (320, 240)
ANT_COUNT = 20
NEST_SIZE = 100.

import os
import pygame
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

class State(object):
		
		def __init__(self, name):				
				self.name = name
				
		def do_actions(self):
				pass
				
		def check_conditions(self):				
				pass		
		
		def entry_actions(self):				
				pass		
		
		def exit_actions(self):				
				pass
				
				
class StateMachine(object):
		
		def __init__(self):
				
				self.states = {}
				self.active_state = None
		
		
		def add_state(self, state):
				
				self.states[state.name] = state
				
				
		def think(self):
				
				if self.active_state is None:
						return
				
				self.active_state.do_actions()				

				new_state_name = self.active_state.check_conditions()
				if new_state_name is not None:
						self.set_state(new_state_name)
				
		
		def set_state(self, new_state_name):
				
				if self.active_state is not None:
						self.active_state.exit_actions()
						
				self.active_state = self.states[new_state_name]				
				self.active_state.entry_actions()
				
			
		
class World(object):
		
		def __init__(self):
				
				self.font = pygame.font.SysFont('Arial', 12, True)
				
				self.entities = {}
				self.exp_table = {}
				self.entity_id = 0	
				self.average_level = 1
				
				for i in xrange(1, 101):
					self.exp_table[i] = float((i * 1000) + ((i-1)*1000))
				
				self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
				self.background.fill((255, 255, 255))
				pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))
				
		def add_entity(self, entity):
				
				self.entities[self.entity_id] = entity
				entity.id = self.entity_id
				self.entity_id += 1
				
		def remove_entity(self, entity):
				
				del self.entities[entity.id]
								
		def get(self, entity_id):
				
				if entity_id in self.entities:
						return self.entities[entity_id]
				else:
						return None
				
		def process(self, time_passed):
								
				time_passed_seconds = time_passed / 1000.0				
				for entity in self.entities.values():
						entity.process(time_passed_seconds)
						
		def render(self, surface):
				
				surface.blit(self.background, (0, 0))
				entity_selected = False
				
				for entity in self.entities.itervalues():
						if entity.selected is True:
							entity_selected = True
						entity.render(surface)
				
				if entity_selected is True:
					x, y = SCREEN_SIZE
					
					x = x - 220
					y = 20
					w = 200
					h = 400
					
					color = (80, 80, 80)
					border = 2
					pygame.draw.line(surface, color, (x, y), (x+w, y), border)
					pygame.draw.line(surface, color, (x+w, y), (x+w, y+h), border)
					pygame.draw.line(surface, color, (x+w, y+h), (x, y+h), border)
					pygame.draw.line(surface, color, (x, y+h), (x, y), border)
					pygame.draw.rect(surface, (255,255,255), (x+border,y+border,w-border,h-border))
					
					xtext = x + 20
					ytext = y + 20
					
					lines = []
					lines.append("Level: %d" % self.level)
					lines.append("Experience: %d" % self.experience)
					lines.append("Death Blows: %d" % self.kills)
					lines.append("Speed: %d" % self.speed)
					
					'''Level'''
					for line in lines:
						text = self.world.font.render(line, 1, (80, 80, 80))
						wtext, htext = text.get_size()
						surface.blit(text, (xtext, ytext, wtext, htext))
						ytext += htext + 10
					
						
		def get_close_entity(self, name, location, range=100.):
				
				location = Vector2(*location)				
				
				for entity in self.entities.itervalues():						
						if entity.name == name:								
								distance = location.get_distance_to(entity.location)
								if distance < range:
										return entity				
				return None
		
		def set_average_level(self):
				i = 0
				total_level = 0
				for entity in self.entities.itervalues():						
						if entity.name == 'ant':
								i += 1			
								total_level += entity.level
								
				self.average_level = int(total_level/i)		
				return None
			
		def get_clicked_entity(self, location):				
				for entity in self.entities.itervalues():
					entity.selected = False
					sprite_loc = Rect(entity.location,entity.image.get_size())
					if sprite_loc.contains(location):
						
						return self.get(entity.id)
					
				return None
	

class GameEntity(object):
		
		def __init__(self, world, name, image):
				
				self.world = world
				self.name = name
				self.image = image
				self.location = Vector2(0, 0)
				self.destination = Vector2(0, 0)
				self.speed = 0.
				self.level = 0
				self.experience = 0.
				self.selected = False
				self.selected_image = pygame.image.load(os.path.join('ressources', 'selected.png')).convert_alpha()
				
				
				self.brain = StateMachine()
				
				self.id = 0
		

				
		def render(self, surface):
				x, y = self.location
				w, h = self.image.get_size()
				
				if self.selected:
					ws, hs = self.selected_image.get_size()
					surface.blit(self.selected_image, (x-ws/2, (y+hs/2)+hs))
				surface.blit(self.image, (x-w/2, y-h/2))
				
				'''
				color = (20, 120, 0)
				pygame.draw.line(surface, color, (x, y), (x+w, y), 2)
				pygame.draw.line(surface, color, (x+w, y), (x+w, y+h), 2)
				pygame.draw.line(surface, color, (x+w, y+h), (x, y+h), 2)
				pygame.draw.line(surface, color, (x, y+h), (x, y), 2)
				'''
				
		def process(self, time_passed):
				
				self.brain.think()
				
				if self.level > 0:
						if self.experience >= self.world.exp_table[self.level]:
							self.level_up()
				
				if self.speed > 0. and self.location != self.destination:
						
						vec_to_destination = self.destination - self.location				
						distance_to_destination = vec_to_destination.get_length()
						heading = vec_to_destination.get_normalized()
						travel_distance = min(distance_to_destination, time_passed * self.speed)
						self.location += travel_distance * heading

class Ore(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "ore", image)
				self.health = 2500
				
		def mined(self):
			self.health -= 1
			if self.health <= 0:
				self.image = self.world.background
				
		def render(self, surface):

				GameEntity.render(self, surface)
				if self.health > 0:
					x, y = self.location
					w, h = self.image.get_size()
					bar_x = x - 25
					bar_y = y + h/2
					surface.fill( (255, 0, 0), (bar_x, bar_y, 50, 4))
					surface.fill( (0, 255, 0), (bar_x, bar_y, int((self.health/50)), 4))
				

class Leaf(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "leaf", image)
				
				
class Spider(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "spider", image)
				self.dead_image = pygame.transform.flip(image, 0, 1)
				self.speed = 50. + randint(-20, 20)
				self.level = self.world.average_level
				self.health = 25 + self.world.average_level
				self.max_health = 25 + self.world.average_level
				
		def bitten(self, ant):
				
				self.health -= 1
				
				if randint(1, 3) == 1:
					ant.bitten()
					if ant.health <= 0:
						self.world.remove_entity(ant)
						
				if self.health <= 0:
						self.speed = 0.
						self.image = self.dead_image
				self.speed = 140.
				

				
		def render(self, surface):
				
				GameEntity.render(self, surface)
								
				x, y = self.location
				w, h = self.image.get_size()
				
				unit = float(25./100.)
				
				'''Level'''
				bar_x = x-(w/4)
				level = self.world.font.render(str(self.level), 1, (80, 80, 80))
				w2,h2 = level.get_size()
				bar_y = y - h 
				surface.blit(level, (bar_x, bar_y, w2,h2))
				
				'''Life Bar'''
				bar_x = x - 12
				bar_y = y + h/2
				rate = float(float(self.health)/float(self.max_health))*100
				surface.fill( (200, 0, 0), (bar_x, bar_y, 25, 4))
				surface.fill( (0, 200, 0), (bar_x, bar_y, rate*unit, 4))
				
		def process(self, time_passed):
				
				x, y = self.location
				if x > SCREEN_SIZE[0] + 2:
						self.world.remove_entity(self)
						return
				
				GameEntity.process(self, time_passed)
				
		
class Ant(GameEntity):
		
		def __init__(self, world, image):
				
				GameEntity.__init__(self, world, "ant", image)

				exploring_state = AntStateExploring(self)
				seeking_state = AntStateSeeking(self)
				delivering_state = AntStateDelivering(self)
				hunting_state = AntStateHunting(self)
				mining_state = Mining(self)
							
				self.brain.add_state(exploring_state)
				self.brain.add_state(seeking_state)
				self.brain.add_state(delivering_state)
				self.brain.add_state(hunting_state)
				self.brain.add_state(mining_state)
				
				self.dead_image = pygame.transform.flip(image, 0, 1)
				self.health = 5
				self.max_health = 5
				self.max_carrying = 100
				self.carrying = 0
				self.carry_image = None
				
				self.kills = 0
				
				''' Experience '''
				self.experience = 0
				self.level = 1

		def refill_life(self):
				self.health = self.max_health

		def level_up(self):
				self.level += 1
				self.max_health += 1
				self.world.set_average_level()
				self.refill_life()
				self.experience = 0
				
		def carry(self, image):
				self.carry_image = image

		def bitten(self):
				
				self.health -= 1
				if self.health <= 0:
						self.speed = 0.
						self.image = self.dead_image

		def drop(self, surface):
				if self.carrying > 0:
					self.experience += 300
					self.carrying = 0
				
				if self.carry_image:
						x, y = self.location
						w, h = self.carry_image.get_size()
						surface.blit(self.carry_image, (x-w, y-h/2))
						self.carry_image = None
						self.experience += 300
				
		def render(self, surface):
				
				GameEntity.render(self, surface)
				x, y = self.location
				w, h = self.image.get_size()
				
				unit = float(25./100.)
				
				'''Level'''
				bar_x = x-(w/4)
				level = self.world.font.render(str(self.level), 1, (80, 80, 80))
				w2,h2 = level.get_size()
				bar_y = y - h 
				surface.blit(level, (bar_x, bar_y, w2,h2))
				
				'''Life Bar'''
				bar_x = x - 12
				bar_y = y + h/2
				rate = float(float(self.health)/float(self.max_health))*100
				surface.fill( (200, 0, 0), (bar_x, bar_y, 25, 4))
				surface.fill( (0, 200, 0), (bar_x, bar_y, rate*unit, 4))
				
				'''Charge Bar'''
				bar_y = y + h/2 + 5
				surface.fill( (180, 180, 180), (bar_x, bar_y, 25, 4))
				surface.fill( (0, 0, 200), (bar_x, bar_y, int(self.carrying/4), 4))
				
				'''Exp bar'''		
				bar_y = y - h + 12
				surface.fill( (180, 180, 180), (bar_x, bar_y, 25, 4))
				rate = float(float(self.experience)/float(self.world.exp_table[self.level]))*100
				surface.fill( (255, 210, 0), (bar_x, bar_y, rate*unit, 4))
								
				if self.carry_image:
						x, y = self.location
						w, h = self.carry_image.get_size()
						surface.blit(self.carry_image, (x-w, y-h/2))

class AntStateExploring(State):
		
		def __init__(self, ant):
				
				State.__init__(self, "exploring")
				self.ant = ant
				
		def random_destination(self):
				
				w, h = SCREEN_SIZE
				self.ant.destination = Vector2(randint(0, w), randint(0, h))		
		
		def do_actions(self):
				
				if randint(1, 20) == 1:
						self.random_destination()
						
		def check_conditions(self):
												
				leaf = self.ant.world.get_close_entity("leaf", self.ant.location)				
				if leaf is not None:
						self.ant.leaf_id = leaf.id
						return "seeking"	
								
				ore = self.ant.world.get_close_entity("ore", self.ant.location)				
				if ore is not None:
						self.ant.ore_id = ore.id
						return "mining"	
								
				spider = self.ant.world.get_close_entity("spider", NEST_POSITION, NEST_SIZE)				
				if spider is not None:
						if self.ant.location.get_distance_to(spider.location) < 100.:
								self.ant.spider_id = spider.id
								return "hunting"
				
				return None
		
		def entry_actions(self):
				self.ant.speed = 120. + randint(-30, 30)
				self.random_destination()
				
class Mining(State):
		def __init__(self, ant):
				
				State.__init__(self, "mining")
				self.ant = ant
				self.max_charge = None
				
		def do_actions(self):
				
				ore = self.ant.world.get(self.ant.ore_id)
			
				if ore is None:
						return
					
				w,h = ore.image.get_size()			
				if self.ant.location.get_distance_to(ore.location) < w:
						
						if self.ant.carrying < self.ant.max_carrying:
								ore.mined()
								self.ant.carrying += 1
						else:
								self.max_charge = True
								
						if ore.health <= 0:								
								self.ant.world.remove_entity(ore)
							
														
				
		def check_conditions(self):
				
				if self.max_charge:
						return "delivering"
				
				ore = self.ant.world.get(self.ant.ore_id)
												
				if ore is None:
						return "exploring"
				
				
				return None

		def exit_actions(self):
				self.max_charge = False
				
		def entry_actions(self):
		
				ore = self.ant.world.get(self.ant.ore_id)
				if ore is not None:
						x,y,w,h = ore.image.get_rect()
						self.ant.destination = ore.location - Vector2(w/2,h/2)
						self.ant.speed = 160. + randint(-20, 20)
							
				
class AntStateSeeking(State):
		
		def __init__(self, ant):
				
				State.__init__(self, "seeking")
				self.ant = ant
				self.leaf_id = None
		
		def check_conditions(self):
				
				leaf = self.ant.world.get(self.ant.leaf_id)
				if leaf is None:
						return "exploring"
				
				if self.ant.location.get_distance_to(leaf.location) < 5.0:
				
						self.ant.carry(leaf.image)
						self.ant.world.remove_entity(leaf)
						return "delivering"
				
				return None
		
		def entry_actions(self):
		
				leaf = self.ant.world.get(self.ant.leaf_id)
				if leaf is not None:												
						self.ant.destination = leaf.location
						self.ant.speed = 160. + randint(-20, 20)
				
				
class AntStateDelivering(State):
		
		def __init__(self, ant):
				
				State.__init__(self, "delivering")
				self.ant = ant
				
				
		def check_conditions(self):
								
				if Vector2(*NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
						if (randint(1, 10) == 1):
								self.ant.drop(self.ant.world.background)
								return "exploring"
						
				return None
				
				
		def entry_actions(self):
				
				self.ant.speed = 60.				
				random_offset = Vector2(randint(-20, 20), randint(-20, 20))
				self.ant.destination = Vector2(*NEST_POSITION) + random_offset			 
			 
				
class AntStateHunting(State):
		
		def __init__(self, ant):
				
				State.__init__(self, "hunting")
				self.ant = ant
				self.got_kill = False
				
		def do_actions(self):
				
				spider = self.ant.world.get(self.ant.spider_id)
				
				if spider is None:
						return
						
				self.ant.destination = spider.location
						
				if self.ant.location.get_distance_to(spider.location) < 15.:
						
						if randint(1, 5) == 1:
								spider.bitten(self.ant)
								
								if spider.health <= 0:
										self.ant.carry(spider.image)								
										self.ant.world.remove_entity(spider)
										self.got_kill = True
										self.kills += 1
										self.ant.experience += 600
														
				
		def check_conditions(self):
				if self.ant.health <= int(self.ant.max_health/10):
						return "exploring"
				
				if self.got_kill:
						return "delivering"
				
				spider = self.ant.world.get(self.ant.spider_id)
												
				if spider is None:
						return "exploring"
				
				if spider.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 3:
						return "exploring"
				
				return None

		def entry_actions(self):
				
				self.speed = 160. + randint(0, 50)

		def exit_actions(self):
				
				self.got_kill = False


		
def run():
		
		pygame.init()
		screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
		#pygame.display.toggle_fullscreen()
		world = World()
		
		w, h = SCREEN_SIZE
		
		clock = pygame.time.Clock()
		
		ant_image = pygame.image.load(os.path.join('ressources', 'bad-1.png')).convert_alpha()
		leaf_image = pygame.image.load(os.path.join('ressources', 'bad-child-1.png')).convert_alpha()
		spider_image = pygame.image.load(os.path.join('ressources', 'glow-1.png')).convert_alpha()
		
		ore_images = []
		ore_images.append(pygame.image.load(os.path.join('ressources', 'ore-1.png')).convert_alpha()) 
		ore_images.append(pygame.image.load(os.path.join('ressources', 'ore-2.png')).convert_alpha())
		ore_images.append(pygame.image.load(os.path.join('ressources', 'ore-3.png')).convert_alpha())
		ore_images.append(pygame.image.load(os.path.join('ressources', 'ore-4.png')).convert_alpha())
		ore_images.append(pygame.image.load(os.path.join('ressources', 'ore-5.png')).convert_alpha())
		ore_images.append(pygame.image.load(os.path.join('ressources', 'ore-6.png')).convert_alpha())

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
									entity.selected = True
								

				time_passed = clock.tick(30)
				
				if randint(1, 500) == 1:
						ore = Ore(world, ore_images[randint(0,5)])
						ore.location = Vector2(randint(0, w), randint(0, h))
						world.add_entity(ore)				

				
				if randint(1, 200) == 1:
					ant = Ant(world, ant_image)
					ant.location = Vector2(randint(0, w), randint(0, h))
					ant.brain.set_state("exploring")
					world.add_entity(ant)
				
															
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
		
