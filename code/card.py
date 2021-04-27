#!/usr/bin/env python3

import os
import sys
import pymysql # Installer le module avec pip

#Variable global
ID 				= 0
NAME 			= 1
COLOR 			= 2
MANA_COST 		= 3
IDENTITY 		= 4
TEXT 			= 5
POWER 			= 6
TOUGHNESS 		= 7
TYPE 			= 8
SUBTYPE 		= 9
SUPERTYPE 		= 10
COLLECTION  	= 11

def main():

	privilege 		= ""
	status			= None
	db 				= None
	curs 			= None
	cardlen 		= 0
#	row_count 		= 0
	all_db_cards 	= None
	card 			= []
	
	

	# Lancement du serveur MySQL local
	if sys.platform.startswith('darwin'):
		os.system("mysql.server start")
	elif sys.platform.startswith('linux'):
		os.system("sudo /etc/init.d/mysql start")
		privilege = "sudo "

	# Création de l'utilisateur avec les droits d'accès à la DB
	os.system(privilege + "mysql -u root -e \"CREATE USER 'card_manager'@'localhost'\"")
	os.system(privilege + "mysql -u root -e \"GRANT ALL ON card_database.* TO 'card_manager'@'localhost'\"")

	# Génération de la DB si elle n'existe pas
	status = os.system("mysql -u card_manager -e \"use card_database\" 2> /dev/null")
	if (status != 0):
		os.system("mysql -u card_manager -e \"CREATE DATABASE card_database\"")
		print("Generating cards inside the database, please wait..")
		os.system("mysql -u card_manager card_database < ../resources/card_database.sql")

	# Connexion à la DB via l'API en python
	db = pymysql.connect(host="localhost", user="card_manager", password="", db="card_database")
	curs = db.cursor()

	# Récupération des cartes (45 premières)
	curs.execute("""
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
	
	#row_count = 100
	all_db_cards = curs.fetchall()

	# Deconnexion de la DB
	db.close()

	# Suppression de l'utilisateur (vérifier son existence au départ pour une implémentation plus légère)
	os.system(privilege + "mysql -u root -e \"DROP USER 'card_manager'@'localhost'\"")

	# Fermeture du serveur MySQL local
	if sys.platform.startswith('darwin'):
		os.system("mysql.server stop")
	elif sys.platform.startswith('linux'):
		os.system("sudo /etc/init.d/mysql stop")
		
	# Rentre les cartes sorti de la BD dans une liste, gère à moitié les double (problème niveau collection)
	for buffer_card in all_db_cards:
		if(cardlen > 0):
			if(card[cardlen-1]._id == buffer_card[ID]):
				card[cardlen-1].add_subtype(buffer_card[11])
			else:
				if(buffer_card[TYPE] == "Creature"):
					card.append(CreatureCard(buffer_card))
					cardlen += 1
				elif(buffer_card[TYPE] == "Instant"):
					card.append(InstantCard(buffer_card))
					cardlen += 1
				elif(buffer_card[TYPE] == "Land"):
					card.append(LandCard(buffer_card))
					cardlen += 1
				elif(buffer_card[TYPE] == "Sorcery"):
					card.append(SorceryCard(buffer_card))
					cardlen += 1
		else:
			if(buffer_card[TYPE] == "Creature"):
				card.append(CreatureCard(buffer_card))
				cardlen += 1
			elif(buffer_card[TYPE] == "Instant"):
				card.append(InstantCard(buffer_card))
				cardlen += 1
			elif(buffer_card[TYPE] == "Land"):
				card.append(LandCard(buffer_card))
				cardlen += 1
			elif(buffer_card[TYPE] == "Sorcery"):
				card.append(SorceryCard(buffer_card))
				cardlen += 1
		
		
	# Affichage
	for i in card:
		print(i.to_string())
	print("\nNombre de cartes obtenu : " + str(len(card)))

class Card:

	def __init__(self,card):

		self._id			= card[ID]
		self._collection 	= card[COLLECTION]
		self._name			= card[NAME]
		self._supertype		= card[SUPERTYPE]
		self._subtype		= card[SUBTYPE]
		self._colors		= self._init_colors(card)
		self._mana_cost 	= self._init_mana_cost(card)
		self._identity		= self._init_identity(card)
		self._text			= card[TEXT]
		self._effects		= ''
		self._type 			= card[TYPE]
		
	def get_id(self):
		return self._id
	

	def _init_mana_cost(self, card):
		#Initialise le cout en mana à 0
		self._mana_cost = {'X' : 0,'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		#Récup le cout en string | card[MANA_COST] == mana cost dans la table mag_card
		temp = card[MANA_COST]
		#Transforme le string en liste
		res = temp.strip('}{').split('}{')
		#Si il a un cout X de base
		if(res[0].isnumeric()):
			self._mana_cost['X'] = int(res[0])
			res.remove(res[0])
		#Incrémente le cout de chaque couleur
		for x in res:
			try:
				self._mana_cost[x] = self._mana_cost[x] + 1
			except:
				self._mana_cost[x] = 1
		return self._mana_cost
	
	def _init_colors(self, card):
		self._colors = {'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card[COLOR]
		res = temp.split(';')
		for x in res:
			if(x == ''):	
				self._colors['C'] = 1
			else:
				self._colors[x] = 1
		return self._colors
	
	def _init_identity(self, card):
		self._identity = {'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card[IDENTITY]
		res = temp.split(';')
		for x in res:
			if(x == ''):	
				self._identity['C'] = 1
			else:
				self._identity[x] = 1
		return self._identity
		
	def add_subtype(self, subtype):
		if(subtype == None):
			pass
		else:
			self._subtype = self._subtype + ' and ' + subtype
	
	def to_string(self):

		string = ""

		if(self._type == None):
			if("token" in self._name):
				string += "CARD TYPE : TOKEN \n"
		else: 
			string += "CARD TYPE : " + self._type + " \n" 
		string += "ID : " + str(self._id) + " \n" 
		string += "COLLECTION : " + str(self._collection) + "\n"
		string += "NAME : " + self._name + "\n"
		if(self._supertype != None):
			string += "SUPERTYPE : " + self._supertype + "\n"
		if(self._subtype != None):
		    string += "SUBTYPE : " + self._subtype + "\n"
		
		string += "COLOR : "
		if (self._colors['C'] == 1):
			string += "Incolore"
		else :
			if (self._colors['W'] == 1):
				string += "Blanc "
			
			if (self._colors['R'] == 1):
				string += "Rouge "
			
			if (self._colors['G'] == 1):
				string += "Vert "
			
			if (self._colors['U'] == 1):
				string += "Bleu "
			
			if (self._colors['B'] == 1):
				string += "Noir"

		string += "\n"
		
		string += "MANA COST : "
		if (self._mana_cost['X'] > 0):
			string += str(self._mana_cost['X']) + "(Mana) "
			
		if (self._mana_cost['C'] > 0):
			string += str(self._mana_cost['C']) + "(Incolore) "

		if (self._mana_cost['W'] > 0):
			string += str(self._mana_cost['W']) + "(Blanc) "

		if (self._mana_cost['R'] > 0):
			string += str(self._mana_cost['R']) + "(Rouge) "

		if (self._mana_cost['G'] > 0):
			string += str(self._mana_cost['G']) + "(Vert) "

		if (self._mana_cost['U'] > 0):
			string += str(self._mana_cost['U']) + "(Bleu) "

		if (self._mana_cost['B'] > 0):
			string += str(self._mana_cost['B']) + "(Noir)"
		
		string += "\n"
		
		
		string += "IDENTITY : "
		if (self._identity['C'] == 1):
			string += "Incolore"
		else :
			if (self._identity['W'] == 1):
				string += "Blanc "
			
			if (self._identity['R'] == 1):
				string += "Rouge "
			
			if (self._identity['G'] == 1):
				string += "Vert "
			
			if (self._identity['U'] == 1):
				string += "Bleu "
			
			if (self._identity['B'] == 1):
				string += "Noir"

		string += "\n"
		
		if(self._text != None):
			string += "TEXT : " + self._text + "\n"
		#if(self._effects != None):
			#string += "EFFECT : " + str(self._effects) + "\n"
		return string


class CreatureCard(Card):

	def __init__(self, card):
		super().__init__(card)
		self.__power = card[POWER]
		self.__toughness = card[TOUGHNESS]
		
	def to_string(self):
		string = super().to_string()
		string += "POWER : " + str(self.__power) + " \n" 
		string += "TOUGHNESS : " + str(self.__toughness) + "\n"
		return string

class SorceryCard(Card):

	def __init__(self, card):
		super().__init__(card)
		
	def to_string(self):
		string = super().to_string()
		return string
		

class LandCard(Card):

	def __init__(self, card):
		super().__init__(card)
	
	def to_string(self):
		string = super().to_string()
		return string

class InstantCard(Card):

	def __init__(self, card):
		super().__init__(card)
	
	def to_string(self):
		string = super().to_string()
		return string

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)
