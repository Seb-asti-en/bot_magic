from effect import Effect

class DrawCard(Effect):

  def __init__(self,name,target,temporality,x):
    super().__init__(name,target,temporality)
    self.nb_card = x

       
  def effect(self,player):
    player.draw_card(self.nb_card)  
    