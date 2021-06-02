from effect import Effect

class MiasmicMummy(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self, all_player,i):
		for player in all_player:
			player.move("HAND", i, "GRAVEYARD")