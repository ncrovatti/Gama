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