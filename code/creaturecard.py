############################ Import ############################
from card import Card
from evergreen import Evergreen

IDLE = -1

POWER = 0
TOUGHNESS = 1
NB_TURNS = 2

class CreatureCard(Card):

	############################ Constructeur ############################
	def __init__(self, card):
		super().__init__(card)
		self.__power = card["Power"]						# Force
		self.__toughness = card["Toughness"]				# Endurance
		self.__evergreen = Evergreen(card["Evergreen"])		# Evergreen
		self.__enchantment = []								# Enchantement
		self.__bonus = [0,0]								# Bonus persistant
		self.__timed_bonuses = []							# Liste des bonus temporaires
		self.__tapped = False								# Etat d'engagement
		self.__summoning_sickness = True					# Mal d'invocation
		self.__target = IDLE								# Joueur ciblé
		self.__blocking = IDLE								# Carte attaquante à bloquer
		
	############################ Getters ############################
	
	def get_power(self):
		return self.__power

	def get_toughness(self):
		return self.__toughness

	def get_target(self):
		return self.__target

	def get_blocking(self):
		return self.__blocking

	############################ Setters ############################

	def set_target(self, target):
		self.__target = target

	def set_blocking(self, blocking):
		self.__blocking = blocking

	def remove_summoning_sickness(self):
		self.__summoning_sickness = False

	############################ Méthode ############################	

	##
	# Fonction pour tap une creature, c'est à dire la rendre inutilisable pour le reste du tour
	##
	def tap(self):

		if(not self.__tapped):

			self.__tapped = True

	##
	# Fonction pour untap une creature, c'est à dire la rendre de nouveau utilisable
	##
	def untap(self):

		if(self.__tapped):
			
			self.__tapped = False
			self.__target = IDLE
			self.__blocking = IDLE

	##
	# Fonction pour retiré le mal d'invocation une creature
	##
	def cure(self):

		self.__summoning_sickness = False

	##
	# Fonction pour savoir si la creature possède actuellement un mal d'invocation
	# @return 	True si la creature à le mal d'invocation, sinon False
	##
	def is_sick(self):

		return self.__summoning_sickness

	##
	# Fonction pour savoir si la creature est actuellement tap 
	# @return 	True si la creature est tap, sinon False
	##
	def is_tapped(self):

		return self.__tapped

	##
	# Fonction pour savoir la force d'une carte en comptant les bonus permanent et temporaire
	# @return 	power	La force de la carte 
	##
	def power(self):

		power = 0

		power = self.__power + self.__bonus[POWER]

		for timed_bonus in self.__timed_bonuses:

			power += timed_bonus[POWER]

		return power

	##
	# Fonction pour savoir l'endurance d'une carte en comptant les bonus permanent et temporaire
	# @return 	toughness	L'endurance de la carte 
	##
	def toughness(self):

		toughness = 0

		toughness = self.__toughness + self.__bonus[TOUGHNESS]

		for timed_bonus in self.__timed_bonuses:

			toughness += timed_bonus[TOUGHNESS]

		return toughness

	##
	# Fonction qui met a jour les bonus temporaire, à la fin du tour leur enlève 1 au compteur de tour restant pour le bonus
	##
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

	##
	# Fonction qui retire tout les bonus sur la carte et lui redonne sa puissance et son endurance originel
	##
	def reset(self):

		self.__bonus[POWER] = 0
		self.__bonus[TOUGHNESS] = 0
		self.__timed_bonuses.clear()


	##
	# Fonction qui sert a savoir si la creature attaque
	# @return	True si la creature est en posture d'attaque, sinon False
	##
	def is_attacking(self):

		return self.__target != IDLE

	##
	# Fonction qui sert a savoir si la creature bloque l'attaque d'une autre creature
	# @return	True si la creature est en posture de defense, sinon False
	##
	def is_blocking(self):

		return self.__blocking != IDLE

	##
	# Fonction qui sert a savoir si la creature attaque
	# @return	True si la creature est en posture d'attaque, sinon False
	##
	def damage(self, power):

		# Dans le cas où les dommages sont négatifs
		if(power < 0):

			power = 0
				
		self.__timed_bonuses.append([0,-power,1])

		
	##
	# Fonction qui sert à modifier les valeurs de puissance et d'enrance bonus
	# @param	power		La puissance à ajouter en bonus
	# @param	Toughness	L'endurance à ajouter en bonus
	##
	def add_bonus(self,power,toughness):
		self.__bonus[POWER] += power
		self.__bonus[TOUGHNESS] += toughness

	##
	# Initialise les evergreen grace au JSON
	# @param	card	La carte JSON pris en refference
	##
	def init_evergreen(self, evergreen):
		self._evergreen = Evergreen(evergreen)
		return self._evergreen

	##
	# Ajoute des bonus de puissance et d'endurance
	# @param	power		La puissance bonus
	# @param 	toughness	L'endurance bonus
	# @param 	nbTour 		Le nombre de tour d'activation du bonus
	##
	def append_timed_bonuses(self,power,toughness,nbTour):
		self.__timed_bonuses.append([power,toughness,nbTour])