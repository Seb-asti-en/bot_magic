from effect import Effect

class SkitteringHeartstopper(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)

       
  def effect(self,creature):
    print("effet")
    creature.get_evergreen().append_tmp_evergreen("deathtouch")