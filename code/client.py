#!/usr/bin/env python3

import socket, pickle, sys, json, os
from player import Player

PACKET_SIZE = 1024
SEGMENT_SIZE = 65536

MULLIGAN = "1"
DRAW_CARD = "2"
PLAY_CARD = "3"
ATTACK = "4"
BLOCK = "5"
DISCARD = "6"
SKIP_PHASE = "7"
CONCEDE = "8"

def main():

	client = None
	player = None

	client = Client()

	# Connexion au serveur principal
	client.connect_server()

	# Connexion au serveur de jeu
	player = client.connect_game()

	# Lancement de la partie
	result = client.play(player)

	# Affichage des résultats de la partie
	if(result == "VICTORY"):

		print("Victory !")

	elif(result == "DEFEAT"):

		print("Defeat.")

	else:

		print("Quelque chose has gone terribly mal (:")

	input("Appuyez sur ENTER pour quitter")

	# Déconnexion du serveur
	client.disconnect()

	# Nettoyage en sortie
	client.clear_terminal()

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

	def main_menu(self):

		self.clear_terminal()

		print("[      Nouvelle partie (1)     ]")
		print("[   Rejoindre une partie (2)   ]")
		print("[         Quitter (3)          ]")

		return input(">")

	def clear_terminal(self):

		command = "clear"

		if os.name == "nt":
			command = "cls"

		os.system(command)

	def disconnect(self):

		self.__game_socket.close()
		self.__server_socket.close()

	# Connexion au serveur UDP
	def connect_server(self):

		user_input = ""
		request = ""
		raw_data = None
		data = None
		server_address = None

		while True:

			# Menu principal
			user_input = self.main_menu()

			# Rafraichissement de l'écran
			self.clear_terminal()
			
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

		player = None
		serialized_data = None
	
		# Connexion au serveur de jeu
		self.__game_socket.connect(self.__game_netconfig)

		# Réception depuis le serveur de jeu : Objet Player (1)
		serialized_data = self.__game_socket.recv(SEGMENT_SIZE)

		# Désérialisation
		player = pickle.loads(serialized_data)

		return player

	def play(self, player):

		result = ""
		request = None
		serialized_request = None
		response = None
		serialized_response = None
		gamestate = None

		while True:

			print("En attente de la fin du tour ennemi")

			# Réception depuis le serveur de jeu : Démarrage de la phase (2)
			serialized_response = self.__game_socket.recv(SEGMENT_SIZE)

			# Déserialisation
			response = pickle.loads(serialized_response)

			if(response == "PHASE_START"):
				break

		while True:

			# Choix de l'action
			request = self.action_menu(player)

			# Sérialisation
			serialized_request = pickle.dumps(request)

			# Envoi vers le serveur de jeu : Requête d'action (3)
			self.__game_socket.send(serialized_request)

			# Réception depuis le serveur de jeu : Acceptation / Refus (4)
			serialized_response = self.__game_socket.recv(SEGMENT_SIZE)

			# Déserialisation
			response = pickle.loads(serialized_response)

			input(response)

			# En cas de refus, on recommence
			if(response == "DECLINE"):
				continue

			elif(response == "PHASE_END"):
				
				while True:
					
					print("En attente de la fin du tour ennemi")

					# Réception depuis le serveur de jeu : Démarrage de la phase (2)
					serialized_response = self.__game_socket.recv(SEGMENT_SIZE)

					# Déserialisation
					response = pickle.loads(serialized_response)

					if(response == "PHASE_START"):
						input("Putain de merde")

						break

					elif(response == "VICTORY"):
						break

					elif(response == "DEATH"):
						break
				
				if(response == "PHASE_START"):
					continue

				elif(response == "DEATH"):
				
					result = "DEFEAT"
					
					break

				elif(response == "VICTORY"):

					result = "VICTORY"

					break

			elif(response == "DEATH"):
				
				result = "DEFEAT"
				
				break

			elif(response == "VICTORY"):

				result = "VICTORY"

				break

			# Réception depuis le serveur de jeu : Etat de la partie (5)
			serialized_response = self.__game_socket.recv(SEGMENT_SIZE)

			# Déserialisation
			gamestate = pickle.loads(serialized_response)

			# Mise à jour des informations de jeu
			self.update(player, gamestate)

		return result

	def action_menu(self, player):

		request = ""

		while True :

			# Rafraichissement de l'écran
			self.clear_terminal()

			# Affichage initial
			print("[  MULLIGAN   (1)  ]")
			print("[  DRAW_CARD  (2)  ]")
			print("[  PLAY_CARD  (3)  ]")
			print("[  ATTACK     (4)  ]")
			print("[  BLOCK      (5)  ]")
			print("[  DISCARD    (6)  ]")
			print("[  SKIP_PHASE (7)  ]")
			print("[  CONCEDE    (8)  ]")

			# Récupération de l'entrée utilisateur
			user_input = input(">")

			if(user_input == MULLIGAN):

				request = { 
					"player" : player.get_id(),
					"type" : "MULLIGAN"
				}

				break

			elif(user_input == DRAW_CARD):
				
				request = { 
					"player" : player.get_id(),
					"type" : "DRAW_CARD"
				}

				break

			elif(user_input == PLAY_CARD):
				
				break

			elif(user_input == SKIP_PHASE):

				request = { 
					"player" : player.get_id(),
					"type" : "SKIP_PHASE"
				}

				break				

			else:

				input("Erreur lors de la saisie, appuyez sur Entrée pour revenir au menu")

		#input(request)

		return request

	def update(self, player, gamestate):
		pass

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