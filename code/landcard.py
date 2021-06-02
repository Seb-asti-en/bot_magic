from card import Card

class LandCard(Card):

	############################ Constructeur ############################

	def __init__(self, card):
		super().__init__(card)

		self.__tapped = False

	############################ Méthode ############################
	
	##
	# Fonction qui tap une carte terrain suivant sa couleur pour la rendre utilisé
	# @param	color	La couleur du mana qu'on veut utiliser
	##
	def tap(self, color):

		is_accepted = False

		# Vérification si le terrain a déjà été engagé
		if(not self.__tapped):

			# Vérification si la couleur choisie est la bonne
			if(color in self.get_identity()):

				# Engagement du terrain
				self.__tapped = True
				is_accepted = True

		return is_accepted

	
	##
	# Fonction qui untap une carte terrain pour la rendre de nouveau utilisable
	##
	def untap(self):

		if(self.__tapped):
			
			self.__tapped = False

	##
	# Fonction qui retourne l'état du terrain
	# Si c'est True alors le terrain est utilisé
	# Si c'est False alors le terrain est utilisable
	##
	def is_tapped(self):

		return self.__tapped