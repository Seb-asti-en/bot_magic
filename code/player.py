#!/usr/bin/env python3

from board import Board

class Player:
	def __init__(self, life, deck):
		self._life	= life
		self._board	= Board(deck)
	
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
	pass


class BotPlayer(Player):
	pass
