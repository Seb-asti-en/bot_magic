from effect import Effect

class BlightKeeper(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)



	def effect(self,player_self, player_oponent):
		player_oponent.damage(4)
		player_self.heal(4)