SCREEN_SIZE = (1280, 800)
NEST_POSITION = (320, 240)
GRID_SQUARE_SIZE = (32, 32)
ANT_COUNT = 20
NEST_SIZE = 200.

import os
import pygame
from pygame.locals import *
from math import sqrt, acos, degrees, atan2, ceil
from random import randint, choice, random
from gameobjects.vector2 import Vector2


def pos_to_coord(pos):				
		coord_x = pos[0] / GRID_SQUARE_SIZE[0]
		coord_y = pos[1] / GRID_SQUARE_SIZE[1]				
		return (int(coord_x), int(coord_y))

def coord_to_pos(coord):
		pos_x = coord[0] * GRID_SQUARE_SIZE[0]
		pos_y = coord[1] * GRID_SQUARE_SIZE[1]
		return (pos_x, pos_y)


class World(object):
		
		def __init__(self):
				self.font = pygame.font.SysFont('Arial', 14, True)
				
				self.entities = {}
				self.entities_count = {}
				self.exp_table = {}
				self.entity_id = 0	
				self.average_level = 1
				self.ore_hull_size = 100000.
				self.ore_farmed = 0.
				self.paused = False
				self.show_bars = False
				self.damages_done = 0
				self.grid = None
				
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
				
				self.explosion_images 			= self.load_sliced_sprites(16, 16, 'explosions-sprite.png')
				self.explosed_images 				= self.load_sliced_sprites(20, 20, 'explosed-sprite.png')
				self.small_explosed_images 	= self.load_sliced_sprites(17, 16, 'explosions-sprite3-10steps-w17xh16.png')
				self.attack_image 					= self.load_sliced_sprites(6, 9, 'bullet-sprite.png')
				
				self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
				self.background.fill((255, 255, 255))
				pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))
	
		def load_sliced_sprites(self, w, h, filename):
				'''
				Sample 5 frames Sprite representation:
				------------------------------------------
				l   1    l   2   l   3   l   4   l   5   l
				l 16x16  l 16x16 l 16x16 l 16x16 l 16x16 l
				l        l       l       l       l       l
				------------------------------------------
				Specs : 
					Master can be any height.
					Sprites frames width must be the same width
					Master width must be len(frames)*frame.width
				'''
				images = []
				master_image = pygame.image.load(os.path.join('ressources', filename)).convert_alpha()

				master_width, master_height = master_image.get_size()
				for i in xrange(int(master_width/w)):
					images.append(master_image.subsurface((i*w,0,w,h)))
				return images
			
		def add_entity(self, entity):

				self.entities[self.entity_id] = entity
				entity.id = self.entity_id
				self.entity_id += 1
				
		def remove_entity(self, entity):
				''' Unlocking Square '''
				loc = self.grid.get(pos_to_coord(entity.location))
				if loc is not None:
						loc.blocked = False
						loc.locked_by = None
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
				
				''' 
				Ugly Fix, was : 
				for entity in self.entities.itervalues():
				RuntimeError: dictionary changed size during iteration
				'''
				for id in self.entities.keys():
						entity = self.get(id)
						if entity.selected is True: entity_selected = entity
						entity.render(surface)

				''' Ore tank ''' 
				'''
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
				pygame.draw.rect(surface, shadowColor, (x+border+shadowMargin,y+border+shadowMargin,w-border,h-border))
				pygame.draw.line(surface, lightColor, (x, y), (x+w, y), border)
				pygame.draw.line(surface, darkColor, (x+w, y), (x+w, y+h), border)
				pygame.draw.line(surface, darkColor, (x+w, y+h), (x, y+h), border)
				pygame.draw.line(surface, lightColor, (x, y+h), (x, y), border)
				pygame.draw.rect(surface, emptyBackgroundColor, (x+border,y+border,w-border,h-border))
				
				unit = float(h)/100.

				rate = (self.ore_farmed/self.ore_hull_size) * 100
				
				y = y + h 
				h = unit * rate
				y -= h -1
				
				pygame.draw.line(surface, lightColor, (x, y), (x+w-border, y), border)
				pygame.draw.rect(surface, backgroundColor, (x,y,w,h))
				'''
				
				
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
					lines.append("Strength: %d" % entity_selected.strength)
					
					'''
					if entity_selected.brain is not None: 
						lines.append("State: %s" % entity_selected.brain.active_state.name)
					'''
					
					'''Text Height'''
					for line in lines:
						htext = entity_selected.world.font.size('I')[1]
						h += htext + 10

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

		def get_entity_count_by_name(self, name):
				i = 0
				for entity in self.entities.itervalues():						
						if entity.name == name:
								i += 1
				return i

		def set_average_level(self):
				i = 0
				total_level = 0
				for entity in self.entities.itervalues():						
						if entity.name == 'ant':
								i += 1			
								total_level += entity.level
				
				if i > 0:
					self.average_level = int(total_level/i)
				else:
					print "Game Over"		
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
				self.pause = False
				self.static = False
				self.route = None
				self.heading = Vector2(0, 0)
				self.decorative = False
				self.name = name
				self.location = Vector2(0, 0)
				self.move(Vector2(0, 0))
				self.speed = 0.
				self.rotation_speed = 360.
				self.rotation = 0.
				self.level = 0
				self.experience = 0.
				self.selected = False
				self.haste = 1000/30
				self.selected_image = pygame.image.load(os.path.join('ressources', 'selected.png')).convert_alpha()
				self.attack_image = self.world.attack_image
				
				self.health = 1
				self.max_health = 1
				self.kills = 0
				self.ore_farmed = 0
				self.exp_value = 100+ self.level* 100
				self.carrying = 0
				self.max_carrying = 0
				self.angle = 0.
				self.damages_done = 0
				
				''' Attributes '''
				self.strength = 0

				
				''' Animation '''
				self.start = pygame.time.get_ticks()
				self.delay = 1000 / 30
				
				self.last_update = 0
				self.frame = 0
				
				self.images = image
				self.original_images = image
				self.image = self.images[self.frame]
				
				w,h = self.image.get_size()
				self.diameter = sqrt(w**2 + h**2)/2
				self.block_area = ceil(self.diameter/GRID_SQUARE_SIZE[0])
				
				self.brain = StateMachine()
				
				self.id = 0
				
		def move(self, destination):
			self.route = None
			loc = pos_to_coord(destination)
			x, y = coord_to_pos(loc)
			x += GRID_SQUARE_SIZE[0]/2
			y += GRID_SQUARE_SIZE[1]/2
			self.destination = Vector2(*(x,y)) 
			
		def attack_animation(self, target): 
			if self.world.get_entity_count_by_name('bullet') < 5:
				bullet = Bullet(self.world, self.attack_image)
				
				radius = int(self.diameter/2)
				target_radius = int(target.diameter/2)
			
				bullet.location = Vector2(*self.location) + Vector2(randint(-radius, radius), randint(-radius, radius))
				bullet.move(Vector2(*target.location) + Vector2(randint(-target_radius, target_radius), randint(-target_radius, target_radius)))
				self.world.add_entity(bullet)
		
		def explosed_animation(self, target, images=False, scale=1): 
			if images is False:
				images = self.world.explosed_images
				
			explosion = Explosion(self.world, images)
			explosion.location = Vector2(*target.location)			
			explosion.move(Vector2(*target.location))
			explosion.doublescale = scale
			self.world.add_entity(explosion)
			
		def explosion_animation(self, target): 

			if self.world.get_entity_count_by_name('explosion') < 10:
				explosion = Explosion(self.world, self.world.explosion_images)
				radius = int(target.diameter/2)
				explosion.parent = target
				explosion.location = Vector2(*target.location) + Vector2(randint(-radius, radius), randint(-radius, radius))
				explosion.move(Vector2(*target.destination) + Vector2(randint(-radius, radius), randint(-radius, radius)))
				explosion.speed = target.speed
				self.world.add_entity(explosion)
			
			
		def face(self):
				''' Heading Calculation '''
				x1, y1 = self.location
				''' Needs work to take into account sub destinations'''
				x2, y2 = self.destination

				rad_angle = atan2((x2-x1), (y2-y1)) 
				self.angle = degrees(rad_angle)
				self.image = pygame.transform.rotate(self.image, self.angle)
						
					
		def experience_attribution(self, killed_unit):
			exp_per_hp = int(killed_unit.exp_value/killed_unit.max_health)

			''' Distributing XP based on damage done '''
			for id in killed_unit.shit_list:
				unit = killed_unit.world.get(id)
				
				''' Some units might have died '''
				if unit is not None:
					unit.experience += unit.damages_done * exp_per_hp
					print "Unit #%d is gain : %d (%d damages done)" % (unit.id, unit.damages_done * exp_per_hp, unit.damages_done)
					unit.damages_done = 0

		def update(self, t):
			
			if t - self.last_update > self.delay:
				self.frame += 1
				if self.frame >= len(self.images):
					self.frame = 0
				self.image = self.images[self.frame]
				
				''' updating diameter because surface size might have changed after rotation'''
				w,h = self.image.get_size()
				self.diameter = sqrt(w**2 + h**2)/2
				
				self.face()

				self.last_update = t
		
		
		def select(self):
				for entity in self.world.entities.values():
						entity.selected = False
				
				self.selected = True
			
			
		def render(self, surface):
					
				x, y = self.location
				w, h = self.image.get_size()
				
				if self.route:
					''' 
						FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU 
						Well, the pathfinding was working but x and y were overwriten here
						FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
					
					i = 0
					for coord in self.route:
							xc, yc = coord_to_pos(coord)
							xc += GRID_SQUARE_SIZE[0] / 2
							yc += GRID_SQUARE_SIZE[1] / 2
							#pygame.draw.circle(surface, (0, 255, 0), (x, y), 3)
							level = self.world.font.render(str(i), 1, (255,255,0))
							surface.blit(level, (xc, yc))
							i +=1
				'''
				if self.world.show_bars is True and self.decorative is False:
					pygame.draw.aaline(surface, (255,255,255), self.location, self.destination, 1)
					
					unit = float(25./100.)
					'''Level'''
					bar_x = x-(w/4)
					level = self.world.font.render('%s' % str(self.id), 1, (255,255,255))
					w2,h2 = level.get_size()
					bar_y = y - h/2 
					surface.blit(level, (bar_x, bar_y, w2,h2))
					
					'''Level'''
					bar_x = x-(w/4)
					level = self.world.font.render('%s' % str(self.level), 1, (255,255,255))
					w2,h2 = level.get_size()
					bar_y = y - h 
					surface.blit(level, (bar_x, bar_y, w2,h2))
					'''
					bar_x = x-(w/4)
					level = self.world.font.render('%s %s %s %s' % (str(self.level), self.angle, self.location, self.destination), 1, (255,255,255))
					w2,h2 = level.get_size()
					bar_y = y - h 
					surface.blit(level, (bar_x, bar_y, w2,h2))
					'''
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
				
				steps = ( (0,	+1), (+1,	0), (0,	-1), (-1,	0 ),
								(+1, -1), (+1, +1), (-1, +1), (-1, -1) )
				self.brain.think()
				
				if self.level > 0:
						if self.experience >= self.world.exp_table[self.level]:
							exceding = self.experience - self.world.exp_table[self.level]
							self.level_up(exceding)
							
				''' 
				Might changes Rules to pathfind the nearest square 
				if the one we want to stop on if already taken
				'''
				if self.speed > 0. and self.location != self.destination and not self.decorative:
					from_loc 		= pos_to_coord(self.location)
					to_loc 			= pos_to_coord(self.destination)
					loc_square 	= self.world.grid.get(from_loc)

					if loc_square is not None:
						if loc_square.blocked is True and loc_square.locked_by != self.id:
							self.route = self.world.grid.find_route(from_loc, to_loc)
						else:					
							loc_square 	= self.world.grid.get(from_loc)
							loc_square.unblock()
							'''
							x,y = from_loc 
							for step  in xrange(self.block_area):
								coord = (x+steps[step][0],y+steps[step][1])
								loc_square 	= self.world.grid.get(coord)
								x,y = coord
								if loc_square is not None:
									loc_square.unblock()
							'''
					''' Default movement '''
					vec_to_destination 				= self.destination - self.location				
					distance_to_destination 	= vec_to_destination.get_length()
					self.heading 							= vec_to_destination.get_normalized()
					travel_distance 					= min(distance_to_destination, time_passed * self.speed)

					''' Overwriting default movement if we have a route ''' 

					if self.route :
						''' Repositioning in sprite to Square center ''' 
						x_dest, y_dest = coord_to_pos(self.route[0])
						x_dest += GRID_SQUARE_SIZE[0]/2
						y_dest += GRID_SQUARE_SIZE[1]/2
						
						''' Affecting new destination '''
						destination 							= Vector2(*(x_dest, y_dest))
						vec_to_destination 				= destination - self.location
						distance_to_destination 	= vec_to_destination.get_length()
						
						if distance_to_destination == 0. : return
						 
						self.heading 							= vec_to_destination.get_normalized()
						
						if self.speed * time_passed > distance_to_destination:
								travel_distance 			= distance_to_destination
								self.route 						=	self.route[1:]
								if len(self.route) == 0 : self.route = None
						else:
								travel_distance 			= self.speed * time_passed
					
					self.location += travel_distance * self.heading
					
					from_loc 		= pos_to_coord(self.location)
					loc_square 	= self.world.grid.get(from_loc)
					if loc_square is not None:
						loc_square.block(self)
					
					'''
					x,y = from_loc 
					for step  in xrange(self.block_area):
						coord = (x+steps[step][0],y+steps[step][1])
						loc_square 	= self.world.grid.get(coord)
						x,y = coord
						if loc_square is not None:
							loc_square.block(self)
					'''

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
				self.delay = 1000 / 30
				
				self.kills = 0
				self.explosed_images = self.world.load_sliced_sprites(33, 31, 'explosions-sprite2-12steps-w33xh31.png')
				
				''' Experience '''
				self.experience = 0
				self.level = 1

		def refill_life(self):
				self.health = self.max_health

		def level_up(self, exceding):
			if self.level < 100:
				self.level += 1
				self.max_health += 1 + 2 * self.level
				self.strength += 2
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

		def bitten(self, unit):
				
				self.health -= (unit.strength + 1)
				if self.health <= 0:
						self.explosed_animation(self, self.explosed_images)
						self.speed = 0.
						self.image = self.dead_image



		def drop(self, surface):
				if self.carrying > 0:
					if self.world.ore_farmed <= self.world.ore_hull_size:
						self.world.ore_farmed += self.carrying
						self.ore_farmed += self.carrying
					self.experience += 300
					self.carrying = 0
					self.refill_life()

				
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
				self.ant.move(Vector2(*NEST_POSITION) + random_offset)
			 
			
