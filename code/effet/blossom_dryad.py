from effect import Effect

class BlossomDryad(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)



	def effect(self, land):
		land.untap()