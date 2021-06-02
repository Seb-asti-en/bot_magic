from effect import Effect

class PainfulLesson(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,player):
		print("effet")
		player.damage(2)