class AntStateExploring(State):
		
		def __init__(self, ant):
				
				State.__init__(self, "exploring")
				self.ant = ant
				
		def random_destination(self):
				
				w, h = SCREEN_SIZE
				self.ant.move(Vector2(randint(0, w), randint(0, h)))		
		
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

				if self.ant.location.get_distance_to(champ.location) < champ.diameter:
						''' Stoping movements if we are in range '''
						self.ant.move(self.ant.location)
						self.ant.attack_animation(champ)
						
						#print "I'm in range : %s" % champ.diameter
						if randint(1, 3) == 1:
								self.ant.explosion_animation(champ)
								champ.bitten(self.ant)
								
								if champ.health <= 0:
										self.ant.explosed_animation(champ)
										self.ant.world.remove_entity(champ)
										self.got_kill = True
										self.ant.kills += 1
										champ.experience_attribution(champ)
				else:
					#print "I'm not in range : %s" % champ.diameter
					# moving to champs location 
					self.ant.move(champ.location)
				
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
						
				self.ant.move(spider.location)

				if self.ant.location.get_distance_to(spider.location) < spider.diameter*3:
					
						self.ant.attack_animation(spider)

						if randint(1, 3) == 1:
								self.ant.explosion_animation(spider)
								spider.bitten(self.ant)
								
								if spider.health <= 0:
										self.ant.explosed_animation(spider)
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
				
				if self.ant.location.get_distance_to(leaf.location) < 50.0:
				
						self.ant.carry(leaf.image)
						self.ant.world.remove_entity(leaf)
						return "delivering"
				
				return None
		
		def entry_actions(self):
		
				leaf = self.ant.world.get(self.ant.leaf_id)
				if leaf is not None:												
						self.ant.move(leaf.location)
						self.ant.speed = 160. + randint(-20, 20)
						
