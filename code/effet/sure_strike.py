from effect import Effect

class SureStrike(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effect(self, creature):
    creature.get_evergreen().append_tmp_evergreen("first_strike")
    creature.append_timed_bonuses(3, 0, 1)