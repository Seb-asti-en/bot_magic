#!/usr/bin/env python3

class Player:
	def __init__(self, life, deck, graveyard, hand, battleground):
		self.__life			= life
		self.__deck			= deck
		self.__graveyard	= graveyard
		self.__hand			= hand
		self.__battleground	= battleground


class HumanPlayer(Player):
	pass


class BotPlayer(Player):
	pass