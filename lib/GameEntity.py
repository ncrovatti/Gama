
class GameEntity(object):
		
		def __init__(self, world, name, image):
				
				self.world = world
				self.name = name
				self.location = Vector2(0, 0)
				self.destination = Vector2(0, 0)
				self.speed = 0.
				self.level = 0
				self.experience = 0.
				self.selected = False
				self.selected_image = pygame.image.load(os.path.join('ressources', 'selected.png')).convert_alpha()
				self.health = 0
				self.max_health = 0
				self.kills = 0
				self.ore_farmed = 0
				
				''' Animation '''
				self.start = pygame.time.get_ticks()
				self.delay = 1000 / 10
				self.last_update = 0
				self.frame = 0
				
				self.images = image
				self.image = self.images[self.frame]
				
				self.brain = StateMachine()
				
				self.id = 0
		

		def update(self, t):
			if t - self.last_update > self.delay:
				self.frame += 1
				if self.frame >= len(self.images):
					self.frame = 0
				self.image = self.images[self.frame]
				self.last_update = t
		
		
		def select(self):
				for entity in self.world.entities.values():
						entity.selected = False
				
				self.selected = True
			
			
		def render(self, surface):
				self.update(pygame.time.get_ticks())	
				x, y = self.location
				w, h = self.image.get_size()
				
				if self.selected:
					ws, hs = self.selected_image.get_size()
					surface.blit(self.selected_image, (x-ws/2, (y+h/2)))
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
						'''
						w,h = self.image.get_size()
						diameter = sqrt(w*w + h*h)
						print diameter
						if self.world.get_close_entity('ant', self.destination, diameter) is not None:
							w, h = SCREEN_SIZE
							self.destination = Vector2(randint(0, w), randint(0, h))
							print "moving out to %s" % str(self.destination)
						'''		
						vec_to_destination = self.destination - self.location				
						distance_to_destination = vec_to_destination.get_length()
						heading = vec_to_destination.get_normalized()
						travel_distance = min(distance_to_destination, time_passed * self.speed)
						self.location += travel_distance * heading
