from effect import Effect
POWER = 0
TOUGHNESS = 1

class JungleDelver(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self,creature):
		print("effet")
		creature.add_bonus(1,1)