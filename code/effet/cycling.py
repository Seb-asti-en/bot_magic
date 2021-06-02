from effect import Effect

class Cycling(Effect):

	def __init__(self,name,target,temporality, activable,x):
		super().__init__(name,target,temporality, activable)
		self.nb_card = x


	def effect(self,player):
		player.draw_card(self.nb_card)
