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
			with open("db_config.json") as file:
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