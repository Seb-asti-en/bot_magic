#!/usr/bin/env python3

class Card:
	def __init__(self, idc = 0, name = "cardname", collection = "", colors = [1,0,0,0,0,0], mcost=[1,0,0,0,0,0], identity=[1,0,0,0,0,0], text = "this is text", quote = "quote", supertype = "supertype", subtype = "subtype"):
		self._id		= idc
		self._name		= name
		self._collection= collection
		self._colors	= colors
		self._mana_cost	= mcost
		self._identity	= identity
		self._text		= text
		self._quote		= quote
		self._supertype	= supertype
		self._subtype	= subtype
		
	def get_name(self):
		return self._name

class Deck:
	def __init__(self, cards):
		self._cards	= cards

class Graveyard:
	def __init__(self, cards):
		self._cards	= cards


class Hand:
	def __init__(self, cards, max_size=7):
		self._cards	   = cards
		self._max_size = max_size


class Battleground:
	def __init__(self, cards):
		self._cards	= cards

class Player:
	def __init__(self, life, deck, graveyard, hand, battleground):
		self._life			= life
		self._deck			= deck
		self._graveyard		= graveyard
		self._hand			= hand
		self._battleground	= battleground
