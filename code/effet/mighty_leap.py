from effect import Effect

class MightyLeap(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self, creature):
		creature.append_timed_bonuses(2,2,1)
		creature.get_evergreen().append_tmp_evergreen("flying")
