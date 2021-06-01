from effect import Effect

class RitualOfRejuvenation(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)

       
  def effect(self,player):
    print("effet")
    player.heal(4)