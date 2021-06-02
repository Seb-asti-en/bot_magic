from board import Board
from effect import Effect
from landcard import LandCard


class Player:

	############################ Constructeur ############################
	def __init__(self, player_id, life, deck):
		self.__id = player_id
		self.__life = life
		self.__board = Board(deck)

		self.__mana_pool = {
			"X" : 0,
			"C" : 0,
			"W" : 0,
			"R" : 0,
			"G" : 0,
			"U" : 0,
			"B" : 0
		}
	
	############################ Getters ############################

	def get_id(self):

		return self.__id

	def get_life(self):

		return self.__life

	def get_board(self):

		return self.__board

	def get_mana_pool(self):

		return self.__mana_pool

	############################ Setter ############################

	def set_id(self,nb_id):

		self.__id = nb_id
	
	def set_life(self,nb_life):

		self.__life = nb_life

	def set_mana_pool(self, mana):

		self.__mana_pool = mana
	
	############################ Methodes ############################

	##
	# permet de piocher un nombre n de carte
	# @param nb_card  le nombre de card a piocher
	##
	def draw_card(self,nb_card=1):

		#print("Eugneugneu vous piocheZ",nb_card,"carte(s) TAILLE")
		if len(self.__board.get_deck().get_cards()) > 0:
			for i in range(nb_card):
				self.__board.add_hand(self.__board.get_deck().get_cards().pop(0))	
		else:
			print("ça marche pas")

	def deck_size(self):

		return len(self.__board.get_deck().get_cards())

	def hand_size(self):

		return len(self.__board.get_hand())

	def battlezone_size(self):

		return len(self.__board.get_battle_zone())

	def landzone_size(self):

		return len(self.__board.get_land_zone())

	def graveyard_size(self):

		return len(self.__board.get_graveyard())

	def exile_size(self):

		return len(self.__board.get_exile())

	def tap_land(self, landzone_position, color):

		is_accepted = False

		# Vérification de la position de la carte
		if(landzone_position >= 0 and landzone_position < self.landzone_size()):

			# Engagement du terrain
			is_accepted = self.get_board().get_land_zone()[landzone_position].tap(color)

			if(is_accepted):

				# Mise à jour du pool de mana
				self.__mana_pool["X"] += 1
				self.__mana_pool[color] += 1 

		return is_accepted

	def engage(self, hand_position, land_played, logfile):

		is_accepted = False
		mana_cost = None
		global_cost = 0

		# Vérification de la position de la carte
		if(hand_position >= 0 and hand_position < self.hand_size()):

			# Récupération du coût de la carte
			mana_cost = self.get_board().get_hand()[hand_position].get_mana_cost()

			# Vérification si la carte est un terrain
			if(type(self.get_board().get_hand()[hand_position]) is LandCard):
				
				# Vérification de la possibilité d'engager un terrain
				if(not land_played):

					is_accepted = True
					land_played = True

			else:

				# Calcul du mana global
				for color in mana_cost:
					
					global_cost += mana_cost[color]

				# Vérification de la quantité de mana global
				if(global_cost <= self.__mana_pool["X"]):

					is_accepted = True

					for color in mana_cost:

							# Vérification de la quantité de mana couleur par couleur et que la clé de couleur existe
							if(color not in self.__mana_pool or mana_cost[color] > self.__mana_pool[color]):

								is_accepted = False

			# On continue si le mana nécessaire peut être consommé
			if(is_accepted):

				# Récupération de la carte
				card = self.get_board().get_hand()[hand_position]

				if(card.get_type() == "Land"):

					logfile.write(f"Joueur {self.get_id()+1} tente de poser le terrain {card.get_name()}")	
						
				elif(card.get_type() == "Creature"):

					logfile.write(f"Joueur {self.get_id()+1} tente de poser {card.get_name()} sur le champ de bataille")		

				elif(card.get_type() == "Artifact"):

					logfile.write(f"Joueur {self.get_id()+1} tente d'utiliser {card.get_name()} (Artefact)")	
				
				elif(card.get_type() == "Enchantment"):

					logfile.write(f"Joueur {self.get_id()+1} tente d'utiliser {card.get_name()} (Enchantement)")

				elif(card.get_type() == "Instant"):

					logfile.write(f"Joueur {self.get_id()+1} tente d'utiliser {card.get_name()} (Éphémère)")		

				elif(card.get_type() == "Sorcery"):

					logfile.write(f"Joueur {self.get_id()+1} tente d'utiliser {card.get_name()} (Rituel)")	

				else:

					is_accepted = False	

					logfile.write(f"Joueur {self.get_id()+1} tente d'utiliser une carte invalide")

		return [is_accepted, land_played]

	def move(self, source_zone, source_position, destination_zone):

		source = None

		# Parsing de la zone source
		if(source_zone == "DECK"):

			source = self.__board.get_deck().get_cards()

		elif(source_zone == "HAND"):

			source = self.__board.get_hand()

		elif(source_zone == "BATTLE_ZONE"):

			source = self.__board.get_battle_zone()

		elif(source_zone == "LAND_ZONE"):

			source = self.__board.get_land_zone()

		elif(source_zone == "GRAVEYARD"):

			source = self.__board.get_graveyard()

		elif(source_zone == "EXILE"):

			source = self.__board.get_exile()

		else:

			return False

		# Parsing de la zone de destination
		if(destination_zone == "DECK"):

			destination = self.__board.get_deck().get_cards()

		elif(destination_zone == "HAND"):

			destination = self.__board.get_hand()

		elif(destination_zone == "BATTLE_ZONE"):

			destination = self.__board.get_battle_zone()

		elif(destination_zone == "LAND_ZONE"):

			destination = self.__board.get_land_zone()

		elif(destination_zone == "GRAVEYARD"):

			destination = self.__board.get_graveyard()

		elif(destination_zone == "EXILE"):

			destination = self.__board.get_exile()

		else:

			return False

		# Déplacement de la carte
		destination.append(source.pop(source_position))
			
		return True

	def disengage(self):

		# Dégagement des cartes terrain
		for card in self.__board.get_land_zone():

			card.untap()

		# Dégagement des cartes créature
		for card in self.__board.get_battle_zone():

			card.untap()

			# Retrait du mal d'invocation
			if(card.is_sick()):

				card.cure()

		# Remise à zéro du pool de mana
		for color in self.__mana_pool:

			self.__mana_pool[color] = 0

	def attack(self, target, battlezone_position, player_count):

		is_accepted = False
		card = None

		# Vérification de l'index du joueur
		if(target >= 0 and target < player_count):

			# Vérification que l'on ne s'attaque pas soi-même
			if(target != self.get_id()):

				# Vérification de l'index de la carte
				if(battlezone_position >= 0 and battlezone_position < self.battlezone_size()):

					card = self.__board.get_battle_zone()[battlezone_position]

					if(not card.is_sick() and not card.is_tapped()):

						card.tap()
						card.set_target(target)

						is_accepted = True

		return is_accepted

	def block(self, target, battlezone_position, blocker):

		is_accepted = False
		ennemy_card = None
		card = None

		# Vérificatiton de l'index de la carte attaquante
		if(battlezone_position >= 0 and battlezone_position < target.battlezone_size()):

			ennemy_card = target.get_board().get_battle_zone()[battlezone_position]

			# Vérification que la carte attaquante nous attaque réellement
			if(ennemy_card.is_tapped() and ennemy_card.get_target() == self.__id):

				# Vérification de l'index de la carte bloquante
				if(blocker >= 0 and blocker < self.battlezone_size()):

					card = self.__board.get_battle_zone()[blocker]

					# Vérification que notre carte peut bloquer
					if(not card.is_tapped() and not card.is_blocking()):

						card.set_blocking(battlezone_position)

						is_accepted = True

		return is_accepted

	def cleanup(self):

		# Soin et retrait des bonus arrivés à échéance sur la Battle Zone
		for card in self.__board.get_battle_zone():
			
			card.update()

	def damage(self, power):

		self.__life -= power

	def consume_mana(self, mana_cost, logfile):

		# Retrait du mana par couleur
		for color in mana_cost:

			self.__mana_pool["X"] -= 1
			self.__mana_pool[color] -= 1 

		# Si le mana tampon (X) arrive à 0, on vide le mana pour toutes les couleurs
		if(self.__mana_pool["X"] <= 0):

			for color in self.__mana_pool:

				self.__mana_pool[color] = 0	

			logfile.write(f"Joueur {self.get_id()+1} a consommé tout son mana")				