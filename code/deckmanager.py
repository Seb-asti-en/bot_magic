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
				 SELECT DISTINCT car_id, car_name, car_colors, car_manacost, car_coloridentity, car_text, car_power, car_toughness, cty_name, cst_name, csu_name, set_name
				 FROM mag_card
				 LEFT JOIN mag_cardtypeli ON ctyl_card = car_id
				 LEFT JOIN mag_cardtype ON cty_id = ctyl_type
				 LEFT JOIN mag_cardsubtypeli ON cstl_card = car_id
				 LEFT JOIN mag_cardsubtype ON cst_id = cstl_subtype
				 LEFT JOIN mag_cardsupertypeli ON csul_card = car_id
				 LEFT JOIN mag_cardsupertype ON csu_id = csul_supertype
				 INNER JOIN mag_setcard ON sca_card = car_id
				 INNER JOIN mag_set ON set_id = sca_set
				 WHERE set_name = "Arena Beginner Set"
				 ORDER BY car_id 
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

