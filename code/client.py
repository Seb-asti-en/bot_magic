#!/usr/bin/env python3

import socket, pickle, sys, json, os
from player import Player

DEBUG = False

PACKET_SIZE = 1024

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

	def send_action(self, action):

		serialized_data = None

		# Sérialisation
		serialized_data = pickle.dumps(action)

		# Envoi vers le serveur de jeu : Taille du segment (1)
		self.send_size(serialized_data)

		# Envoi vers le serveur de jeu : Segment (Requête d'action) (2)
		self.__game_socket.send(serialized_data)
		
		if(DEBUG):
			print("REQUETE D'ACTION :",action,"(envoyé)")


	def send_size(self, segment):

		data = ""
		serialized_data = None

		# Calcul de la taille du segment à envoyer passé en paramètre
		data = '%16s' %len(segment)

		# Sérialisation
		serialized_data = data.encode()

		# Envoi vers le serveur de jeu : Taille du segment
		self.__game_socket.send(serialized_data)

		if(DEBUG):
			print(int(data),"BYTES (envoyé)")

	def recv_signal(self):

		size = 0
		serialized_data = None
		data = ""

		# Réception depuis le serveur de jeu : Taille du segment (1)
		size = self.recv_size()

		# Réception depuis le serveur de jeu : Signal (2)
		serialized_data = self.__game_socket.recv(size)

		# Désérialisation
		data = pickle.loads(serialized_data)

		if(DEBUG):
			print("SIGNAL :",data,"(reçu)")

		return data

	# TODO : (à modifier plus tard selon le format JSON)
	def recv_gamestate(self):

		size = 0
		serialized_data = None
		data = None

		# Réception depuis le serveur de jeu : Taille du segment (1)
		size = self.recv_size()

		# Réception depuis le serveur de jeu : Gamestate (2)
		serialized_data = self.__game_socket.recv(size)

		# Désérialisation
		data = pickle.loads(serialized_data)

		if(DEBUG):
			print("GAMESTATE (reçu)")	

		return data	

	def recv_size(self):

		data = 0
		serialized_data = None

		# Réception depuis le client : Taille du segment (1)
		serialized_data = self.__game_socket.recv(16)

		# Désérialisation
		data = int(serialized_data.decode())

		if(DEBUG):
			print(data,"BYTES (reçu)")

		return data

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
	
		# Connexion au serveur de jeu
		self.__game_socket.connect(self.__game_netconfig)

		# Réception depuis le serveur de jeu : Objet Player (1)
		player = self.recv_gamestate()

		return player

	def play(self, player):

		result = ""
		request = None
		response = None
		gamestate = None

		while True:

			# Réception depuis le serveur de jeu : Signal (2)
			response = self.recv_signal()

			if(response == "PLAY"):

				# Choix de l'action
				request = self.action_menu(player)

				# Envoi vers le serveur de jeu : Requête d'action (3)
				self.send_action(request)

				# Réception depuis le serveur de jeu : Acceptation / Refus (4)
				response = self.recv_signal()

				# En cas de refus, on recommence
				if(response == "DECLINE"):
					continue

				# Réception depuis le serveur de jeu : Etat de la partie (5)
				gamestate = self.recv_gamestate()

				# Mise à jour des informations de jeu
				player = gamestate
				
				if(DEBUG):
					print("MAJ DE LA PARTIE")

				#input(response)

			elif(response == "DEATH"):
					
				result = "DEFEAT"
				
				break

			elif(response == "VICTORY"):

				result = "VICTORY"

				break

		return result

	def action_menu(self, player):

		request = ""

		if(DEBUG):
			input("[CLEAR SCREEN]")

		while True :

			# Rafraichissement de l'écran
			self.clear_terminal()

			# Affichage initial
			print("Joueur", player.get_id(), "(" + str(player.get_life()) + ")")
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

				request = { 
					"player" : player.get_id(),
					"type" : "PLAY_CARD"
				}

				break
				
			elif(user_input == ATTACK):

				request = { 
					"player" : player.get_id(),
					"type" : "ATTACK"
				}

				break
				
			elif(user_input == BLOCK):

				request = { 
					"player" : player.get_id(),
					"type" : "BLOCK"
				}

				break

			elif(user_input == DISCARD):

				request = { 
					"player" : player.get_id(),
					"type" : "DISCARD"
				}

				break

			elif(user_input == SKIP_PHASE):

				request = { 
					"player" : player.get_id(),
					"type" : "SKIP_PHASE"
				}

				break

			elif(user_input == CONCEDE):

				request = { 
					"player" : player.get_id(),
					"type" : "CONCEDE"
				}

				break				

			else:

				input("Erreur lors de la saisie, appuyez sur Entrée pour revenir au menu")

		#input(request)

		return request

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