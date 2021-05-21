############################ Import ############################
from card import Card


class CreatureCard(Card):

	############################ Constructeur ############################
	def __init__(self, card):
		super().__init__(card)
		self.__power = card["Power"]
		self.__toughness = card["Toughness"]
		self.__damage = card["Power"]
		self.__life = card["Toughness"]
		self.__tmp_life = card["Toughness"]
		self.__tmp_damage = card["Power"]

		self.__tapped = False
		self.__summoning_sickness = True

		
	############################ Getters ############################
	def get_power(self):
		return self.__power

	def get_toughness(self):
		return self.__toughness

	def get_damage(self):
		return self.__damage 
		
	def get_life(self):
		return self.__life
	
	def get_tmp_damage(self):
		return self.__tmp_damage	
	
	def get_tmp_life(self):
		return self.__tmp_life


	############################ Setters ############################
	def set_damage(self,nb_damage):
		self.__damage = nb_damage

	def set_life(self,nb_life):
		self.__life = nb_life


	############################ Méthode ############################
	##
	# Augmente les dégats de la carte 
	# @param quantity 	La quantitée de dégats ajouté
	##
	def buf_damage(self, quantity):
		self.__damage = self.__damage + quantity
	
	##
	# Réduit les dégats de la carte 
	# @param quantity 	La quantitée de dégats retiré
	##
	def reduce_damage(self, quantity):
		self.__damage = self.__damage - quantity
		
	##
	# Augmente les point de vie de la carte 
	# @param quantity 	La quantitée de point de vie ajouté
	##
	def buf_life(self, quantity):
		self.__life = self.__life + quantity
		
	##
	# Réduit les point de vie de la carte 
	# @param quantity 	La quantitée de point de vie retiré
	##
	def reduce_life(self, quantity):
		self.__life = self.__life - quantity
	
	##
	# Extension de la fonction to string de la classe card 
	##
	def to_string(self):
		string = super().to_string()
		string += "POWER : " + str(self.__power) + " \n" 
		string += "TOUGHNESS : " + str(self.__toughness) + "\n"
		string += "DAMAGE DEAL : " + str(self.__damage) + " \n" 
		string += "LIFE : " + str(self.__life) + "\n"
		return string

	##
	# Reset la carte aux stats par defaut
	##
	def reset(self):
		self.__damage = self.__power
		self.__life = self.__toughness
		self.__tmp_life =self.__toughness
		self.__tmp_damage = self.__power

	def untap(self):

		if(self.__tapped):
			
			self.__tapped = False

	def cure(self):

		self.__summoning_sickness = False

	def is_sick(self):

		return self.__summoning_sickness

	def is_tapped(self):

		return self.__tapped