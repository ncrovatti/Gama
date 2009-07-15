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
					self.world.ore_farmed += self.carrying
					self.ore_farmed += self.carrying
					self.experience += 300
					self.carrying = 0
					
				
				if self.carry_image:
						x, y = self.location
						w, h = self.carry_image.get_size()
						#surface.blit(self.carry_image, (x-w, y-h/2))
						self.carry_image = None
						self.experience += 300
				
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