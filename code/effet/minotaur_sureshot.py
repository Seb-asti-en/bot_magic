from effect import Effect

class MinotaurSureshot(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,creature):
		print("effet")
		creature.append_timed_bonuses(1,0,1)