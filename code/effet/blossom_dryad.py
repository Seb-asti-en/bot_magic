from effect import Effect

class BlossomDryad(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)

       

  def effect(self,land):
    print("effet")
    land.untap()