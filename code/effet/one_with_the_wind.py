from effect import Effect

class OneWithTheWind(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effect(self, creature):
    #Peut etre créer une fonction "enchant" dans creature card
    creature.get_evergreen().append_permanent_evergreen("flying")
    creature.add_bonus(2,2)

  def retire_effect(self, creature):
    #Peut etre créer une fonction "enchant" dans creature card
    creature.retire_enchantment("OneWithTheWind")
    creature.get_evergreen().pop("flying")
    creature.add_bonus(-2,-2)