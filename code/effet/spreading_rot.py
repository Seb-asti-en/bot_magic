from effect import Effect

class SpreadingRot(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,player,index):
		print("effet")
		player.move("BATTLE_ZONE",index,"GRAVEYARD")
		player.damage(2)