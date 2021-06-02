from effect import Effect

class FanBearer(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,creature):
		print("effet")
		creature.set_tapped(True)