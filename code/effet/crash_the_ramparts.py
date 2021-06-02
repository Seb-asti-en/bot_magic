from effect import Effect

class CrashTheRamparts(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)



	def effect(self,creature):
		print("effet")
		creature.append_timed_bonuses(3,3,1)
		creature.get_effect().append_tmp_evergreen("trample")
