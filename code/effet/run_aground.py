from effect import Effect

class RunAground(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self, player, i):
		player.move("BATTLE_ZONE", i, "DECK")