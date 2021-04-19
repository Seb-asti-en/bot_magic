#!/usr/bin/env python3

class Player:
	def __init__(self, life, deck, graveyard, hand, battleground):
		self._life			 = life
		self._deck			 = deck
		self._graveyard	     = graveyard
		self._hand			 = hand
		self._battleground	 = battleground
	
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
