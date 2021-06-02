from effect import Effect

class PullFromTomorrow(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,obj):
		print("effet")