class SpiderChampion(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, 'spider_champ', image)
				self.almost_dead_image = pygame.image.load(os.path.join('ressources', 'alphabad-almost-dead.png')).convert_alpha()
				self.dead_image = self.almost_dead_image
				
				self.speed = 120. + randint(-20, 20)
				self.level = self.world.average_level + randint(5, 10)
				self.health = self.world.average_level * self.world.average_level * 2
				self.max_health = self.health
				self.damage_done = 0
				self.strength = int(self.world.average_level/4)
				self.exp_value = self.exp_value+1200*self.level*1000
				self.almost_dead = False
				self.shit_list = {}
				self.delay = 1000 / 60
				
		def bitten(self, ant):
				
				if ant.id not in self.shit_list:
					self.shit_list[ant.id] = 1

				damages = (ant.strength + 1)
				ant.damages_done += damages
				self.health -= damages

				if randint(1,6) is 1:
					ant.bitten(self)
					self.damages_done += (self.strength + 1)

				if ant.health <= 0:
					self.kills += 1
					self.world.remove_entity(ant)
					self.world.set_average_level()

				if self.health > 0 and self.health < int(self.max_health/3):
						self.image = self.almost_dead_image
						self.face()
						self.almost_dead = True
						if self.location == self.destination:
							w,h = SCREEN_SIZE
							self.move(Vector2(randint(w, w+100), randint(h, h+100)))
							self.speed = 170.

				if self.health <= 0:
						self.speed = 0.
						self.image = self.dead_image
						ant.move(self.location)
						print "Fight report"
						print "Damage Done : %d" % self.damages_done
						print "Kills : %d" % self.kills
						print "Exp given : %d to %d attackers" % (self.exp_value, len(self.shit_list))
						print 
				

				
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

