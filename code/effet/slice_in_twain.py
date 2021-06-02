from effect import Effect

class SliceInTwain(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,obj):
		print("effet")