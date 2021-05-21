from card import Card

class LandCard(Card):

	def __init__(self, card):
		super().__init__(card)

		self.__tapped = False
	
	def to_string(self):
		string = super().to_string()
		return string

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

	def untap(self):

		if(self.__tapped):
			
			self.__tapped = False

	def is_tapped(self):

		return self.__tapped