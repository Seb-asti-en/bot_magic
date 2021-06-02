class Board:

	############################ Constructeur ############################
	def __init__(self,deck):
		self.__deck = deck
		self.__hand = []
		self.__battle_zone = []
		self.__land_zone = []
		self.__graveyard = []
		self.__exile = []

	############################ Getters ############################
	
	def get_deck(self):
		return self.__deck
	
	def get_hand(self):
		return self.__hand

	def get_battle_zone(self):
		return self.__battle_zone
	
	def get_land_zone(self):
		return self.__land_zone
	
	def get_graveyard(self):
		return self.__graveyard

	def get_exile(self):
		return self.__exile

	############################ Setters ############################
	
	def set_deck(self,deck):
		self.__deck = deck
	
	def set_hand(self,hand):
		self.__hand = hand

	def set_battle_zone(self,battle_zone):
		self.__battle_zone = battle_zone
	
	def set_land_zone(self,land_zone):
		self.__land_zone = land_zone
	
	def set_graveyard(self,graveyard):
		self.__graveyard = graveyard

	def set_exile(self,exile):
		self.__exile = exile

	############################ Méthode ############################

	##
	# Fonction qui ajoute une carte dans la main du joueur
	# @param	Card	La carte que l'on ajoute a la main
	##
	def add_hand(self,Card):
		self.__hand.append(Card)
		
	##
	# Fonction qui defausse la main du joueur
	##
	def empty_hand(self):

		card = None

		while len(self.__hand) > 0:
		   
			card = self.__hand.pop(0)

			self.__deck.add_card(card)

	##
	# Fonction qui defausse une carte de la main via un index
	# @param	index_card	L'index de la carte à defausser de la main
	##
	def discard_hand_card(self,index_card):
		self.__hand.pop(index_card)