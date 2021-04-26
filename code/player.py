#!/usr/bin/env python3

from abc import ABC
from board import Board



class Player(ABC):

	#Constructeur
	def __init__(self, life, deck):
		self.__life = life
		self.__board = Board(deck)
	

	#Getters
	def get_board(self):
		return self.__board
	
	def get_life(self):
		return self.__life

	#Methodes
	def draw_card(self,nb_card=1):
		for i in range(nb_card):
			self.__board.add_hand(self.__board.get_deck().get_cards().pop(0)) 
	
		
	def play_card():
		pass
	
	def use_card():
		pass
	
	def discard_card():
		pass
	
	def attack():
		pass
	
	def block():
		pass
	
	def concede():
		pass

	def choice_card(self):
		pass
	
	def debug_print_hand(self):
		for card in self.__board.get_hand():
			print(card)
		if len(self.__board.get_hand()) == 0:
			print("vide")

class HumanPlayer(Player):

	def __init__(self, life, deck):
		super().__init__(life, deck)

class BotPlayer(Player):

	def __init__(self, life, deck):
		super().__init__(life, deck)
