#!/usr/bin/env python3

import os
import sys
import json

def main():

	database = Database()

	database.run()
	database.generate()
	database.set_logins()

	input("Appuyez sur ENTER pour éteindre le serveur SQL")

	database.stop()

class Database:

	def __init__(self):

		file = None
		json_string = None

		try:
			with open("JSON/db_config.json") as file:
				json_string = json.load(file)
		except OSError:
			sys.exit("Impossible d'ouvrir le fichier JSON")

		self.__username = json_string['username']
		self.__password = json_string['password']
		self.__dbname 	= json_string['dbname']

	# Lancement du serveur MySQL local
	def run(self):

		print("Lancement du serveur")
	
		if sys.platform.startswith('darwin'):
			os.system("mysql.server start")
		elif sys.platform.startswith('linux'):
			os.system("sudo /etc/init.d/mysql start")

	# Fermeture du serveur MySQL local
	def stop(self):

		print("Arrêt du serveur")

		if sys.platform.startswith('darwin'):
			os.system("mysql.server stop")
		elif sys.platform.startswith('linux'):
			os.system("sudo /etc/init.d/mysql stop")

	# Créer et remplir une base de données
	def generate(self):

		status = None
		privilege = ""
		sql_filepath = "../resources/card_database.sql"
		self.__dbname = "card_database"

		if sys.platform.startswith('linux'):
			privilege = "sudo "

		status = os.system(privilege + "mysql -u root -e \"use " + self.__dbname + "\" 2> /dev/null")
		if (status != 0):
			print("Génération de la base de données")
			os.system(privilege + "mysql -u root -e \"CREATE DATABASE " + self.__dbname + "\"")
			print("Generating cards inside the database, please wait..")
			os.system(privilege + "mysql -u root " + self.__dbname + " < " + sql_filepath)

	# Création de l'utilisateur avec les droits d'accès au serveur
	def set_logins(self):

		privilege = ""
		self.__username = "deck_manager"

		if sys.platform.startswith('linux'):
			privilege = "sudo "

		print("Création des logins de connexion")

		os.system(privilege + "mysql -u root -e \"CREATE USER '" + self.__username + "'@'localhost'\" 2> /dev/null")
		os.system(privilege + "mysql -u root -e \"GRANT ALL ON " + self.__dbname + ".* TO '" + self.__username + "'@'localhost'\"")

main()

class OldDeckManager:

	TYPE = 8

	def __init__(self):

		self.__decks = []

	def get_deck(self, index = 0):

		if(abs(index) < len(self.__decks)):

			return self.__decks[index]

		else:

			print("Il n'y a pas de deck à cet index, récupération du deck de base")
			
			sys.exit(0)

	def add(self):
		file = None
		json_s = None
		database = None
		db_cursor = None
		number_of_rows = 0
		sql_request = None

		duplicates = 0

		try:
			with open("JSON/db_config.json") as file:
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
		deck = Deck("Deck de démarrage",[])
		for card in sql_request:

			if(duplicates > 0):

				if(deck.get_cards()[duplicates-1]._id == card[ID]):
					
					deck.get_cards()[duplicates-1].add_subtype(card[11])
				
				else:
					
					if(card[TYPE] == "Creature"):
					
						deck.add_card(CreatureCard(card,[]))
						duplicates += 1
					
					elif(card[TYPE] == "Instant"):
					
						deck.add_card(InstantCard(card,[]))
						duplicates += 1

					elif(card[TYPE] == "Land"):
						
						deck.add_card(LandCard(card,[]))
						duplicates += 1
					
					elif(card[TYPE] == "Sorcery"):
					
						deck.add_card(SorceryCard(card,[]))
						duplicates += 1
			
			else:
				
				if(card[TYPE] == "Creature"):
				
					deck.add_card(CreatureCard(card,[]))
					duplicates += 1
				
				elif(card[TYPE] == "Instant"):
				
					deck.add_card(InstantCard(card,[]))
					duplicates += 1
				
				elif(card[TYPE] == "Land"):
				
					deck.add_card(LandCard(card,[]))
					duplicates += 1
				
				elif(card[TYPE] == "Sorcery"):
				
					deck.add_card(SorceryCard(card,[]))
					duplicates += 1

		# Ajout du deck dans le deckmanager
		
		self.__decks.append(deck)

	def remove(self, index):

		if(index < len(self.__decks)):
			self.__decks.pop(index)

		else:
			print("Il n'y a pas de deck à cet index")

	def size(self):
		
		return len(self.__decks)

	def copy_deck(self, index):

		return copy.deepcopy(self.get_deck(index))