class Explosion(GameEntity):
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "explosion", image)
				self.decorative = True
				self.doublescale = randint(0,2) 
				self.delay = 1000 / 60
				
		def update(self, t):
			if t - self.last_update > self.delay:
				self.frame += 1
				''' Remove self after one loop '''
				if self.frame >= len(self.images):
					self.frame = 0
					self.world.remove_entity(self)
		
				self.image = self.images[self.frame]
				
				modifier = 1
				w,h = self.image.get_size()
				if self.doublescale is 1:
					modifier = 2 
					modifier += random()
					
				if self.doublescale is 2:
					modifier += random()
					
				self.image = pygame.transform.smoothscale(self.image, (w*modifier, h*modifier))
					
				self.last_update = t

				
		def render(self, surface):
			#if self.parent is not None and self.world.get(self.parent.id) is not None:
				self.update(pygame.time.get_ticks())
				GameEntity.render(self, surface)

class Bullet(GameEntity):
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "bullet", image)
				self.decorative = True
				self.speed = 200.
				self.delay = 1000 / 30 
				
		def update(self, t):
			if t - self.last_update > self.delay:
				self.frame += 1
				if self.frame >= len(self.images):
					self.frame = 0
		
				self.image = self.images[self.frame]
				self.last_update = t
				
		def process(self, time_passed):
			self.update(pygame.time.get_ticks())
			if self.location == self.destination:
				self.world.remove_entity(self)
				
			GameEntity.process(self, time_passed)
				
				
