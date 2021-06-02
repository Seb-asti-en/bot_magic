from effect import Effect

class LightningStrike(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self, obj):
		obj.damage(3)