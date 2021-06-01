from effect import Effect

class Electrify(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effect(self, creature):
    creature.damage(4)