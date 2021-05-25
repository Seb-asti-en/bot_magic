############################ Import ############################
from card import Card

IDLE = -1

POWER = 0
TOUGHNESS = 1
NB_TURNS = 2

class CreatureCard(Card):

	############################ Constructeur ############################
	def __init__(self, card):
		super().__init__(card)
		self.__power = card["Power"]			# Force
		self.__toughness = card["Toughness"]	# Endurance

		self.__damage = card["Power"]
		self.__life = card["Toughness"]
		self.__tmp_life = card["Toughness"]
		self.__tmp_damage = card["Power"]

		self.__bonus = [0,0]					# Bonus persistant
		self.__timed_bonuses = []				# Liste des bonus temporaires
		self.__tapped = False					# Etat d'engagement
		self.__summoning_sickness = True		# Mal d'invocation
		self.__target = IDLE					# Joueur ciblé
		self.__blocking = IDLE					# Carte attaquante à bloquer
		
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

	def get_target(self):

		return self.__target

	def get_blocking(self):

		return self.__blocking

	############################ Setters ############################
	def set_damage(self,nb_damage):
		self.__damage = nb_damage

	def set_life(self,nb_life):
		self.__life = nb_life

	def set_target(self, target):
		
		self.__target = target

	def set_blocking(self, blocking):

		self.__blocking = blocking

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

	# ##
	# # Reset la carte aux stats par defaut
	# ##
	# def reset(self):
	# 	self.__damage = self.__power
	# 	self.__life = self.__toughness
	# 	self.__tmp_life =self.__toughness
	# 	self.__tmp_damage = self.__power

	def tap(self):

		if(not self.__tapped):

			self.__tapped = True

	def untap(self):

		if(self.__tapped):
			
			self.__tapped = False
			self.__target = IDLE
			self.__blocking = IDLE

	def cure(self):

		self.__summoning_sickness = False

	def is_sick(self):

		return self.__summoning_sickness

	def is_tapped(self):

		return self.__tapped

	def power(self):

		power = 0

		power = self.__power + self.__bonus[POWER]

		for timed_bonus in self.__timed_bonuses:

			power += timed_bonus[POWER]

		return power

	def toughness(self):

		toughness = 0

		toughness = self.__toughness + self.__bonus[TOUGHNESS]

		for timed_bonus in self.__timed_bonuses:

			toughness += timed_bonus[TOUGHNESS]

		return toughness

	def update(self):

		i = 0

		for timed_bonus in self.__timed_bonuses[:]:

			if(timed_bonus[NB_TURNS] == 1):

				# On supprime le bonus
				self.__timed_bonuses.pop(i)

			else:
	
				# On décrémente le timer du bonus
				self.__timed_bonuses[i][NB_TURNS] -= 1

				i += 1

	def reset(self):

		self.__bonus[POWER] = 0
		self.__bonus[TOUGHNESS] = 0
		self.__timed_bonuses.clear()

	def is_attacking(self):

		return self.__target != IDLE

	def is_blocking(self):

		return self.__blocking != IDLE

	def damage(self, power):

		# Dans le cas où les dommages sont négatifs
		if(power < 0):

			power = 0
				
		self.__timed_bonuses.append([0,-power,1])