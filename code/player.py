from board import Board
from effect import Effect 

class Player():

	############################ Constructeur ############################
	def __init__(self, player_id, life, deck):
		self.__id = player_id
		self.__life = life
		self.__board = Board(deck)
		self.__available_mana = {}

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
	def get_board(self):

		return self.__board
	
	def get_life(self):

		return self.__life

	def get_id(self):

		return self.__id
	
	def get_available_mana(self):

		return self.__available_mana



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

	### TODO: Soustrait mana quand carte jouer
	
	##
	# Ajoute un mana dans la reserve de mana
	# @param key la couleur voulu
	# @param Card la carte regardé
	##
	def add_mana(self, Card):

		for key in Card.get_identity():
			if key in self.__available_mana:
				self.__available_mana[key] = self.__available_mana[key] + 1
			else:
				self.__available_mana[key] = 1

	##
	# Le nombre de mana disponible  
	# @return nb mana
	##
	def remaining_mana(self):
		res = 0
		for key in self.__available_mana:
			res += self.__available_mana[key]
		return res
	##
	# (pour l'instant) Enlève le mal d'invocation
	##
	def untap(self):

		for card in self.__board.get_battle_zone():
			card.set_issummoning_sickness(False)

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
		
	##
	# permet de jouer une cart et la place selon sont type
	# @param index_card index de la carte
	##
	def play_card(self,index_card):
		b = False
		print("taille",len(self.__board.get_hand()),index_card)
		if index_card < 0 or index_card >=  len(self.__board.get_hand()) :
			print("index trop grand ou trop petit")
			
		elif self.playable_card(index_card) == False:
			print("Le mana necessaire pour certe carte est insuffisant")
		
		else:
			if self.__board.get_hand()[index_card].get_type() =="Land":
				print("itsss lannnd",self.__board.get_hand()[index_card]._name)
				land_card = self.__board.get_hand().pop(index_card)
				self.__board.add_land_zone(land_card)
				self.add_mana(land_card)
				b = True	
				

			elif self.__board.get_hand()[index_card].get_type() == "Creature" or self.__board.get_hand()[index_card].get_type() == "Artifact" :
				print("itsss creature",self.__board.get_hand()[index_card]._name)
				self.__board.add_battle_zone(self.__board.get_hand().pop(index_card)) 
				b = True

			elif self.__board.get_hand()[index_card].get_type() =="Instant" :
				print("itsss INSTANT")
				print(self.__board.get_hand()[index_card].to_string())
				b = True
		
		return b

	##
	# permet de savoir si une carte est jouable 
	# @param index_card index de la carte vérifié
	# retourne true si elle est jouable, sinon false
	##
	def playable_card(self, index_card):

		b = True
		print(self.__board.get_hand()[index_card].get_mana_cost())
		print(self.__board.get_hand()[index_card].get_identity())
		if self.__board.get_hand()[index_card].get_mana_cost() != {}:
			tmpX = 0
			tmp = self.remaining_mana()
			if tmp != 0:
				for key in self.__board.get_hand()[index_card].get_mana_cost():
					if key == 'X':
						tmpX = self.__board.get_hand()[index_card].get_mana_cost()['X']
					elif key in self.__available_mana:
						if self.__available_mana[key] >= self.__board.get_hand()[index_card].get_mana_cost()[key]:
							tmp -= self.__board.get_hand()[index_card].get_mana_cost()[key]
						else:
							b = False
					else:
						b = False
				if tmpX != 0 and b != False:
					if tmp >= tmpX:
						b = True
					else:
						b = False
		return b

	##
	# permet d'utiliser des cartes
	##	
	def use_card(self,index_source):

		pass

	##
	# permet de netoyer une carte de ses effets
	# @param Card la carte a clear
	##
	def clear_card(self,Card):

		Card.reset()
		
	##
	# permet de mettre une carte dans le cimetiere de nimporte qu'elle liste
	# @param source_list la liste  ou se trouve la carte a defausser 
	# @param index_card l'index de la carte a defausser
	##
	def to_graveyard(self,source_list,index_card):

		if source_list == "HAND":
			if len(self.__board.get_hand()) != 0 :
				self.clear_card(self.__board.get_hand()[index_card])
				self.__board.add_graveyard(self.__board.get_hand().pop(index_card))
		elif source_list == "BATTLE_ZONE":
			if len(self.__board.get_battle_zone()) != 0 :
				self.clear_card(self.__board.get_battle_zone()[index_card])
				self.__board.add_graveyard(self.__board.get_battle_zone().pop(index_card))
	
	##
	# permet de choisir les cartes bloquante
	# @param Player_target le joueur adverse
	# @param index_target  l'index de la carte adverse a bloquer
	# @param index_src	l'index de la carte qui doit bloquer
	##
	def choice_block(self,Player_target,attacker,blocker):

		b = False
		if self.__board.isempty_battle_zone():
			print("Vous n'avez pas de cartes pour vous defendre")
		elif blocker >= len(self.__board.get_battle_zone()) or blocker < 0:
				print("l'index source est trop grand ou trop petit", blocker)
		elif Effect.early_choice_block(Player_target.get_board().get_battle_zone()[attacker], self.__board.get_battle_zone()[blocker]) == True :
			b = True
			self.__board.get_battle_zone()[blocker].set_isblocked(True)
			if Player_target.get_board().get_battle_zone()[attacker].get_isattack() == True:
				Player_target.get_board().get_battle_zone()[attacker].set_istarget(True)
			else:
				print("selectioner un attaquant")
		else:
			print("vous ne pouvez pas bloquer")
		return b

	###
	# permet de choisir la carte qui attaque
	# @param index l'index de la carte
	###
	def choice_attack(self,index):
		b = False
		if self.__board.isempty_battle_zone() or index >= len(self.__board.get_battle_zone()) or index < 0 :
			print("l'index est trop grand ou trop petit", index)
			
		elif Effect.early_choice_attack(self.__board.get_battle_zone()[index]) == False :
			print("la carte ne peut pas attaquer")
			
		elif self.get_board().get_battle_zone()[index].get_issummoning_sickness() == True:
			print("la carte ne peut pas attaquer elle a le mal d'invocation")
			
		else:
			self.__board.get_battle_zone()[index].set_isattack(True)
			b = True
		return b

	##
	# donne des degats aux joueurs  adverse
	# @param Player_target le joueur adverse
	# @param index_source l'index de la carte qui attaque
	##
	def direct_attack(self,Player_target,index_source):

		self.deal_damage_to_player(index_source,Player_target)

	##
	# donne des degats aux carte  adverse
	# @param Player_target le joueur adverse
	# @parem index_target l'index de la carte adverse
	# @param index_source l'index de la carte qui attaque
	##
	# def attack(self,Player_target,index_target,index_source):

	# 	self.deal_damage_to_card( Player_target,index_target, index_source)

	##
	# suprime le deck
	##
	def delete_deck(self):

		for i in range( len(self.get_board().get_deck().get_cards())):
			self.get_board().get_deck().get_cards().pop(0)

	##
	# donne des degats au joueur adverse
	# @param Player_target joueur adverse
	# @param index_source carte qui inflige les dps
	##
	def deal_damage_to_player(self,Player_target,index_source):

		source_dps = self.__board.get_battle_zone()[index_source]
		ennemi_life = Player_target.get_life()

		Player.set_life(ennemi_life - source_dps)

	##
	# donne des degats au carte adverse
	# @param Player_target joueur adverse
	# @param index_target l'index de la carte adverse
	# @param index_source carte qui inflige les dps
	##
	def deal_damage_to_card(self,Player_target,index_target,index_source):

		#defini les cartes(pour que ça soit plus court a ecrire)
		card_attk = self.__board.get_battle_zone()[index_source]
		card_deff = Player_target.get_board().get_battle_zone()[index_target]

		print("EFECT ATTACK",card_attk.get_effect().get_list_effects())
		print("EFECT DEFF",card_deff.get_effect().get_list_effects())

		#regarde si il y a un effet avant l'attaque
		if Effect.early_battle_phase(card_deff,card_attk) == False:
			card_deff.set_life(card_deff.get_life() - card_attk.get_damage())
			card_attk.set_life(card_attk.get_life() - card_deff.get_damage())

		#effets apres l'attaque
		Effect.end_battle_phase(Player_target,card_deff,self,card_attk)
	
	##
	#permet de conceder
	##
	def concede():

		pass

	##
	# affiche  le nom des carte de la main
	##
	def debug_print_hand(self):

		print("Hand (" + str(len(self.__board.get_hand())) + "):")
		
		for card in self.__board.get_hand():
			print("[" + card._name, end="] ")

		print("\n")
		
		if len(self.__board.get_hand()) == 0:
			print("La main est vide")

	##
	# affiche  le nom des carte de la battlezone
	##
	def debug_print_battle_zone(self):

		for card in self.__board.get_battle_zone():
			print("|",card._name,"|",end=' ')
		print("")
		if len(self.__board.get_battle_zone()) == 0:
			print("vide")

	def debug_print_land_zone(self):
		
		print("|",self.get_available_mana(),"|")

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

	def engage(self, hand_position):

		is_accepted = False
		mana_cost = None
		global_cost = 0

		# Vérification de la position de la carte
		if(hand_position >= 0 and hand_position < self.hand_size()):

			mana_cost = self.get_board().get_hand()[hand_position].get_mana_cost()

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

			if(is_accepted):

				# Engager la carte
				if(self.get_board().get_hand()[hand_position].get_type() == "Land"):

					is_accepted = self.move("HAND",hand_position,"LAND_ZONE")

				elif(self.get_board().get_hand()[hand_position].get_type() == "Creature"):

					is_accepted = self.move("HAND",hand_position,"BATTLE_ZONE")

				if(is_accepted):

					# Mise à jour du pool de mana
					for color in mana_cost:

						self.__mana_pool["X"] -= 1
						self.__mana_pool[color] -= 1 

					if(self.__mana_pool["X"] == 0):

						for color in self.__mana_pool:

							self.__mana_pool[color] = 0	

		return is_accepted						

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

	def attack(self,target,battlezone_position,player_count):

		is_accepted = False
		card = None

		if(target >= 0 and target < player_count):

			print("1")

			if(battlezone_position >= 0 and battlezone_position < self.battlezone_size()):

				print("2")

				card = self.__board.get_battle_zone()[battlezone_position]

				if(not card.is_sick() and not card.is_tapped()):

					print("3")

					card.tap()

					card.set_target(target)

					is_accepted = True

		return is_accepted

	# def block(self,Player_target,battlezone_position,blocker):

	# 	is_accepted = False

	# 	if(self.battlezone_size() > 0):





	# 	b = False
	# 	if self.__board.isempty_battle_zone():
	# 		print("Vous n'avez pas de cartes pour vous defendre")
	# 	elif blocker >= len(self.__board.get_battle_zone()) or blocker < 0:
	# 			print("l'index source est trop grand ou trop petit", blocker)
	# 	elif Effect.early_choice_block(Player_target.get_board().get_battle_zone()[attacker], self.__board.get_battle_zone()[blocker]) == True :
	# 		b = True
	# 		self.__board.get_battle_zone()[blocker].set_isblocked(True)
	# 		if Player_target.get_board().get_battle_zone()[attacker].get_isattack() == True:
	# 			Player_target.get_board().get_battle_zone()[attacker].set_istarget(True)
	# 		else:
	# 			print("selectioner un attaquant")
	# 	else:
	# 		print("vous ne pouvez pas bloquer")
	# 	return b