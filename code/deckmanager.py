import json
import pymysql
from deck import Deck
from card import Card, CreatureCard, SorceryCard, LandCard, InstantCard

TYPE = 8

CREATURE_CARD = 3
INSTANT_CARD = 7
LAND_CARD = 8
SORCERY_CARD = 14

class DeckManager:

	def __init__(self):

		self.__decks = []

	def add(self):

		file = None
		json_s = None
		database = None
		db_cursor = None
		number_of_rows = 0
		sql_request = None

		try:
			with open("db_config.json") as file:
				json_s = json.load(file)
		except OSError:
			sys.exit("Impossible d'ouvrir le fichier JSON")

		# Connexion à la DB via l'API en python
		database = pymysql.connect(host = "localhost", user = json_s['username'], password = json_s['password'], db = json_s['dbname'])

		# Création du curseur
		db_cursor = database.cursor()

		# Récupération des cartes (45 premières)
		number_of_rows = 45
		db_cursor.execute("""
				 SELECT DISTINCT CAR_ID, CAR_NAME, CAR_COLORS, CAR_MANACOST, CAR_COLORIDENTITY, CAR_TEXT, CAR_POWER, CAR_TOUGHNESS, CTY_ID, CTY_NAME
				 FROM mag_setcard, mag_set, mag_card, mag_cardtypeli, mag_cardtype
				 WHERE SET_ID = SCA_SET 
				 AND SCA_CARD = CAR_ID
				 AND CTYL_CARD = CAR_ID
				 AND CTYL_TYPE = CTY_ID
				 ORDER BY CAR_ID
				 """)
		sql_request = db_cursor.fetchmany(number_of_rows)

		# Créations du deck
		deck = Deck("Deck de démarrage")
		for card in sql_request:

			if(card[TYPE] == CREATURE_CARD):
				deck.add_card(CreatureCard(card))
			
			elif(card[TYPE] == LAND_CARD):
				deck.add_card(LandCard(card))
			
			elif(card[TYPE] == INSTANT_CARD):
				deck.add_card(InstantCard(card))
			
			elif(card[TYPE] == SORCERY_CARD):
				deck.add_card(SorceryCard(card))

		# Ajout du deck dans le deckmanager
		self.__decks.append(deck)

	def remove(self, index):

		if(index < len(self.__decks)):
			self.__decks.pop(index)

		else:
			print("Il n'y a pas de deck à cet index")

	def get_deck(self, index):

		if(index < len(self.__decks)):
			return self.__decks[index]

		else:
			if(len(self.__decks) == 0) :
				self.add()
			
			print("Il n'y a pas de deck à cet index, récupération du deck de base")
			
			return self.__decks[0]

	def size(self):

		return len(self.__decks)

