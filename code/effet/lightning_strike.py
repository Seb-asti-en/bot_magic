from effect import Effect

class LightningStrike(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effect(self, obj):
    obj.damage(3)