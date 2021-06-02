from effect import Effect

class RitualOfRejuvenation(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,player):
		print("effet")
		player.heal(4)