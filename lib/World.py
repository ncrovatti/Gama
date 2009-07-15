		
class World(object):
		
		def __init__(self):
				
				self.font = pygame.font.SysFont('Arial', 12, False)
				
				self.entities = {}
				self.exp_table = {}
				self.entity_id = 0	
				self.average_level = 1
				self.ore_hull_size = 100000.
				self.ore_farmed = 0.
				
				for i in xrange(0, 101):
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
	