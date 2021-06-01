from effect import Effect

class MightyLeap(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effet(self, creature):
    creature.append_timed_bonuses(2,2,1)
    creature.get_evergreen().append_tmp_evergreen("flying")