class Building(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "building", image)
				self.static = True
				self.speed = 0
				self.delay = 1000/2
				
		
		def render(self, surface):
			self.update(pygame.time.get_ticks())
			GameEntity.render(self, surface)
				
class Leaf(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "leaf", image)
				self.decorative = True
							
							
class Mining(State):
		def __init__(self, ant):
				
				State.__init__(self, "mining")
				self.ant = ant
				self.max_charge = None
				
		def do_actions(self):
				
				ore = self.ant.world.get(self.ant.ore_id)
			
				if ore is None:
						return
					
				self.ant.move(ore.location)
				
				if self.ant.location.get_distance_to(ore.location) < ore.diameter:
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
						self.ant.move(ore.location - Vector2(w/2,h/2))
						self.ant.speed = 160. + randint(-20, 20)
							
							
class Ore(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "ore", image)
				self.health = 2500
				self.max_health = 2500
				self.decorative = True
				
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
				self.health = 10 + int(self.world.average_level*2)
				self.max_health = self.health
				self.exp_value = 600
				
		def bitten(self, ant):
				damages = (ant.strength + 1)
				ant.damages_done += damages
				self.health -= damages
				
				if randint(1, 6) == 1:
					ant.bitten(self)
					if ant.health <= 0:
						self.world.remove_entity(ant)
						self.world.set_average_level()
						
				if self.health <= 0:
						self.speed = 0.
						self.image = self.dead_image
				self.speed = 140.
				
		def render(self, surface):
				self.update(pygame.time.get_ticks())
				GameEntity.render(self, surface)
				
		def process(self, time_passed):
				
				x, y = self.location
				if x > SCREEN_SIZE[0] + 2:
						self.world.remove_entity(self)
						return
				
				GameEntity.process(self, time_passed)
				
				

