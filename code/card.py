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


