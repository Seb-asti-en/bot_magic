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

class InstantCard(Card):

	def __init__(self, card):
		super().__init__(card)
	
	def to_string(self):
		string = super().to_string()
		return string

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)
