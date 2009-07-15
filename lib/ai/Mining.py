				
class Mining(State):
		def __init__(self, ant):
				
				State.__init__(self, "mining")
				self.ant = ant
				self.max_charge = None
				
		def do_actions(self):
				
				ore = self.ant.world.get(self.ant.ore_id)
			
				if ore is None:
						return
					
				w,h = ore.image.get_size()			
				if self.ant.location.get_distance_to(ore.location) < w:
						
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
						self.ant.destination = ore.location - Vector2(w/2,h/2)
						self.ant.speed = 160. + randint(-20, 20)
							