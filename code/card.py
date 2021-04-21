#!/usr/bin/env python3

#### PARTIE SQL ####
# Connexion localhost via wamp/phpmyadmin
import os
import sys
import pymysql # Installer le module avec pip

status = None

# Lancement du serveur MySQL local
if sys.platform.startswith('darwin'):

	os.system("mysql.server start")

	status = os.system("mysql -u root -e \"use card_database\" 2> /dev/null")
	if (status != 0):
		os.system("mysql -u root -e \"CREATE DATABASE card_database\"")
		print("Generating cards inside the database, please wait..")
		os.system("mysql -u root card_database < ../resources/card_database.sql")

elif sys.platform.startswith('linux'):
	
	os.system("sudo /etc/init.d/mysql start")

	status = os.system("sudo mysql -u root -e \"use card_database\" 2> /dev/null")
	if (status != 0):
		os.system("sudo mysql -u root -e \"CREATE DATABASE card_database\"")
		print("Generating cards inside the database, please wait..")
		os.system("sudo mysql -u root card_database < ../resources/card_database.sql")

db = pymysql.connect(host="127.0.0.1", user="root", password="", db="card_database")

curs = db.cursor()

curs.execute("""
			 SELECT DISTINCT CAR_ID, CAR_NAME, CAR_COLORS, CAR_MANACOST, CAR_COLORIDENTITY, CAR_TEXT, CAR_POWER, CAR_TOUGHNESS, CTY_ID, CTY_NAME
			 FROM MAG_SETCARD, MAG_SET, MAG_CARD, MAG_CARDTYPELI, MAG_CARDTYPE
			 WHERE SET_ID = SCA_SET 
			 AND SCA_CARD = CAR_ID
			 AND CTYL_CARD = CAR_ID
			 AND CTYL_TYPE = CTY_ID
			 ORDER BY CAR_ID
			 """)
row_count = 45
all_db_cards = curs.fetchmany(row_count)	
#all_db_cards = curs.fetchall()	
db.close()

# Fermeture du serveur MySQL local
if sys.platform.startswith('darwin'):

	os.system("mysql.server stop")

elif sys.platform.startswith('linux'):
	
	os.system("sudo /etc/init.d/mysql stop")

#### FIN SQL ####

class Card:

	def __init__(self,card):

		self._id			= card[0]
		self._collection 	= ''
		self._name			= card[1]
		self._supertype		= ''
		self._subtype		= ''
		self._init_colors(card)
		self._init_mana_cost(card)
		self._init_identity(card)
		self._text			= ''
		self._effects		= ''
		self._type 		= card[9]
		
	def get_id(self):
		return self._id
	

	def _init_mana_cost(self, card):
		#Initialise le cout en mana à 0
		self._mana_cost = {'X' : 0,'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		#Récup le cout en string | card[3] == mana cost dans la table mag_card
		temp = card[3]
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
	
	def _init_colors(self, card):
		self._colors = {'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card[2]
		res = temp.split(';')
		for x in res:
			self._colors[x] = self._colors[x] + 1
	
	def _init_identity(self, card):
		self._identity = {'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card[4]
		res = temp.split(';')
		for x in res:
			self._identity[x] = self._identity[x] + 1
		
	def print_colors(self):
		print(self._colors)
		
	def print_mana_cost(self):
		print(self._mana_cost)
		
	def print_identity(self):
		print(self._identity)
	
	def to_string(self):

		string = ""

		string += "CARD TYPE : " + self._type + " \n" 
		string += "Id : " + str(self._id) + " \n" 
		string += "Collection : " + str(self._collection) + "\n"
		string += "Name : " + self._name + "\n"
		string += "Supertype and subtype : " + self._supertype + " " + self._subtype + "\n"
		
		string += "Color : "
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
		
		string += "Mana cost : "
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
		
		
		string += "Identity : "
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
		
		string += "Text : " + self._text + "\n"
		return string


class CreatureCard(Card):

	def __init__(self, card):
		super().__init__(card)
		self.__power = card[6]
		self.__toughness = card[7]
		
	def to_string(self):
		string = super().to_string()
		string += "Power : " + str(self.__power) + " \n" 
		string += "Toughness : " + str(self.__toughness) + "\n"
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


#### TEST D'UNE CARTE ####
card = []
for x in all_db_cards:
	if(x[8] == 3):
		card.append(CreatureCard(x))
	if(x[8] == 14):
		card.append(SorceryCard(x))
	if(x[8] == 8):
		card.append(LandCard(x))
	if(x[8] == 7):
		card.append(InstantCard(x))
	
creature = CreatureCard(all_db_cards[0])
	
for i in card:
	print(i.to_string())
	