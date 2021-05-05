from board import Board
from effect import Effect 

class Player():

	#Constructeur
	def __init__(self, player_id, life, deck):
		self.__id = player_id
		self.__life = life
		self.__board = Board(deck)

	
	#Getters
	def get_board(self):
		return self.__board
	
	def get_life(self):
		return self.__life

	def get_id(self):
		return self.__id
	
	#Setter
	def set_life(self,nb_life):
		self.__life = nb_life

	#Methodes


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
		print("taille",len(self.__board.get_hand()),index_card)
		if index_card < 0 or index_card >=  len(self.__board.get_hand()) :
			print("index trop grand ou trop petit")
		else:

			if self.__board.get_hand()[index_card].get_type() =="Land":
				print("itsss lannnd",self.__board.get_hand()[index_card]._name)
				self.__board.add_land_zone(self.__board.get_hand().pop(index_card))

			elif self.__board.get_hand()[index_card].get_type() =="Creature" or self.__board.get_hand()[index_card].get_type() =="Artifact" :
	
				print("itsss creature",self.__board.get_hand()[index_card]._name)
				self.__board.add_battle_zone(self.__board.get_hand().pop(index_card)) 

			elif self.__board.get_hand()[index_card].get_type() =="Instant" :
				print("itsss INSTANT")
				print(self.__board.get_hand()[index_card].to_string())
				
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
	def choice_block(self,Player_target,index_target,index_src):
		if self.__board.isempty_battle_zone() or index_src >= len(self.__board.get_battle_zone()) or index_src < 0:
				print("l'index source est trop grand ou trop petit", index_src)
		else:
			self.__board.get_battle_zone()[index_src].set_isblocked(True)
			if Player_target.get_board().get_battle_zone()[index_target].get_isattack() == True:
				Player_target.get_board().get_battle_zone()[index_target].set_istarget(True)
			else:
				print("selectioner un attaquant")

	###
	#permet de choisir la carte qui attaque
	# @param index l'index de la carte
	###
	def choice_attack(self,index):
		print("index",index,len(self.__board.get_battle_zone()))
		if self.__board.isempty_battle_zone() or index >= len(self.__board.get_battle_zone()) or index < 0 :
			print("l'index est trop grand ou trop petit", index)
		else:
			self.__board.get_battle_zone()[index].set_isattack(True)

	##
	# donne des degats aux joueurs  adverse
	# @param Player_target le joueur adverse
	# @param index_source l'index de la carte qui attaque
	##
	def attack(self,Player_target,index_source):

		deal_damage_to_player(index_source,Player_target)

	##
	# donne des degats aux carte  adverse
	# @param Player_target le joueur adverse
	# @parem index_target l'index de la carte adverse
	# @param index_source l'index de la carte qui attaque
	##
	def defense(self,Player_target,index_target,index_source):
		self.deal_damage_to_card( Player_target,index_target, index_source)

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

		card_attk = self.__board.get_battle_zone()[index_source]
		card_deff = Player_target.get_board().get_battle_zone()[index_target]

		source_dps = card_deff.get_damage()
		source_life = card_deff.get_life()

		ennemi_dps = card_attk.get_damage()
		ennemi_life = card_attk.get_life()

		print("EFECT ATTACK",card_attk.get_effect().get_list_effects())
		print("EFECT DEFF",card_deff.get_effect().get_list_effects())


		if "first" or "double" in card_attk.get_effect().get_list_effects() :
			card_deff.set_life(source_life - ennemi_dps)

			if  card_deff.get_life() >= 0:
				card_attk.set_life(ennemi_life - source_dps)

				if "double" in card_attk.get_effect().get_list_effects() :
					card_deff.set_life(card_deff.get_life() - ennemi_dps)
		else:
				card_deff.set_life(ennemi_life - source_dps)
				card_attk.set_life(source_life - ennemi_dps)


		for effect in card_attk.get_effect().get_list_effects():
			card_attk.get_effect().end_battle_phase(effect, Player_target, self, card_deff)

		# if "lifelink" in card_deff.get_effect().get_list_effects():
		#  	card_deff.get_effect().lifelink(self,card_deff)
		# if "lifelink" in card_attk.get_effect().get_list_effects():
		#  	card_attk.get_effect().lifelink(Player_target,card_attk)
		
		# if "trample" in card_deff.get_effect().get_list_effects():
		#  	card_deff.get_effect().trample(card_attk,ennemi_life)
	
		# if "deathtouch" in card_deff.get_effect().get_list_effects():
		#  	card_deff.get_effect().deathtouch(card_attk)
		# if "deathtouch" in card_attk.get_effect().get_list_effects():
		#  	card_attk.get_effect().deathtouch(card_deff)
		

	def concede():
		pass

	def debug_print_hand(self):
		print("Hand (" + str(len(self.__board.get_hand())) + "):")
		
		for card in self.__board.get_hand():
			print("[" + card._name, end="] ")

		print("\n")
		
		if len(self.__board.get_hand()) == 0:
			print("La main est vide")

	def debug_print_battle_zone(self):
		for card in self.__board.get_battle_zone():
			print("|",card._name,"|",end=' ')
		print("")
		if len(self.__board.get_battle_zone()) == 0:
			print("vide")
