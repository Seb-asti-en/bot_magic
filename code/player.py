from abc import ABC
from board import Board



class Player(ABC):

	#Constructeur
	def __init__(self, player_id, life, deck):
		self.__id = player_id
		self.__life = life
		self.__board = Board(deck)

	def get_id(self):
		return self.__id
	
	#Getters
	def get_board(self):
		return self.__board
	
	def get_life(self):
		return self.__life

	#Setter
	def set_life(self,nb_life):
		self.__life = nb_life


	#Methodes
	def draw_card(self,nb_card=1):
		print("Vous piochez",nb_card,"carte(s)")
		for i in range(nb_card):
			self.__board.add_hand(self.__board.get_deck().get_cards().pop(0)) 
	
		
	def play_card(self,index_card):
		self.__board.add_battle_zone(self.__board.get_hand().pop(index_card))
	
	def use_card():
		pass


	def to_graveyard(self,source_list,index_card):
		if source_list == "HAND":
			self.__board.add_graveyard(self.__board.get_hand().pop(index_card))
		elif source_list == "BATTLE_ZONE":
			self.__board.add_graveyard(self.__board.get_battle_zone().pop(index_card))

	def choice_block(self,Player_target,index_target,index_src):
		self.__board.get_battle_zone()[index_src].set_isblocked(True)
		if Player_target.get_board().get_battle_zone()[index_target].get_isattack() == True:
			 Player_target.get_board().get_battle_zone()[index_target].set_istarget(True)
		
	def choice_attack(self,index):
		self.__board.get_battle_zone()[index].set_isattack(True)

	def attack(self,index_source,Player_target):
		deal_damage_to_player(index_source,Player_target)

	def defense(self,Player_target,index_target,index_source):
		self.deal_damage_to_card(index_target, index_source, Player_target)


	def deal_damage_to_player(self,index_source,Player):
		source_dps = self.__board.get_battle_zone()[index_source]
		ennemi_life = Player.get_life()

		Player.set_life(ennemi_life - source_dps)

	def deal_damage_to_card(self,index_target,index_source,Player):
		source_dps = self.__board.get_battle_zone()[index_source]
		ennemi_life = Player.get_board()[index_target].get_life()

		Player.get_board()[index_target].set_toughness(ennemi_life - source_dps)
	

	
	
	def concede():
		pass

	def debug_print_hand(self):
		print("Hand (" + str(len(self.__board.get_hand())) + "):")
		
		for card in self.__board.get_hand():
			print("[" + card._name, end="] ")

		print()
		
		if len(self.__board.get_hand()) == 0:
			print("La main est vide")

	def debug_print_battle_zone(self):
		for card in self.__board.get_battle_zone():
			print("|",card._name,"|",end=' ')
		print("")
		if len(self.__board.get_battle_zone()) == 0:
			print("vide")

	


class HumanPlayer(Player):

	def __init__(self, life, deck):
		super().__init__(life, deck)

class BotPlayer(Player):

	def __init__(self, life, deck):
		super().__init__(life, deck)
