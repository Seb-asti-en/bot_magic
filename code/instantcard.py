from card import Card

class InstantCard(Card):

	def __init__(self, card):
		super().__init__(card)
	
	def to_string(self):
		string = super().to_string()
		return string
		