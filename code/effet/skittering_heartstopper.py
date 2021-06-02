from effect import Effect

class SkitteringHeartstopper(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,creature):
		print("effet")
		creature.get_evergreen().append_tmp_evergreen("deathtouch")