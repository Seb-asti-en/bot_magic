############################ Import ############################
import random

class Deck:

	############################ Constructeur ############################
    def __init__(self,name,cards):
        self.__name = name
        self.__cards = cards

    ############################ Getters ############################
    def get_name(self):
        return self.__name
    
    def get_cards(self):
        return self.__cards

    ############################ Setters ############################
    def set_name(self,name):
        self.__name = name

    def set_cards(self,cards):
        self.__cards = cards

    ############################ Méthode ############################
	##
	# Mélange les cartes du deck
	##
    def shuffle(self):
        random.shuffle(self.__cards)

	##
	# Ajoute une carte dans le deck
	##
    def add_card(self,card):
        self.__cards.append(card)

	##
	# Retire une carte du deck
	##
    def remove_card(self,card):
        self.__cards.remove(card) 