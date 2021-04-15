#!/usr/bin/env python3

class Card:
	def __init__(self, idc = 0, name = "cardname", collection = "", colors = [1,0,0,0,0,0], mcost=[1,0,0,0,0,0], identity=[1,0,0,0,0,0], text = "this is text", quote = "quote", supertype = "supertype", subtype = "subtype"):
		self.__id		= idc
		self.__name		= name
		self.__collection= collection
		self.__colors	= colors
		self.__mana_cost= mcost
		self.__identity	= identity
		self.__text		= text
		self.__quote	= quote
		self.__supertype= supertype
		self.__subtype	= subtype
		
	def get_name(self):
		return self.__name

class CreatureCard:
	def __init__(self):
		pass

class SorceryCard:
	def __init__(self):
		pass

class LandCard:
	def __init__(self):
		pass

class InstantCard:
	def __init__(self):
		pass


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

class Player:
	def __init__(self, life, deck, graveyard, hand, battleground):
		self.__life			= life
		self.__deck			= deck
		self.__graveyard	= graveyard
		self.__hand			= hand
		self.__battleground	= battleground


class HumanPlayer:
	def __init__(self):
		pass

class BotPlayer:
	def __init__(self):
		pass



