class Square(object):
		
		def __init__(self, coord):
				
				self.coord = coord
				self.blocked = False
				self.locked_by = None
				self.parent = None
				self.marked = False		
				
		def reset(self):
				self.parent = None
		
		def block(self, unit):
				self.blocked = True
				self.locked_by = unit.id
 
		def unblock(self):
				self.blocked = False
				self.locked_by = None
 


class Grid(object):
		
		def __init__(self, world, width, height):
				self.world = world
				self.width = width
				self.height = height
				w,h = SCREEN_SIZE
				self.layer = pygame.Surface((w,h))
				self.layer.convert_alpha() # give it some alpha values
				self.layer.set_colorkey((0,0,0))
				self.layer.fill((0, 0, 0, 0)) # fill it with black translucent
				self.layer.set_alpha(255)
				
				self.rows = []
				for row in xrange(height):						
						row_squares = []						
						for col in xrange(width):								
								row_squares.append( Square((col, row)) )
						self.rows.append(row_squares)								
				
		def get(self, coord):
				
				if not self.is_valid_coordinate(coord):
						return None
				x, y = coord
				return self.rows[int(y)][int(x)]
		
		def set(self, coord, blocked):
				
				if self.is_valid_coordinate(coord):
						x, y = coord
						self.rows[y][x] = blocked
		
		def is_valid_coordinate(self, coord):
				
				x, y = coord
				if x < 0 or y < 0 or x >= self.width or y >= self.height:
						return False
				return True

		def reset(self):
				
				for row in self.rows:
						for square in row:
								square.reset()
		
				
		def find_route(self, start_coord, dest_coord):
				
				self.reset()
				
				visited = set()
				open_squares = []
				
				open_squares.append(start_coord)		
				
				steps = ( (0,	+1), (+1,	0), (0,	-1), (-1,	0 ),
									(+1, -1), (+1, +1), (-1, +1), (-1, -1) )
				
				while open_squares:
						
						coord = open_squares.pop(0)				
						
						if coord == dest_coord:
								path = []						
								while coord != start_coord:
										path.append(coord)
										square = self.get(coord)								
										parent_square = self.get(square.parent)
										coord = square.parent								
								return path[::-1]
		 
						for step in steps:
								
								new_coord = (coord[0]+step[0], coord[1]+step[1])
								
								if new_coord in visited:
										continue
								
								visited.add(new_coord)						
								square = self.get(new_coord)
								
								if square is None or square.blocked:
										continue
								
								self.get(new_coord).parent = coord
								open_squares.append(new_coord)
								
				return None
		

		def render(self, surface, block_surface):
			self.layer.fill((0,0,0,0))
			self.layer.set_alpha(200)

			if self.world.show_bars is not True: return

			for y in xrange(self.height):
					for x in xrange(self.width):	
							coord = (x, y)
							render_x = x * GRID_SQUARE_SIZE[0]
							render_y = y * GRID_SQUARE_SIZE[1]
							points = ((render_x,render_y), (render_x+GRID_SQUARE_SIZE[0],render_y),(render_x+GRID_SQUARE_SIZE[0],render_y+GRID_SQUARE_SIZE[1]), (render_x,render_y+GRID_SQUARE_SIZE[1]))
							
							if self.get(coord).blocked:
								pygame.draw.circle(self.layer, (255,255,0,127), (render_x+GRID_SQUARE_SIZE[0]/2, render_y+GRID_SQUARE_SIZE[1]/2), GRID_SQUARE_SIZE[0]/2, 1)
							
							pygame.draw.polygon(self.layer, (0,170,255,127), points, 1)				
			surface.blit(self.layer, (0, 0))

								
		
