#!/usr/bin/env python3

import socket, pickle, sys, json
from deckmanager import DeckManager
from deck import Deck

PACKET_SIZE = 1024
SEGMENT_SIZE = 65536

def main():

	client = None

	client = Client()

	client.connect_server()

	client.connect_game()

	print("YAY")
	

class Client:

	def __init__(self):

		self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__server_netconfig = None
		self.__game_netconfig = None

		try:
			with open("JSON/ip_config.json") as file:
				json_string = json.load(file)
		except Exception:
			sys.exit("Impossible d'ouvrir le fichier JSON")

		# Récupération des informations réseaux du serveur
		self.__server_netconfig = (json_string['host_server'], int(json_string['port_server']))

		# Définition du timeout UDP
		self.__server_socket.settimeout(10.0)

	def menu(self):

		print("[      Nouvelle partie (1)     ]")
		print("[   Rejoindre une partie (2)   ]")
		print("[         Quitter (3)          ]")

		return input(">")

	# Connexion au serveur UDP
	def connect_server(self):

		user_input = ""
		request = ""
		raw_data = None
		data = None
		server_address = None

		while True:

			user_input = self.menu()
			
			# Demande de lancement d'une nouvelle partie
			if user_input == "1":

				request = "NEW_GAME"

				# Envoi vers le serveur : requête initiale (1)
				self.__server_socket.sendto(request.encode(),self.__server_netconfig)

				# Réception depuis le serveur : réponse (2)
				try:

					raw_data,server_address = self.__server_socket.recvfrom(PACKET_SIZE)
					data = pickle.loads(raw_data)
				
				except socket.timeout:
					
					print("Temps d'attente dépassé")
					continue

				print("Message reçu :", data, "de", server_address)

				if(data[0] == "ACCEPT"):
					
					self.__game_netconfig = data[1]
					break

				elif(data[0] == "DECLINE"):

					print(data[1])
					continue

			# Demande de rejoindre une partie
			elif user_input == "2":

				request = "JOIN_GAME"

				# Envoi vers le serveur : requête initiale (1)
				self.__server_socket.sendto(request.encode(),self.__server_netconfig)

				# Réception depuis le serveur : réponse (2)
				try:

					raw_data,server_address = self.__server_socket.recvfrom(PACKET_SIZE)
					data = pickle.loads(raw_data)
				
				except socket.timeout:
					
					print("Temps d'attente dépassé")
					continue

				print("Message reçu :", data, "de", server_address)

				if(data[0] == "ACCEPT"):
					
					self.__game_netconfig = data[1]
					break

				elif(data[0] == "DECLINE"):

					print(data[1])
					continue
				
			# Demande de quitter
			elif user_input == "3":
				
				sys.exit(0)

	# Connexion à la partie
	def connect_game(self):

		deck = None
		raw_data = None
		data = None
	
		# Connexion au serveur de jeu
		self.__game_socket.connect(self.__game_netconfig)
			
		deck = DeckManager().get_deck()

		# Envoi vers le client : Deck (TCP)(1)
		self.__game_socket.send(pickle.dumps(deck))

		# Réception depuis le serveur : Deck (TCP)(2)
		raw_data = self.__game_socket.recv(SEGMENT_SIZE)

		data = pickle.loads(raw_data)
		
		print('Données recues :', data.get_cards()[0].to_string())

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)

# # Apparently safe user-input
# while True:
# 	try:
# 		user_input = input()
# 		break
# 	except ValueError:
# 		continue