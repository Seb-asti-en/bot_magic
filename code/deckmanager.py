############################ Import ############################
import json, sys, copy
from creaturecard  import CreatureCard
from sorcerycard import SorceryCard
from instantcard import InstantCard
from landcard import LandCard
from deck import Deck
from card import Card


class DeckManager:

	############################ Constructeur ############################
	def __init__(self):
		self.__decks = []


	############################ Getters ############################
	def get_deck(self, index = 0):
		if(abs(index) < len(self.__decks)):
			return self.__decks[index]
		else:
			print("Il n'y a pas de deck à cet index, récupération du deck de base")
			sys.exit(0)


	############################ Méthode ############################
	##
	# Ajoute un deck dans le deck manager grace à la recherche du nom dans le JSON des decks
	# @param name 	Le nom du deck voulu
	##
	def add(self, name):
		json_cards = None
		json_deck = None
		cards = None
		deck = None
		
		#Ouverture du JSON des decks
		try:
			with open("JSON/decks.json") as file:
				json_deck = json.load(file)
		except OSError:
			sys.exit("Impossible d'ouvrir le fichier decks JSON")
		
		#recupère le JSON du deck
		for recup_deck in json_deck["decks"]:
			if name in recup_deck["Name"]:
				deck = Deck(name,[])
				cards = recup_deck["cards"]
				try:
					with open("JSON/all_cards.json") as file:
						json_cards = json.load(file)
				except OSError:
					sys.exit("Impossible d'ouvrir le fichier decks JSON")
		
		#Ajoute chaque carte du json_all_cards grace au json_deck
		for d_card in cards:
			for j_card in json_cards["cards"]:
				if j_card["Id"] == int(d_card["Id"]):
		 			for y in range(int(d_card["copy"])):
		 				if "Creature" in j_card["Type"]:
		 					deck.add_card(CreatureCard(j_card))
		 				elif "Land" in j_card["Type"]:
		 					deck.add_card(LandCard(j_card))
		 				elif "Instant" in j_card["Type"]:
		 					deck.add_card(InstantCard(j_card))
		 				elif "Sorcery" in j_card["Type"] :
		 					deck.add_card(SorceryCard(j_card))
		 				elif "Enchantment" in j_card["Type"]:
		 					deck.add_card(Card(j_card))
		 				elif "Artifact" in j_card["Type"]:
							 deck.add_card(Card(j_card))
 				
 		# Ajout du deck dans le deckmanager
		self.__decks.append(deck)

	##
	# Retire le deck du manager deck à l'index voulu
	# @param index 	l'index du deck dans le deck manager
	##
	def remove(self, index):
		if(index < len(self.__decks)):
			self.__decks.pop(index)
		else:
			print("Il n'y a pas de deck à cet index")

	##
	# Retourne la taille du deck manager
	##
	def size(self):
		return len(self.__decks)

	##
	# Copie un deck grace a l'index d'un deck
	# @param index 	l'index du deck à copier
	##
	def copy_deck(self, index):
		return copy.deepcopy(self.get_deck(index))

