from effect import Effect

class SplendidAgony(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effect(self, creature):
    creature.add_bonus(-1,-1)