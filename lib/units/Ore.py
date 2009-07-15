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
				
