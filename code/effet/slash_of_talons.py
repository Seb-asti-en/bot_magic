from effect import Effect

class SlashOfTalons(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self, creature):
		creature.damage(2)