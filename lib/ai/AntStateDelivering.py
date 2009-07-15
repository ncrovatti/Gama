				
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
			 