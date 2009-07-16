SCREEN_SIZE = (1024, 700)
NEST_POSITION = (320, 240)
ANT_COUNT = 20
NEST_SIZE = 200.

import os
import pygame
from pygame.locals import *
from math import sqrt, acos, degrees
from random import randint, choice
from gameobjects.vector2 import Vector2

class World(object):
		
		def __init__(self):
				self.font = pygame.font.SysFont('Arial', 12, False)
				
				self.entities = {}
				self.entities_count = {}
				self.exp_table = {}
				self.entity_id = 0	
				self.average_level = 1
				self.ore_hull_size = 100000.
				self.ore_farmed = 0.
				self.paused = False
				self.show_bars = False
				
				for i in xrange(0, 120):
					self.exp_table[i] = float((i * 1000) + ((i-1)*1000))
					
				self.ground_images = {}
				for i in xrange(14):
					i += 1
					filename = 'g%d.png' % i
					self.ground_images[i] = pygame.image.load(os.path.join('ressources', filename)).convert() 
				
				self.map_images = {}
				for i in xrange(4):
					i += 1
					filename = 'r%d.png' % i
					self.map_images[i] = pygame.image.load(os.path.join('ressources', filename)).convert_alpha() 
					
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
				entity_selected = None
				
				for entity in self.entities.itervalues():
						if entity.selected is True:
							entity_selected = entity
						entity.render(surface)

				''' Ore tank ''' 
				x, y = NEST_POSITION 
				x = x - 20
				w = 20
				
				h = NEST_SIZE/2
				
				lightColor = (100, 170, 208, 127)
				darkColor = (3, 69, 105)
				backgroundColor = (8, 108, 162)
				emptyBackgroundColor = (154, 192, 212, 80)
				shadowColor = (80,80,80, 127)

				
				shadowMargin = 2
				border = 1
				pygame.draw.rect(self.background, shadowColor, (x+border+shadowMargin,y+border+shadowMargin,w-border,h-border))
				pygame.draw.line(self.background, lightColor, (x, y), (x+w, y), border)
				pygame.draw.line(self.background, darkColor, (x+w, y), (x+w, y+h), border)
				pygame.draw.line(self.background, darkColor, (x+w, y+h), (x, y+h), border)
				pygame.draw.line(self.background, lightColor, (x, y+h), (x, y), border)
				pygame.draw.rect(self.background.convert_alpha(), emptyBackgroundColor, (x+border,y+border,w-border,h-border))
				
				unit = float(h)/100.
				rate = (self.ore_farmed/self.ore_hull_size) * 100
				
				y = y + h 
				h = unit * rate
				y -= h -1
				
				pygame.draw.line(self.background, lightColor, (x, y), (x+w-border, y), border)
				pygame.draw.rect(self.background, backgroundColor, (x,y,w,h))


				if entity_selected is not None:
					x, y = SCREEN_SIZE
					
					x = x - 220
					y = 20
					w = 200
					h = 30
					

					xtext = x + 20
					ytext = y + 20
					
					lines = []
					lines.append("Level: %d" % entity_selected.level)
					lines.append("Hit Points: %d/%d" % (entity_selected.health, entity_selected.max_health))
					lines.append("Experience: %d/%d" % (entity_selected.experience, self.exp_table[entity_selected.level]))
					lines.append("Death Blows: %d" % entity_selected.kills)
					lines.append("Ore Farmed: %d" % entity_selected.ore_farmed)
					lines.append("Speed: %d" % entity_selected.speed)
					
					'''
					if entity_selected.brain is not None: 
						lines.append("State: %s" % entity_selected.brain.active_state.name)
					'''
					
					'''Text Height'''
					for line in lines:
						htext = entity_selected.world.font.size('I')[1]
						h += htext + 10

					
					''' Frame 
					lightColor = (255, 229, 115)
					darkColor = (255, 207, 0)
					backgroundColor = (255, 219, 64)
					shadowColor = (80,80,80, 127)
					border = 2
					pygame.draw.rect(surface, shadowColor, (x+border+5,y+border+5,w-border,h-border))
					pygame.draw.line(surface, lightColor, (x, y), (x+w, y), border)
					pygame.draw.line(surface, darkColor, (x+w, y), (x+w, y+h), border)
					pygame.draw.line(surface, darkColor, (x+w, y+h), (x, y+h), border)
					pygame.draw.line(surface, lightColor, (x, y+h), (x, y), border)
					pygame.draw.rect(surface, backgroundColor, (x+border,y+border,w-border,h-border))
					''' 
					self.panel_image = pygame.image.load(os.path.join('ressources', 'panel.png')).convert_alpha()
					w, h = self.panel_image.get_size()
					surface.blit(self.panel_image, (x, y, w, h))
					
					for line in lines:
						text = entity_selected.world.font.render(line, 1, (166, 135, 0))
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
				self.location = Vector2(0, 0)
				self.destination = Vector2(0, 0)
				self.speed = 0.
				self.rotation_speed = 360.
				self.rotation = 0.
				self.level = 0
				self.experience = 0.
				self.selected = False
				self.selected_image = pygame.image.load(os.path.join('ressources', 'selected.png')).convert_alpha()
				self.health = 1
				self.max_health = 1
				self.kills = 0
				self.ore_farmed = 0
				self.exp_value = 100+ self.level* 100
				self.carrying = 0
				self.max_carrying = 0
				self.angle = 0.
				
				''' Attributes '''
				self.strength = 0

				
				''' Animation '''
				self.start = pygame.time.get_ticks()
				self.delay = 1000 / 10
				self.last_update = 0
				self.frame = 0
				
				self.images = image
				self.original_images = image
				self.image = self.images[self.frame]
				
				self.brain = StateMachine()
				
				self.id = 0
		

		def update(self, t):
			if t - self.last_update > self.delay:
				self.frame += 1
				if self.frame >= len(self.images):
					self.frame = 0
				self.image = self.images[self.frame]
				
				''' Heading Calculation '''
				x, y = self.location
				x2, y2 = self.destination
				Distance = Vector2.from_points(self.location, self.destination).get_magnitude()
				LowerDistance = Vector2.from_points(self.location, Vector2(x2, y)).get_magnitude()

				if Distance > 0:
					self.angle = degrees(acos(LowerDistance/Distance))
					self.image = pygame.transform.rotate(self.image, self.angle)

				self.last_update = t
		
		
		def select(self):
				for entity in self.world.entities.values():
						entity.selected = False
				
				self.selected = True
			
			
		def render(self, surface):
					
				x, y = self.location
				w, h = self.image.get_size()
				
				if self.world.show_bars is True:
					unit = float(25./100.)
					
					'''Level'''
					bar_x = x-(w/4)
					level = self.world.font.render('%s %s %s %s' % (str(self.level), self.angle, self.location, self.destination), 1, (255,255,255))
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
								
								
				if self.selected:
					ws, hs = self.selected_image.get_size()
					surface.blit(self.selected_image, (x-ws/2, (y+h/2)))
				surface.blit(self.image, (x-w/2, y-h/2))
				
				
		def process(self, time_passed):
				
				self.brain.think()
				
				if self.level > 0:
						if self.experience >= self.world.exp_table[self.level]:
							exceding = self.experience - self.world.exp_table[self.level]
							self.level_up(exceding)
				
				if self.speed > 0. and self.location != self.destination:
						vec_to_destination = self.destination - self.location				
						distance_to_destination = vec_to_destination.get_length()
						heading = vec_to_destination.get_normalized()
						travel_distance = min(distance_to_destination, time_passed * self.speed)
						self.location += travel_distance * heading

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
				
				
			
