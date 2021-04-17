#!/usr/bin/env python3

class Deck:
	def __init__(self, cards):
		self.__cards	= cards
	
	def shuffle(self):
		pass
		
	def add_card_deck(self, card):
		self.__cards.append(card)



class Graveyard:
	def __init__(self, cards):
		self.__cards	= cards	
	
	def add_card_graveyard(self, card):
		self.__cards.append(card)



class Hand:
	def __init__(self, cards, max_size=7):
		self.__max_size 	= max_size
		self.__init_cards(cards)
	
	def __init_cards(self, cards):
		self.__cards = [0]
		print(self.__max_size-len(self.__cards))
		for i in range(self.__max_size-len(self.__cards)):
			self.__cards.append(cards[i])
	
	def add_card_hand(self, card):
		self.__cards.append(card)

	def remove_card_hand(self, card_number):
		del self.__cards[card_number]
		
	def show_cards(self):
		print(self.__cards)
		


class Battleground:
	def __init__(self, cards = []):
		self.__cards	= cards

	def add_card_battleground(self, card):
		self.__cards.append(card)
		


# Test #

