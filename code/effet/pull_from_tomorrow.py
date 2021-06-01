from effect import Effect

class PullFromTomorrow(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)

       
  def effect(self,obj):
    print("effet")