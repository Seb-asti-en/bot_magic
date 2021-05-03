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

class CreatureCard(Card):

	def __init__(self, card, effect):
		super().__init__(card, effect)
		self.__power = card[POWER]
		self.__toughness = card[TOUGHNESS]
		self.__damage = card[POWER]
		self.__life = card[TOUGHNESS]
		self.__buff_life = self.__life
		self.__tristan_damage = card[POWER]

	#Getter
	def get_power(self):
		return self.__power

	def get_toughness(self):
		return self.__toughness

	def get_damage(self):
		return self.__damage 
		
	def get_life(self):
		return self.__life
	
	def get_damage(self):
		return self.__damage

	#Setter
	def set_damage(self,nb_damage):
		self.__damage = nb_damage

	def set_life(self,nb_life):
		self.__life = nb_life


	def buf_damage(self, quantity):
		self.__damage = self.__damage + quantity

	def reduce_damage(self, quantity):
		self.__damage = self.__damage - quantity
		
	def buf_life(self, quantity):
		self.__life = self.__life + quantity
		
	def reduce_life(self, quantity):
		self.__life = self.__life - quantity
	
	def to_string(self):
		string = super().to_string()
		string += "POWER : " + str(self.__power) + " \n" 
		string += "TOUGHNESS : " + str(self.__toughness) + "\n"
		string += "DAMAGE DEAL : " + str(self.__damage) + " \n" 
		string += "LIFE : " + str(self.__life) + "\n"
		return string