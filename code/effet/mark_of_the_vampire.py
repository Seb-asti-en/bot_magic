from effect import Effect

class MarkOfTheVampire(Effect):

	def __init__(self,name,target,temporality, activable):
		super().__init__(name,target,temporality, activable)


	def effect(self, creature):
		#Peut etre créer une fonction "enchant" dans creature card
		creature.append_enchantment("MarkOfTheVampire")
		creature.get_evergreen().append_permanent_evergreen("lifelink")
		creature.bonus(2,2)
	
	
	def retire_effect(self, creature):
		#Peut etre créer une fonction "enchant" dans creature card
		creature.retire_enchantment("MarkOfTheVampire")
		creature.get_evergreen().pop("lifelink")
		creature.add_bonus(-2,-2)