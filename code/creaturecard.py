from card import Card

class CreatureCard(Card):

	def __init__(self, card):
		super().__init__(card)
		self.__power = card["Power"]
		self.__toughness = card["Toughness"]
		self.__damage = card["Power"]
		self.__life = card["Toughness"]
		self.__buff_life = card["Toughness"]
		self.__buff_damage = card["Power"]

		

	#Getter
	def get_power(self):
		return self.__power

	def get_toughness(self):
		return self.__toughness

	def get_damage(self):
		return self.__damage 
		
	def get_life(self):
		return self.__life
	
	def get_buff_damage(self):
		return self.__buff_damage	
	
	def get_buff_life(self):
		return self.__buff_life

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