class Ant(GameEntity):
		
		def __init__(self, world, image):
				
				GameEntity.__init__(self, world, "ant", image)

				exploring_state = AntStateExploring(self)
				seeking_state = AntStateSeeking(self)
				delivering_state = AntStateDelivering(self)
				hunting_state = AntStateHunting(self)
				champ_hunting_state = AntStateChampHunting(self)
				mining_state = Mining(self)
							
				self.brain.add_state(exploring_state)
				self.brain.add_state(seeking_state)
				self.brain.add_state(delivering_state)
				self.brain.add_state(hunting_state)
				self.brain.add_state(champ_hunting_state)
				self.brain.add_state(mining_state)
				
				self.dead_image = pygame.transform.flip(image[0], 0, 1)
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

		def level_up(self, exceding):
			if self.level < 100:
				self.level += 1
				self.max_health += 1
				self.world.set_average_level()
				self.refill_life()
				if exceding > 0:
					self.experience = exceding
				else: 
					self.experience = 0 
			else: 
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
					self.world.ore_farmed += self.carrying
					self.ore_farmed += self.carrying
					self.experience += 300
					self.carrying = 0
					self.refill_life()
					self.strength += int(self.ore_farmed/100)+1
					
				
				if self.carry_image:
						x, y = self.location
						w, h = self.carry_image.get_size()
						#surface.blit(self.carry_image, (x-w, y-h/2))
						self.carry_image = None
						self.experience += 300
				
		def render(self, surface):
				self.update(pygame.time.get_ticks())
				GameEntity.render(self, surface)
				x, y = self.location
				w, h = self.image.get_size()
				
				if self.carry_image:
						x, y = self.location
						w, h = self.carry_image.get_size()
						surface.blit(self.carry_image, (x-w, y-h/2))
									
				
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
				
				champ = self.ant.world.get_close_entity("spider_champ", NEST_POSITION, NEST_SIZE)				
				if champ is not None:
						if self.ant.location.get_distance_to(champ.location) < 300.:
								self.ant.champ_id = champ.id
								return "champ_hunting"
							
				spider = self.ant.world.get_close_entity("spider", NEST_POSITION, NEST_SIZE)				
				if spider is not None:
						if self.ant.location.get_distance_to(spider.location) < 100.:
								self.ant.spider_id = spider.id
								return "hunting"
				
				return None
		
		def entry_actions(self):
				self.ant.speed = 120. + randint(-30, 30)
				self.random_destination()
				
				