def run():
		#GameInit()
		pygame.init()
		screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
		#pygame.display.toggle_fullscreen()
		world = World()

		Background = world.ground_images[4]
		graphRect = world.ground_images[1].get_rect()

		w, h = SCREEN_SIZE
		world.grid = Grid(world, (w/GRID_SQUARE_SIZE[0])+1, (h/GRID_SQUARE_SIZE[1])+1)
		
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
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	5,	6,	7,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	5,	6,	9,	3,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	10,	6,	6,	7,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	10,	11,	12],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	1,	2,	3,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	5,	6,	7,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	5,	6,	9,	3,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	10,	6,	6,	7,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	10,	11,	12,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	1,	2,	3,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	5,	6,	7,	4,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	5,	6,	9,	3,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	10,	6,	6,	7,	4,	4,	4,	4,	4,	4],
			[4,	4,	4,	4,	4,	4,	4,	4,	4,	10,	11,	12,	4,	4,	4,	4,	4,	4],
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
		bgStr = pygame.image.tostring(screen, 'RGBA')

		world.background = pygame.image.fromstring(bgStr, SCREEN_SIZE, 'RGBA').convert_alpha()
		
		base_images = world.load_sliced_sprites(113, 145, 'collony-base-1step-w113xh145.png')

		base = Building(world, base_images)
		base.location = Vector2(*NEST_POSITION)
		world.add_entity(base)
		
		clock = pygame.time.Clock()
		
		ant_image = world.load_sliced_sprites(21, 28, 'collony-member-2steps-w21xh28.png')
		
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
								ore = Ore(world, ore_images[randint(0,5)])
								ore.location = Vector2(*pygame.mouse.get_pos())
								world.add_entity(ore)		
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
					
			
					if randint(1, 200) == 1:
							champion = SpiderChampion(world, champion_images)
							champion.location = Vector2(randint(0, w), randint(0, h))
							random_offset = Vector2(randint(-NEST_SIZE/2, NEST_SIZE/2), randint(-NEST_SIZE/2, NEST_SIZE/2))
							champion.move(Vector2(*NEST_POSITION) + random_offset)
							world.add_entity(champion)			
					
																
					if randint(1, 100) == 1 and len(world.entities) < 100:
							leaf = Leaf(world, leaf_image)
							leaf.location = Vector2(randint(0, w), randint(0, h))
							world.add_entity(leaf)
							
					if randint(1, 50) == 1:
							spider = Spider(world, spider_image)
							spider.location = Vector2(-50, randint(0, h))
							spider.move(Vector2(w+50, randint(0, h)))						
							world.add_entity(spider)
					
					world.process(time_passed)
				
				world.render(screen)
				world.grid.render(screen, None)	
				pygame.display.update()
		
if __name__ == "__main__":		
		run()
		
