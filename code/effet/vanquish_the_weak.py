from effect import Effect

class VanquishTheWeak(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,player,index):
		print("effet")
		player.move("BATTLE_ZONE",index,"GRAVEYARD")
