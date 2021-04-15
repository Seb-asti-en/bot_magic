#!/usr/bin/env python3

class Deck:
	def __init__(self, cards):
		self.__cards	= cards
	
	def shuffle(self):
		pass
		
	def draw(self):
		return 0


class Graveyard:
	def __init__(self, cards):
		self.__cards	= cards


class Hand:
	def __init__(self, cards, max_size=7):
		self.__cards	   = cards
		self.__max_size = max_size


class Battleground:
	def __init__(self, cards):
		self.__cards	= cards