class AntStateChampHunting(State):
		
		def __init__(self, ant):
				
				State.__init__(self, "champ_hunting")
				self.ant = ant
				self.got_kill = False
				
		def do_actions(self):
				
				champ = self.ant.world.get(self.ant.champ_id)
				
				if champ is None:
						return
				w,h = champ.image.get_size()

				self.ant.destination = champ.location
				
				if self.ant.location.get_distance_to(champ.location) < 90.:
						''' Stoping movements if we are in range '''
						
						if randint(1, 3) == 1:
								champ.bitten(self.ant)
								
								if champ.health <= 0:
										self.ant.carry(champ.image)								
										self.ant.world.remove_entity(champ)
										self.got_kill = True
										self.ant.kills += 1
										self.ant.experience += champ.exp_value
				
		def check_conditions(self):
				if self.ant.health <= int(self.ant.max_health/10):
						return "exploring"
				
				if self.got_kill:
						return "delivering"
				
				champ = self.ant.world.get(self.ant.champ_id)
												
				if champ is None:
						return "exploring"
				
				if champ.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 3:
						return "exploring"
				
				return None

		def entry_actions(self):
				
				self.speed = 160. + randint(0, 50)

		def exit_actions(self):
				
				self.got_kill = False
				
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

						if randint(1, 3) == 1:
								spider.bitten(self.ant)
								
								if spider.health <= 0:
										self.ant.carry(spider.image)								
										self.ant.world.remove_entity(spider)
										self.got_kill = True
										self.ant.kills += 1
										self.ant.experience += spider.exp_value
				
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
						
