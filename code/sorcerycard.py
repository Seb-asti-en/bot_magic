from card import Card

#Variable global
ID 				= 0
NAME 			= 1
COLOR 			= 2
MANA_COST 		= 3
IDENTITY 		= 4
TEXT 			= 5
POWER 			= 6
TOUGHNESS 		= 7
TYPE 			= 8
SUBTYPE 		= 9
SUPERTYPE 		= 10
COLLECTION  	= 11

class SorceryCard(Card):

	def __init__(self, card, effect):
		super().__init__(card, effect)
		
	def to_string(self):
		string = super().to_string()
		return string
		