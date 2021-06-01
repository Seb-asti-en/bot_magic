from effect import Effect

class Demystify(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)

       

  def effect(self,player,creature,name_enchantment):
    print("effet")
    for effect_creature in creature.get_effect():
      if effect_creature.get_name() == name_enchantment:
        effect_creature.retire_effect(effect_creature)



   