class SpiderChampion(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, 'spider_champ', image)
				self.almost_dead_image = pygame.image.load(os.path.join('ressources', 'alphabad-almost-dead.png')).convert_alpha()
				self.dead_image = self.almost_dead_image
				
				self.speed = 120. + randint(-20, 20)
				self.level = self.world.average_level + 5
				self.health = 50 + self.world.average_level*2
				self.max_health = self.health
				self.damage_done = 0
				self.exp_value = self.exp_value+1200*self.level*1000
				self.almost_dead = False
				
		def bitten(self, ant):
				
				self.health -= (ant.strength + 1)
				
				if randint(1, 5) == 1:
					ant.bitten()
					self.damage_done += 1
					
					if ant.health <= 0:
						self.kills += 1
						self.world.remove_entity(ant)
						self.world.set_average_level()
						
				''' Find a way to reswap original images '''
				if self.health > 0 and self.health < int(self.max_health/3):
						self.image = self.almost_dead_image
						self.almost_dead = True

				
				if self.health <= 0:
						self.speed = 0.
						self.image = self.dead_image
						ant.destination = self.location
						print "Fight report"
						print "Damage Done : %d" % self.damage_done
						print "Kills : %d" % self.kills
						print "Exp given : %d" % self.exp_value
						print 
				self.speed = 0.
				

				
		def render(self, surface):
				if self.almost_dead is False:
					self.update(pygame.time.get_ticks())
					
				GameEntity.render(self, surface)
								
				x, y = self.location
				w, h = self.image.get_size()
				
				unit = float(25./100.)
				
				'''Level'''
				bar_x = x-(w/4)
				level = self.world.font.render(str(self.level), 1, (255,255,255))
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
				

class Leaf(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "leaf", image)

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
							
							
class Ore(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "ore", image)
				self.health = 2500
				self.max_health = 2500
				
		def mined(self):
			self.health -= 1
			if self.health <= 0:
				self.image = self.world.background
				
		def render(self, surface):

				GameEntity.render(self, surface)
				if self.selected is True: 
					x, y = self.location
					w, h = self.image.get_size()
					bar_x = x - 25
					bar_y = y + h/2
					surface.fill( (255, 0, 0), (bar_x, bar_y, 50, 4))
					surface.fill( (0, 255, 0), (bar_x, bar_y, int((self.health/50)), 4))
				



			
class Spider(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "spider", image)
				self.dead_image = pygame.transform.flip(image[0], 0, 1)
				self.speed = 50. + randint(-20, 20)
				self.level = self.world.average_level
				self.health = 5 + self.world.average_level
				self.max_health = 5 + self.world.average_level
				self.exp_value = 600
				
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
				level = self.world.font.render(str(self.level), 1, (255,255,255))
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
		
		champion_images = []
		champion_images.append(pygame.image.load(os.path.join('ressources', 'alphabad-1.png')).convert_alpha()) 
		champion_images.append(pygame.image.load(os.path.join('ressources', 'alphabad-2.png')).convert_alpha()) 
		
		for ant_no in xrange(ANT_COUNT):
				ant = Ant(world, ant_image)
				ant.location = Vector2(randint(0, w), randint(0, h))
				ant.brain.set_state("exploring")
				world.add_entity(ant)
		
		
		while True:
				
				for event in pygame.event.get():
				
						if event.type == KEYDOWN:
							if event.key == K_p:
								world.paused = not world.paused
							if event.key == K_l:
								world.show_bars = not world.show_bars
								print world.show_bars
							if event.key == K_ESCAPE:
								return
						if event.type == QUIT:
								return				
						if event.type == MOUSEBUTTONDOWN:
								entity = world.get_clicked_entity(pygame.Rect(pygame.mouse.get_pos() + (4,4)))
								if entity is not None:
									entity.select()
									
									
				time_passed = clock.tick(30)			
				if world.paused is not True :
					
					
					
					if randint(1, 500) == 1:
							ore = Ore(world, ore_images[randint(0,5)])
							ore.location = Vector2(randint(0, w), randint(0, h))
							world.add_entity(ore)		
					'''		
					if randint(1, 50) == 1:			
						ant = Ant(world, ant_image)
						ant.location = Vector2(randint(0, w), randint(0, h))
						ant.brain.set_state("exploring")
						world.add_entity(ant)
					'''
					
			
					if randint(1, 500) == 1:
							champion = SpiderChampion(world, champion_images)
							champion.location = Vector2(randint(0, w), randint(0, h))
							random_offset = Vector2(randint(-NEST_SIZE/2, NEST_SIZE/2), randint(-NEST_SIZE/2, NEST_SIZE/2))
							champion.destination = Vector2(*NEST_POSITION) + random_offset
							world.add_entity(champion)			
					
																
					if randint(1, 100) == 1 and len(world.entities) < 100:
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
		
