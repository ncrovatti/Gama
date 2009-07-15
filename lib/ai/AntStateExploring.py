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