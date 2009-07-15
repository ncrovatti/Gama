class Spider(GameEntity):
		
		def __init__(self, world, image):
				GameEntity.__init__(self, world, "spider", image)
				self.dead_image = pygame.transform.flip(image[0], 0, 1)
				self.speed = 50. + randint(-20, 20)
				self.level = self.world.average_level
				self.health = 5 + self.world.average_level
				self.max_health = 5 + self.world.average_level
				
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