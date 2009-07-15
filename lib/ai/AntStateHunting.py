				
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
										self.ant.kills += 1
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