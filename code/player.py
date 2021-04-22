#!/usr/bin/env python3

from abc import ABC
from board import Board

class Player(ABC):

	#Constructeur
	def __init__(self, life, deck):
		self.__life = life
		self.__board = Board(deck)
	
	#Methodes
	def draw_card():
		pass
	
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

class HumanPlayer(Player):

	def __init__(self, life, deck):
		super().__init__(life, deck)

class BotPlayer(Player):

	def __init__(self, life, deck):
		super().__init__(life, deck)
