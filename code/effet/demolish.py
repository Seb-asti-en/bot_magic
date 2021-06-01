from effect import Effect

class Demolish(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)



  def effect(self, player, i):
    player.move("LAND_ZONE", i, "GRAVEYARD")