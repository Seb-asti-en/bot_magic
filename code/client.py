#!/usr/bin/env python3

import socket, pickle, sys, json, os, random, time
from player import Player

DEBUG = False

PACKET_SIZE = 1024

SHOW_GAME = "S"
MULLIGAN = "0"
DRAW_CARD = "1"
TAP_LAND = "2"
PLAY_CARD = "3"
USE_EFFECT = "4"
SELECT = "5"
ATTACK = "6"
BLOCK = "7"
SKIP_PHASE = "8"
CONCEDE = "9"

HUMAN = "1"
BOT_RANDOM = "2"
BOT_SKIP = "3"

ID = 0
LIFE = 1
MANA = 2
DECK = 3
HAND = 4
BATTLE_ZONE = 5
LAND_ZONE = 6
GRAVEYARD = 7
EXILE = 8

SELECTION_PLAYER = 0
SELECTION_DECK = 1
SELECTION_HAND = 2
SELECTION_BATTLEZONE = 3
SELECTION_LANDZONE = 4
SELECTION_GRAVEYARD = 5
SELECTION_EXILE = 6

TARGET_ID = 0
TARGET_TYPE = 1
TARGET_POSITION = 2

def main():

	client = None

	client = Client()

	# Connexion au serveur principal
	client.connect_server()

	# Connexion au serveur de jeu
	client.connect_game()

	# Lancement de la partie
	result = client.play()

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
		self.__player_id = -1
		self.__players = []
		self.__behaviour = ""

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

		main_input = ""
		behaviour_input = ""

		while True:

			self.clear_terminal()

			print("[      Nouvelle partie (1)     ]")
			print("[   Rejoindre une partie (2)   ]")
			print("[         Quitter (3)          ]")

			main_input = input(">")

			if(main_input.isnumeric() and int(main_input) in range(1,4)):

					break

		if(int(main_input) in range(1,3)):

			while True:

				self.clear_terminal()

				print("HUMAN (1)")
				print("BOT_RANDOM (2)")
				print("BOT_SKIP (3)")

				behaviour_input = input(">")

				if(behaviour_input.isnumeric()):

					if(behaviour_input == HUMAN):

						self.__behaviour = "HUMAN"

						break

					elif(behaviour_input == BOT_RANDOM):

						self.__behaviour = "BOT_RANDOM"

						break

					elif(behaviour_input == BOT_SKIP):

						self.__behaviour = "BOT_SKIP"

						break

		return main_input

	def clear_terminal(self):

		command = "clear"

		if os.name == "nt":
			command = "cls"

		os.system(command)

	def update(self, gamestate):

		for player in gamestate:

			if(player[LIFE] != None):

				self.__players[player[ID]].set_life(player[LIFE])

			if(player[MANA] != None):

				self.__players[player[ID]].set_mana_pool(player[MANA])

			if(player[DECK] != None):

				self.__players[player[ID]].get_board().set_deck(player[DECK])

			if(player[HAND] != None):

				self.__players[player[ID]].get_board().set_hand(player[HAND])

			if(player[BATTLE_ZONE] != None):

				self.__players[player[ID]].get_board().set_battle_zone(player[BATTLE_ZONE])

			if(player[LAND_ZONE] != None):

				self.__players[player[ID]].get_board().set_land_zone(player[LAND_ZONE])

			if(player[GRAVEYARD] != None):

				self.__players[player[ID]].get_board().set_graveyard(player[GRAVEYARD])

			if(player[EXILE] != None):

				self.__players[player[ID]].get_board().set_exile(player[EXILE])

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

	def input(self, min_value, max_value):

		input_value = -1

		if(self.__behaviour == "HUMAN"):

			input_value = input(">")

		elif(self.__behaviour == "BOT_RANDOM"):

			input_value = random.randint(min_value,max_value)

			# time.sleep(0.25)

		elif(self.__behaviour == "BOT_SKIP"):

			if(random.randint(0,10) > 2):

				input_value = 8

			else:

				input_value = 1

		return str(input_value)

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
	
		# Connexion au serveur de jeu
		self.__game_socket.connect(self.__game_netconfig)

		# Réception depuis le serveur de jeu : ID Player (1)
		self.__player_id = int(self.recv_signal())

		# Réception depuis le serveur de jeu : Objet Player (2)
		self.__players = self.recv_gamestate()

	def play(self):

		result = ""
		request = None
		response = None
		gamestate = None

		while True:

			# Réception depuis le serveur de jeu : Signal (3)
			response = self.recv_signal()

			if(response == "PLAY"):

				# Choix de l'action
				request = self.action_menu()

				# Envoi vers le serveur de jeu : Requête d'action (4)
				self.send_action(request)

				# Réception depuis le serveur de jeu : Acceptation / Refus (5)
				response = self.recv_signal()

				# En cas d'acceptation
				if(response == "ACCEPT"):

					# Réception depuis le serveur de jeu : Etat de la partie (6)
					gamestate = self.recv_gamestate()

					# Mise à jour des informations de jeu
					self.update(gamestate)
					
					if(DEBUG):
						print("MAJ DE LA PARTIE")	

				# En cas de refus, on recommence
				elif(response == "DECLINE"):
					continue

			elif(response == "GAME_UPDATE"):

				# Réception depuis le serveur de jeu : Etat de la partie
				gamestate = self.recv_gamestate()

				# Mise à jour des informations de jeu
				self.update(gamestate)
				
				if(DEBUG):
					print("MAJ DE LA PARTIE")

			elif(response == "DEATH"):
					
				result = "DEFEAT"
				
				break

			elif(response == "VICTORY"):

				result = "VICTORY"

				break

		return result

	def action_menu(self):

		user_input = ""
		request = ""
		i = 0
		identity = []
		selecting = True

		if(DEBUG):
			input("[CLEAR SCREEN]")

		while True :

			# Rafraichissement de l'écran
			self.clear_terminal()

			# Affichage initial
			print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
			print("[  SHOW_GAME  (S)  ]")
			print("[  MULLIGAN   (0)  ]")
			print("[  DRAW_CARD  (1)  ]")
			print("[  TAP_LAND   (2)  ]")
			print("[  PLAY_CARD  (3)  ]")
			print("[  USE_EFFECT (4)  ]")
			print("[  SELECT     (5)  ]")
			print("[  ATTACK     (6)  ]")
			print("[  BLOCK      (7)  ]")
			print("[  SKIP_PHASE (8)  ]")
			print("[  CONCEDE    (9)  ]")

			# Récupération de l'entrée utilisateur
			user_input = self.input(0,8)

			if(user_input == SHOW_GAME):

				# Rafraichissement de l'écran
				self.clear_terminal()

				for player in self.__players:

					print("Player", player.get_id(), "-", player.get_life(), "HP - Deck :", len(player.get_board().get_deck().get_cards()))
					print(player.get_mana_pool())

					for card in player.get_board().get_hand():
						
						print("[" + card._name, end="] ")

					print()

					for card in player.get_board().get_land_zone():
						
						if(card.is_tapped()):
							
							print("[(T)" + card._name, end="] ")

						else:
							
							print("[" + card._name, end="] ")

					print()

					for card in player.get_board().get_battle_zone():

						if(card.is_sick()):

							if(card.is_tapped()):

								print("[(S)(T)" + card._name, end="] ")

							else:
							
								print("[(S)" + card._name, end="] ")

						else:
							
							if(card.is_tapped()):

								print("[(T)" + card._name, end="] ")

							else:
								
								print("[" + card._name, end="] ")

					print()

				input(">")

			elif(user_input == MULLIGAN):

				request = { 
					"player" : self.__player_id,
					"type" : "MULLIGAN"
				}

				break

			elif(user_input == DRAW_CARD):
				
				request = { 
					"player" : self.__player_id,
					"type" : "DRAW_CARD"
				}

				break

			elif(user_input == TAP_LAND):

				if(self.__players[self.__player_id].landzone_size() > 0):

					while True:

						i = 0

						# Rafraichissement de l'écran
						self.clear_terminal()

						# Affichage de nos cartes terrain
						print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
						for card in self.__players[self.__player_id].get_board().get_land_zone():

							if(card.is_tapped()):
								
								print("(T)" + card.get_name() + "(" + str(i) + ")")

							else:

								print(card.get_name() + "(" + str(i) + ")")

							i = i + 1

						# Récupération de l'entrée utilisateur
						user_input = self.input(0,self.__players[self.__player_id].landzone_size()-1)

						if(user_input.isnumeric()):

							user_input = int(user_input)

							if(user_input >= 0 and user_input < self.__players[self.__player_id].landzone_size()):

								identity = self.__players[self.__player_id].get_board().get_land_zone()[user_input].get_identity()

								request = { 
									"player" : self.__player_id,
									"type" : "TAP_LAND",
									"landzone_position" : user_input,
									"color" : ""
								}								

								if(len(identity) == 1):

									request["color"] = identity[0]

								else:

									while True:

										i = 0

										# Rafraichissement de l'écran
										self.clear_terminal()

										# TODO : Ajouter la gestion des mana double via un menu de selection (compliqué)
										for color in identity:

											print(color + " (" + str(i) + ")")

											i += 1

										# Récupération de l'entrée utilisateur
										user_input = self.input(0,len(identity)-1)

										if(user_input.isnumeric()):

											user_input = int(user_input)

											if(user_input >= 0 and user_input < len(identity)):

												request["color"] = identity[user_input]

												break

								break

					break

			elif(user_input == PLAY_CARD):

				if(self.__players[self.__player_id].hand_size() > 0):

					while True:

						i = 0

						# Rafraichissement de l'écran
						self.clear_terminal()

						# Affichage des cartes
						print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
						for card in self.__players[self.__player_id].get_board().get_hand():

							print(card.get_name() + "(" + str(i) + ")")

							i = i + 1

						# Récupération de l'entrée utilisateur
						user_input = self.input(0,self.__players[self.__player_id].hand_size()-1)	

						if(user_input.isnumeric()):

							user_input = int(user_input)

							if(user_input >= 0 and user_input < self.__players[self.__player_id].hand_size()):			

								request = { 
									"player" : self.__player_id,
									"type" : "PLAY_CARD",
									"hand_position" : user_input
								}

								break
					break

			elif(user_input == USE_EFFECT):

				print("y'a r")
				
			elif(user_input == SELECT):

				request = { 
					"player" : self.__player_id,
					"type" : "SELECT",
					"selections" : []
				}

				selecting = True

				while selecting:

					# Choix du joueur
					while True:

						i = 0

						# Rafraichissement de l'écran
						self.clear_terminal()

						# Affichage des joueurs
						for player in self.__players:

							print(f"PLAYER {player.get_id()} ({i})")

							i = i + 1 
						print(f"STOP ({i})")

						# Récupération de l'entrée utilisateur
						user_input = self.input(0,i)

						if(user_input.isnumeric()):

							user_input = int(user_input)

							if(user_input == i):

								selecting = False

								break

							elif(user_input >= 0 and user_input < len(self.__players)):

								request["selections"].append([])

								request["selections"][-1].append(user_input)

								# Choix de la zone
								while True:

									# Rafraichissement de l'écran
									self.clear_terminal()

									# Affichage des zones
									print("PLAYER (0)")
									print("DECK (1)")
									print("HAND (2)")
									print("BATTLE_ZONE (3)")
									print("LAND_ZONE (4)")
									print("GRAVEYARD (5)")
									print("EXILE (6)")

									# Récupération de l'entrée utilisateur
									user_input = self.input(0,6)

									if(user_input.isnumeric()):

										user_input = int(user_input)

										if(user_input == SELECTION_PLAYER):

											request["selections"][-1].append("PLAYER")

											break										

										elif(user_input == SELECTION_DECK):

											request["selections"][-1].append("DECK")

											break

										elif(user_input == SELECTION_HAND):

											request["selections"][-1].append("HAND")

											# Vérification que l'on soit le joueur concerné et qu'on possède des cartes
											if(request["selections"][-1][TARGET_ID] == self.__player_id and self.__players[self.__player_id].hand_size() > 0):

												# Choix de la carte
												while True:

													i = 0

													# Rafraichissement de l'écran
													self.clear_terminal()

													# Affichage des cartes
													for card in self.__players[self.__player_id].get_board().get_hand():
														
														print(f"{card.get_name()} ({i})")

														i = i + 1

													# Récupération de l'entrée utilisateur
													user_input = self.input(0,self.__players[self.__player_id].hand_size()-1)

													if(user_input.isnumeric()):

														user_input = int(user_input)

														if(user_input >= 0 and user_input < self.__players[self.__player_id].hand_size()):	

															request["selections"][-1].append(user_input)

															break
											break

										elif(user_input == SELECTION_BATTLEZONE):

											# Vérification qu'il y ait des cartes dans la zone
											if(self.__players[self.__player_id].battlezone_size() > 0):

												request["selections"][-1].append("BATTLE_ZONE")

												# Choix de la carte
												while True:

													i = 0

													# Rafraichissement de l'écran
													self.clear_terminal()

													# Affichage des cartes
													for card in self.__players[self.__player_id].get_board().get_battle_zone():
														
														print(f"{card.get_name()} ({i})")

														i = i + 1

													# Récupération de l'entrée utilisateur
													user_input = self.input(0,self.__players[self.__player_id].battlezone_size()-1)

													if(user_input.isnumeric()):

														user_input = int(user_input)

														if(user_input >= 0 and user_input < self.__players[self.__player_id].battlezone_size()):	

															request["selections"][-1].append(user_input)

															break
												break

										elif(user_input == SELECTION_LANDZONE):

											# Vérification qu'il y ait des cartes dans la zone
											if(self.__players[self.__player_id].landzone_size() > 0):

												request["selections"][-1].append("LAND_ZONE")

												# Choix de la carte
												while True:

													i = 0

													# Rafraichissement de l'écran
													self.clear_terminal()

													# Affichage des cartes
													for card in self.__players[self.__player_id].get_board().get_land_zone():
														
														print(f"{card.get_name()} ({i})")

														i = i + 1

													# Récupération de l'entrée utilisateur
													user_input = self.input(0,self.__players[self.__player_id].landzone_size()-1)

													if(user_input.isnumeric()):

														user_input = int(user_input)

														if(user_input >= 0 and user_input < self.__players[self.__player_id].landzone_size()):	

															request["selections"][-1].append(user_input)

															break
												break

										elif(user_input == SELECTION_GRAVEYARD):

											# Vérification qu'il y ait des cartes dans la zone
											if(self.__players[self.__player_id].graveyard_size() > 0):

												request["selections"][-1].append("GRAVEYARD")

												# Choix de la carte
												while True:

													i = 0

													# Rafraichissement de l'écran
													self.clear_terminal()

													# Affichage des cartes
													for card in self.__players[self.__player_id].get_board().get_graveyard():
														
														print(f"{card.get_name()} ({i})")

														i = i + 1

													# Récupération de l'entrée utilisateur
													user_input = self.input(0,self.__players[self.__player_id].graveyard_size()-1)

													if(user_input.isnumeric()):

														user_input = int(user_input)

														if(user_input >= 0 and user_input < self.__players[self.__player_id].graveyard_size()):	

															request["selections"][-1].append(user_input)

															break
												break

										elif(user_input == SELECTION_EXILE):

											# Vérification qu'il y ait des cartes dans la zone
											if(self.__players[self.__player_id].exile_size() > 0):

												request["selections"][-1].append("EXILE")

												# Choix de la carte
												while True:

													i = 0

													# Rafraichissement de l'écran
													self.clear_terminal()

													# Affichage des cartes
													for card in self.__players[self.__player_id].get_board().get_exile():
														
														print(f"{card.get_name()} ({i})")

														i = i + 1

													# Récupération de l'entrée utilisateur
													user_input = self.input(0,exile_size()-1)

													if(user_input.isnumeric()):

														user_input = int(user_input)

														if(user_input >= 0 and user_input < self.__players[self.__player_id].exile_size()):	

															request["selections"][-1].append(user_input)

															break
												break
								break
				break

			elif(user_input == ATTACK):

				if(self.__players[self.__player_id].battlezone_size() > 0):

					# Sélection du joueur
					while True:

						# Rafraichissement de l'écran
						self.clear_terminal()

						# Affichage de la liste des joueurs
						print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
						for player in self.__players:

							print("[  Player " + str(player.get_id()) + "  ]")

						# Récupération de l'entrée utilisateur
						user_input = self.input(0,len(self.__players)-1)

						if(user_input.isnumeric()):

							user_input = int(user_input)

							if(user_input >= 0 and user_input < len(self.__players)):

								request = { 
									"player" : self.__player_id,
									"type" : "ATTACK",
									"target" : user_input,
									"attacker" : -1
								}

								break

					# Sélection de la carte attaquante
					while True:

						i = 0

						# Rafraichissement de l'écran
						self.clear_terminal()

						# Affichage des cartes sur notre Battle Zone
						print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
						for card in self.__players[self.__player_id].get_board().get_battle_zone():

							if(card.is_sick()):

								if(card.is_tapped()):

									print("(S)(T)" + card.get_name() + "(" + str(i) + ")")
								
								else:
								
									print("(S)" + card.get_name() + "(" + str(i) + ")")

							else:

								if(card.is_tapped()):

									print("(T)" + card.get_name() + "(" + str(i) + ")")

								else:

									print(card.get_name() + "(" + str(i) + ")")

							i = i + 1

						# Récupération de l'entrée utilisateur
						user_input = self.input(0,self.__players[self.__player_id].battlezone_size()-1)

						if(user_input.isnumeric()):

							user_input = int(user_input)

							if(user_input >= 0 and user_input < len(self.__players[self.__player_id].get_board().get_battle_zone())):

								request["attacker"] = user_input

								break

					break
				
			elif(user_input == BLOCK):

				if(self.__players[self.__player_id].battlezone_size() > 0):

					# Sélection du joueur
					while True:

						# Rafraichissement de l'écran
						self.clear_terminal()

						# Affichage de la liste des joueurs
						print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
						for player in self.__players:

							print("[  Player " + str(player.get_id()) + "  ]")

						# Récupération de l'entrée utilisateur
						user_input = self.input(0,len(self.__players)-1)

						if(user_input.isnumeric()):

							user_input = int(user_input)

							if(user_input >= 0 and user_input < len(self.__players)):

								request = { 
									"player" : self.__player_id,
									"type" : "BLOCK",
									"target" : user_input,
									"ennemy_attacker" : -1,
									"blocker" : -1
								}

								break

					if(self.__players[user_input].battlezone_size() > 0):

						# Sélection de la carte ennemie à bloquer
						while True:

							i = 0

							# Rafraichissement de l'écran
							self.clear_terminal()

							# Affichage de la Battle Zone ennemie
							print("Joueur", request["target"], "(" + str(self.__players[request["target"]].get_life()) + ")")
							for card in self.__players[request["target"]].get_board().get_battle_zone():

								print(card.get_name() + "(" + str(i) + ")")

								i = i + 1

							# Récupération de l'entrée utilisateur
							user_input = self.input(0,self.__players[request["target"]].battlezone_size()-1)

							if(user_input.isnumeric()):

								user_input = int(user_input)

								if(user_input >= 0 and user_input < len(self.__players[request["target"]].get_board().get_battle_zone())):

									request["ennemy_attacker"] = user_input

									break
		
						# Sélection de la carte bloquante
						while True:

							i = 0

							# Rafraichissement de l'écran
							self.clear_terminal()

							# Affichage de notre Battle Zone
							print("Joueur", self.__player_id, "(" + str(self.__players[self.__player_id].get_life()) + ")")
							for card in self.__players[self.__player_id].get_board().get_battle_zone():

								if(card.is_tapped()):
									
									print("(T)" + card.get_name() + "(" + str(i) + ")")

								else:

									print(card.get_name() + "(" + str(i) + ")")

								i = i + 1

							# Récupération de l'entrée utilisateur
							user_input = self.input(0,self.__players[self.__player_id].battlezone_size()-1)

							if(user_input.isnumeric()):

								user_input = int(user_input)

								if(user_input >= 0 and user_input < len(self.__players[self.__player_id].get_board().get_battle_zone())):

									request["blocker"] = user_input

									break

						break

			elif(user_input == SKIP_PHASE):

				request = { 
					"player" : self.__player_id,
					"type" : "SKIP_PHASE"
				}

				break

			elif(user_input == CONCEDE):

				request = { 
					"player" : self.__player_id,
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