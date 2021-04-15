#!/usr/bin/env python3

class Player:
	def __init__(self, life, deck, graveyard, hand, battleground):
		self._life			 = life
		self._deck			 = deck
		self._graveyard	     = graveyard
		self._hand			 = hand
		self._battleground	 = battleground


class HumanPlayer(Player):
	pass


class BotPlayer(Player):
	pass
