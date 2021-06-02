from effect import Effect

class Demolish(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)



	def effect(self, player, i):
		player.move("LAND_ZONE", i, "GRAVEYARD")