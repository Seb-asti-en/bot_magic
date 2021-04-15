#!/usr/bin/env python3

class Card:

	def __init__(self, card_id, collection, name, supertype, subtype, colors, mana_cost, identity, text, quote, effects):

		self._id			= card_id
		self._collection 	= collection
		self._name			= name
		self._supertype		= supertype
		self._subtype		= subtype
		self._colors		= colors
		self._mana_cost		= mana_cost
		self._identity		= identity
		self._text			= text
		self._quote			= quote
		self._effects		= effects

	def to_string(self):

		string = ""

		string += self._id + " " + self._collection + "\n"
		string += self._name + "\n"
		string += self._supertype + " " + self._subtype + "\n"
		
		if (self._colors[0] == 1):
			string += "Incolore"
		else :
			if (self._colors[1] == 1):
				string += "Blanc "
			
			if (self._colors[2] == 1):
				string += "Rouge "
			
			if (self._colors[3] == 1):
				string += "Vert "
			
			if (self._colors[4] == 1):
				string += "Bleu "
			
			if (self._colors[5] == 1):
				string += "Noir"

		string += "\n"

		if (self._mana_cost[0] > 0):
			string += self._mana_cost[0] + "(Incolore) "

		if (self._mana_cost[1] > 0):
			string += self._mana_cost[1] + "(Blanc) "

		if (self._mana_cost[2] > 0):
			string += self._mana_cost[2] + "(Rouge) "

		if (self._mana_cost[3] > 0):
			string += self._mana_cost[3] + "(Vert) "

		if (self._mana_cost[4] > 0):
			string += self._mana_cost[4] + "(Bleu) "

		if (self._mana_cost[5] > 0):
			string += self._mana_cost[5] + "(Noir)"
		
		string += "\n"
		
		if (self._identity[0] == 1):
			string += "Incolore"
		else :
			if (self._identity[1] == 1):
				string += "Blanc "
			
			if (self._identity[2] == 1):
				string += "Rouge "
			
			if (self._identity[3] == 1):
				string += "Vert "
			
			if (self._identity[4] == 1):
				string += "Bleu "
			
			if (self._identity[5] == 1):
				string += "Noir"

		string += self._text + "\n"
		string += self._quote + "\n"




class CreatureCard(Card):

	def __init__(self, power, toughness, **kwargs):

		super().__init__(**kwargs)
		self.__power = power
		self.__toughness = toughness

class SorceryCard(Card):

	def __init__(self, **kwargs):

		super().__init__(**kwargs)

	def print(self):

		super().print()
		print(self.__power + "/" + self.__toughness)
		

class LandCard(Card):

	def __init__(self, **kwargs):

		super().__init__(**kwargs)

class InstantCard(Card):

	def __init__(self, **kwargs):

		super().__init__(**kwargs)


card = Card()