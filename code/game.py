import socket, pickle, sys, os
from deckmanager import DeckManager
from player import Player
from log import Log

DEBUG = False

SOCKET = 0
PLAYER = 1
PLAYER_LIFE = 10

DEFAULT_DECK = "White"

ID = 0
LIFE = 1
MANA = 2
DECK = 3
HAND = 4
BATTLE_ZONE = 5
LAND_ZONE = 6
GRAVEYARD = 7
EXILE = 8

IDLE = -1

TARGET_ID = 0
TARGET_TYPE = 1
TARGET_POSITION = 2

class Game:

	def __init__(self, socket, slots = 2):

		self.__socket = socket
		self.__deckmanager = DeckManager()
		self.__slots = slots
		self.__players = []
		self.__dead_players = []
		self.__log = Log()

		# Création du fichier de log
		self.__log.start(socket.getsockname()[1])

	def get_socket(self):
		return self.__socket

	def get_deckmanager(self):
		return self.__deckmanager
	
	def netconfig(self):
		return self.__socket.getsockname()

	def is_full(self):
		return len(self.__players) >=  self.__slots

	def clear_terminal(self):

		command = "clear"

		if os.name == "nt":
			command = "cls"

		os.system(command)

	def players_alive(self):

		alive = 0

		for player in self.__players:

			if(player[PLAYER].get_life() > 0): 

				alive += 1

		return alive

	def choose_gamestate(self, choice):

		player_id = 0
		gamestate = []

		if(choice == "INIT"):

			for player in self.__players:

				gamestate.append(player[PLAYER])

		elif(choice == "ALL"):

			for player in self.__players:

				player_state = [player[PLAYER].get_id(),None,None,None,None,None,None,None,None]	

				player_state[LIFE] = player[PLAYER].get_life()
				player_state[MANA] = player[PLAYER].get_mana_pool()
				player_state[DECK] = player[PLAYER].get_board().get_deck()
				player_state[HAND] = player[PLAYER].get_board().get_hand()
				player_state[BATTLE_ZONE] = player[PLAYER].get_board().get_battle_zone()
				player_state[LAND_ZONE] = player[PLAYER].get_board().get_land_zone()
				player_state[GRAVEYARD] = player[PLAYER].get_board().get_graveyard()
				player_state[EXILE] = player[PLAYER].get_board().get_exile()

				gamestate.append(player_state)

		elif(choice == "EMPTY"):

			gamestate.append([None,None,None,None,None,None,None,None,None])

		elif(choice):

			for player_choice in choice: 

				player_state = [player_choice[ID],None,None,None,None,None,None,None,None]

				if("LIFE" in player_choice):
					
					player_state[LIFE] = self.__players[player_state[ID]][PLAYER].get_life()

				if("MANA" in player_choice):

					player_state[MANA] = self.__players[player_state[ID]][PLAYER].get_mana_pool()

				if("DECK" in player_choice):
					
					player_state[DECK] = self.__players[player_state[ID]][PLAYER].get_board().get_deck()

				if("HAND" in player_choice):
					
					player_state[HAND] = self.__players[player_state[ID]][PLAYER].get_board().get_hand()

				if("BATTLE_ZONE" in player_choice):

					player_state[BATTLE_ZONE] = self.__players[player_state[ID]][PLAYER].get_board().get_battle_zone()

				if("LAND_ZONE" in player_choice):

					player_state[LAND_ZONE] = self.__players[player_state[ID]][PLAYER].get_board().get_land_zone()

				if("GRAVEYARD" in player_choice):

					player_state[GRAVEYARD] = self.__players[player_state[ID]][PLAYER].get_board().get_graveyard()
				
				if("EXILE" in player_choice):

					player_state[EXILE] = self.__players[player_state[ID]][PLAYER].get_board().get_exile()

				gamestate.append(player_state)

		return gamestate

	def kill_player(self, index):

		# Envoi vers le client : Signal de mort
		self.send_signal(index,"DEATH")

		# Mise à jour des morts
		self.__dead_players.append(index)

		self.__log.write(f"Joueur {index+1} est une sombre merde, il est mort comme un chien")

	def concede(self, index):

		gamestate = None

		# Envoi vers le client : Acceptation
		self.send_signal(index,"ACCEPT")
		
		# On met la vie du joueur à 0
		self.__players[index][PLAYER].set_life(0)

		# Envoi vers le client : Etat de la partie
		gamestate = self.choose_gamestate([[index,"LIFE"]])
		self.send_gamestate(index,gamestate)

		self.__log.write(f"Joueur {index+1} renonce à la victoire")
		
		# Mise à mort du joueur
		self.kill_player(index)

	def use_effect(self, index, card_zone, card_position, temporality):

		is_accepted = True
		data = None
		selections_buffer = None
		card = None
		fitting_effects = []
		target_card = None

		# Envoi vers le client : Signal de jeu
		self.send_signal(index,"PLAY")

		# Réception depuis le client : Paramètres pour chaque effet (SELECT)
		data = self.recv_action(index)

		# Vérification du type d'action
		if(data["type"] == "SELECT"):

			# Copie du choix de cible pour garder l'intégrité lors des vérification
			selections_buffer = data["selections"][:]

			# Récupération de la carte
			if(card_zone == "HAND"):

				card = self.__players[index][PLAYER].get_board().get_hand()[card_position]

			elif(card_zone == "LAND_ZONE"):

				card = self.__players[index][PLAYER].get_board().get_land_zone()[card_position]

			elif(card_zone == "BATTLE_ZONE"):

				card = self.__players[index][PLAYER].get_board().get_battle_zone()[card_position]

			# Récupération des effets à la bonne temporalité
			for effect in card.get_effect():

				# Vérification de la temporalité
				if(effect.get_temporality() == temporality):

					# Ajout à la liste des effets valides pour cette temporalité
					fitting_effects.append(effect)

			# Vérification qu'il y ait au moins un effet valide
			if(len(fitting_effects) > 0):

				# # Vérification du coût par effet
				# for effect in fitting_effects:

				# 	# Récupération du type de coût de l'effet
				# 	cost_type = effect.get

				for effect in fitting_effects:

					# Vérification qu'il reste au moins une sélection
					if(len(selections_buffer) > 0):

						# Vérification du type de cible
						if("player" in effect.get_target()):

							# Vérification du formatage
							if(selections_buffer[0][TARGET_TYPE] == "PLAYER"):

								# Vérification du joueur visé
								if(selections_buffer[0][TARGET_ID] >= 0 and selections_buffer[0][TARGET_ID] < len(self.__players) and selections_buffer[0][TARGET_ID] not in self.__dead_players):

									# Mise à jour de la sélection
									selections_buffer.pop(0)

								else:

									is_accepted = False

									break

							else:

								is_accepted = False

								break

						elif("creature" in effect.get_target()):
							
							# La cible est la carte elle même
							if("self" in effect.get_target()):

								# Vérification du formatage : index joueur
								if(selections_buffer[0][TARGET_ID] == index):

									# Vérification du formatage : zone, position
									if(selections_buffer[0][TARGET_TYPE] == card_zone and selections_buffer[0][TARGET_POSITION] == card_position):
									
										# Mise à jour de la sélection
										selections_buffer.pop(0)

									else:

										is_accepted = False

										break

								else:

									is_accepted = False

									break

							else :

								# Vérification du formatage : index joueur
								if(selections_buffer[0][TARGET_ID] >= 0 and selections_buffer[0][TARGET_ID] < len(self.__players)):

									# Vérification du formatage : zone, position	
									if(selections_buffer[0][TARGET_TYPE] == "BATTLE_ZONE" and selections_buffer[0][TARGET_POSITION] >= 0 and selections_buffer[0][TARGET_POSITION] < self.__players[selections_buffer[0][TARGET_ID]][PLAYER].battlezone_size()):

										target_card = self.__players[selections_buffer[0][TARGET_ID]][PLAYER].get_board().get_battle_zone()[selections_buffer[0][TARGET_POSITION]]

										# La cible doit être en train d'attaquer
										if("attack" in effect.get_target()):

											if(not target_card.is_attacking()):

												is_accepted = False

												break

										# La cible doit être en train de bloquer
										elif("block" in effect.get_target()):

											if(not target_card.is_blocking()):

												is_accepted = False

												break

										# La cible doit être engagée
										elif("tapped" in effect.get_target()):

											if(not target_card.is_tapped()):

												is_accepted = False

												break																						

										# Mise à jour de la sélection
										selections_buffer.pop(0)

									else:

										is_accepted = False

										break

								else:

									is_accepted = False

									break

						elif("move" in effect.get_target()):
							is_accepted = False
							break
							
						#other targets
						else:
							is_accepted = False

							break
					
					#empty selection
					else:
						is_accepted = False

						break

				# Vérification de l'intégrité de la sélection du client pour activer les effets
				if(is_accepted and len(selections_buffer) == 0):

					for effect in fitting_effects:

						# Vérification du type de cible
						if("player" in effect.get_target()):
												
							# Activation de l'effet
							effect.effect(self.__players[data["selections"][0][TARGET_ID]][PLAYER])

						elif("creature" in effect.get_target()):
							
							# Activation de l'effet
							effect.effect(self.__players[data["selections"][0][TARGET_ID]][PLAYER].get_board().get_battle_zone()[data["selections"][0][TARGET_POSITION]])

						elif("move" in effect.get_target()):
							pass

						# Mise à jour
						data["selections"].pop(0)

				else:
					
					is_accepted = False

					self.__log.write(f"La sélection de cibles du Joueur {index+1} est incorrecte")

			# Vérification que la carte ne soit ni une créature ni un terrain dans le cas où elle n'a pas d'effet valide
			elif(card.get_type() != "Creature" and card.get_type() != "Land"):

				is_accepted = False

		else:

			self.__log.write(f"Joueur {index+1} dit n'importe quoi")

		return is_accepted

	def send_signal(self, index, data):

		serialized_data = None

		# Sérialisation
		serialized_data = pickle.dumps(data)

		# Envoi vers le client : Taille du segment (1)
		self.send_size(index,serialized_data)

		# Envoi vers le client : Segment (signal) (2)
		self.__players[index][SOCKET].send(serialized_data)
		
		if(DEBUG):
			print(data,"(envoyé)")

	def send_gamestate(self, index, gamestate):

		serialized_data = None

		# Sérialisation
		serialized_data = pickle.dumps(gamestate)

		# Envoi vers le client : Taille du segment (1)
		self.send_size(index,serialized_data)

		# Envoi vers le client : Segment (gamestate) (2)
		self.__players[index][SOCKET].send(serialized_data)

		if(DEBUG):
			print("GAMESTATE (envoyé)")

	def send_size(self, index, segment):

		data = ""
		serialized_data = None

		# Calcul de la taille du segment à envoyer passé en paramètre
		data = '%16s' %len(segment)

		# Sérialisation
		serialized_data = data.encode()

		# Envoi vers le client : Taille du segment
		self.__players[index][SOCKET].send(serialized_data)

		if(DEBUG):
			print(int(data),"BYTES (envoyé)")

	def recv_action(self, index):
		
		size = 0
		serialized_data = None
		data = None

		# Réception depuis le client : Taille du segment (1)
		size = self.recv_size(index)

		# Réception depuis le client : Segment (action) (2)
		serialized_data = self.__players[index][SOCKET].recv(size)

		# Désérialisation
		data = pickle.loads(serialized_data)

		if(DEBUG):
			print(data,"(reçu)")
		
		return data

	def recv_size(self,index):

		data = 0
		serialized_data = None

		# Réception depuis le client : Taille du segment
		serialized_data = self.__players[index][SOCKET].recv(16)

		# Désérialisation
		data = int(serialized_data.decode())

		if(DEBUG):
			print(data,"BYTES (reçu)")

		return data

	def wait_client(self):

		i = 1

		# Mise en écoute de la socket TCP
		self.__socket.listen(self.__slots)

		# Connexions des joueurs
		while not self.is_full():
			
			self.__players.append([self.__socket.accept()[0],None])

			self.__log.write(f"Connexion du Joueur {i}")

			i += 1

	def choose_deck(self):

		player_id = 0
		deck = None

		for player in self.__players:
	
			# Création automatique du deck sans demander au client
			self.__deckmanager.add(DEFAULT_DECK)
			deck = self.__deckmanager.copy_deck(0)

			# Création de l'objet Player en lui passant le deck
			player[PLAYER] = Player(player_id,PLAYER_LIFE,deck)

			# Incrémentation du compteur définissant l'identifiant du joueur
			player_id += 1

			self.__log.write(f"Joueur {player[PLAYER].get_id()+1} a choisi le deck {DEFAULT_DECK}")

	def start(self):

		gamestate = None

		# Initialisation de la partie
		for player in self.__players:

			# Envoi vers le player : ID Player (1)
			self.send_signal(player[PLAYER].get_id(),str(player[PLAYER].get_id()))

			# Envoi vers le player : Liste de Players (2)
			gamestate = self.choose_gamestate("INIT")

			self.send_gamestate(player[PLAYER].get_id(),gamestate)

		# Phase Mulligan
		for player in self.__players:		
		
			# Exécution de la phase
			self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}] Phase Mulligan")
			self.mulligan(player[PLAYER].get_id())

	def mulligan(self, index):

		data = None
		mulligan_count = 0
		gamestate = None

		# Mélange initial du deck
		self.__players[index][PLAYER].get_board().get_deck().shuffle()

		# Pioche 7 cartes
		self.__players[index][PLAYER].draw_card(7)

		# Envoi vers le player : Etat de la partie initiale
		self.send_signal(index,"GAME_UPDATE")
		gamestate = self.choose_gamestate([[index,"HAND","DECK"]])
		self.send_gamestate(index,gamestate)

		while True:

			# Envoi vers le player : Signal de jeu (3)
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action (4)
			data = self.recv_action(index)

			# Continuer à mulligan ?
			if( (data.get("type") == "MULLIGAN") and (mulligan_count < 7) ):

				# Envoi vers le client : Acceptation (5.1.1)
				self.send_signal(index,"ACCEPT")

				# Défausse de la main
				self.__players[index][PLAYER].get_board().empty_hand()
				
				# Mélange du deck
				self.__players[index][PLAYER].get_board().get_deck().shuffle()

				mulligan_count += 1

				# Pioche (7-n) cartes
				self.__players[index][PLAYER].draw_card(7 - mulligan_count)

				# Envoi vers le client : Etat de la partie (5.1.2)
				gamestate = self.choose_gamestate([[index,"DECK","HAND"]])
				self.send_gamestate(index,gamestate)

				self.__log.write(f"Joueur {index+1} veut continuer le mulligan")
			
			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (5.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (5.2.2)
				gamestate = self.choose_gamestate([[index,"DECK","HAND"]])
				self.send_gamestate(index,gamestate)

				self.__log.write(f"Joueur {index+1} a terminé le mulligan")

				break
			
			elif(data.get("type") == "CONCEDE"):

				# Envoi vers le client : Fin de partie (5.3)
				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus (5.4)
				self.send_signal(index,"DECLINE")

				self.__log.write(f"Joueur {index+1} dit n'importe quoi")

				continue

	def turn(self): 

		data = None
		land_played = False

		while self.players_alive() > 1:

			for player in self.__players:

				self.__log.write(f"Tour du joueur {player[PLAYER].get_id()+1}")

				# Permission de poser un terrain
				land_played = False

				# Vérification si le joueur est encore en vie
				if (self.players_alive() > 1) and (player[PLAYER].get_life() > 0):

					self.__log.write(f"Le joueur {player[PLAYER].get_id()+1} est en vie ({player[PLAYER].get_life()}HP)")

					# Phase de départ
					self.start_phase(player[PLAYER].get_id())

					# # Phase Effet 1
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 1")
					# self.effect_phase(player[PLAYER].get_id())

					# # Phase Ephémère 1
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Ephémères 1")
					# self.instant_phase(player[PLAYER].get_id())

					# Phase de pioche
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}] Phase de pioche")
					self.draw_phase(player[PLAYER].get_id())

					# # Phase Effet 2
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 2")
					# for ennemy in self.__players:

					# 	if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

					# 		print("L'ennemi", ennemy[PLAYER].get_id()+1, "peut activer un effet")

					# 		# Phase Effet 2 par ennemy
					# 		self.effect_phase(ennemy[PLAYER].get_id())

					# Phase Principale
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}] Phase principale (1)")
					land_played = self.main_phase(player[PLAYER].get_id(),land_played)

					# Phase d'Attaque (Déclaration des monstres attaquants)
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}] Phase d'attaque")
					self.attack_phase(player[PLAYER].get_id())
					
					# # Phase Éphémère 2
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Éphémères 2")
					# for ennemy in self.__players:

					# 	if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

					# 		print("L'ennemi", ennemy[PLAYER].get_id()+1, "peut activer un effet")

					# 		# Phase Éphémère 2 par ennemy
					# 		self.instant_phase(ennemy[PLAYER].get_id())

					# Phase Blocage (Ennemi déclare les monstres bloquants)
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}]  Phase de blocage")
					for ennemy in self.__players:

						if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

							self.__log.write(f"Joueur {ennemy[PLAYER].get_id()+1} peut bloquer les cartes du Joueur {player[PLAYER].get_id()+1}")

							# Phase de blocage par ennemy
							self.block_phase(ennemy[PLAYER].get_id())

					# # Phase Effet 3
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 3")
					# self.effect_phase(player[PLAYER].get_id())

					# # Phase Ephémère 3
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Ephémères 3")
					# self.instant_phase(player[PLAYER].get_id())

			 		# Phase Dommages (Appliquer les dommages de combat (prévenir du décès avec une requête))
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}]  Résolution des dégats")
					self.damage_phase(player[PLAYER].get_id())
					
					# Phase Secondaire
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}]  Phase principale (2)")
					land_played = self.main_phase(player[PLAYER].get_id(),land_played)

					# Phase de fin
					self.__log.write(f"[JOUEUR {player[PLAYER].get_id()+1}]  Phase de fin")
					self.end_phase(player[PLAYER].get_id())

		# Envoi des résultats
		for player in self.__players:

			if(player[PLAYER].get_life() > 0):
				
				# Envoi vers le client : Signal de victoire
				self.send_signal(player[PLAYER].get_id(),"VICTORY")

				self.__log.write(f"Joueur {player[PLAYER].get_id()+1} a remporté la partie")

			elif player[PLAYER].get_id() not in self.__dead_players:
				
				# Mise à mort du joueur
				self.kill_player(player[PLAYER].get_id())

	def start_phase(self,index):

		gamestate = None

		# Envoi vers le client : Signal d'update
		self.send_signal(index,"GAME_UPDATE")

		# Dégagement des cartes
		self.__players[index][PLAYER].disengage()

		# Envoi vers le client : Etat de la partie
		gamestate = self.choose_gamestate([[index,"MANA","BATTLE_ZONE","LAND_ZONE"]])
		self.send_gamestate(index,gamestate)

		self.__log.write(f"Dégagement des cartes du Joueur {index+1}")

	# def effect_phase(self, index):

	# 	data = None
	# 	gamestate = None

	# 	while True:

	# 		# Envoi vers le client : Signal de jeu (5)
	# 		self.send_signal(index,"PLAY")

	# 		# Réception depuis le client : Requête d'action (6)
	# 		data = self.recv_action(index)

	# 		if(data.get("type") == "USE_EFFECT"):

	# 			# Envoi vers le client : Acceptation (7.1.1)
	# 			self.send_signal(index,"ACCEPT")

	# 			# TODO : Activation des effets

	# 			# Envoi vers le client : Etat de la partie (7.1.2)
	# 			gamestate = self.choose_gamestate("ALL")
	# 			self.send_gamestate(index,gamestate)

	# 			break

	# 		elif(data.get("type") == "SKIP_PHASE"):

	# 			# Envoi vers le client : Acceptation (7.2.1)
	# 			self.send_signal(index,"ACCEPT")

	# 			# Envoi vers le client : Etat de la partie (7.2.2)
	# 			gamestate = self.choose_gamestate("EMPTY")
	# 			self.send_gamestate(index,gamestate)

	# 			break
			
	# 		elif(data.get("type") == "CONCEDE"):

	# 			self.concede(index)

	# 			break

	# 		else:

	# 			# Envoi vers le client : Refus (7.3)
	# 			self.send_signal(index,"DECLINE")

	# def instant_phase(self, index):

	# 	data = None
	# 	gamestate = None

	# 	while True:

	# 		# Envoi vers le client : Signal de jeu (8)
	# 		self.send_signal(index,"PLAY")

	# 		# Réception depuis le client : Requête d'action (9)
	# 		data = self.recv_action(index)

	# 		if(data.get("type") == "INSTANT"):

	# 			# Envoi vers le client : Acceptation (10.1.1)
	# 			self.send_signal(index,"ACCEPT")

	# 			# TODO : Activation des ephémères

	# 			# Envoi vers le client : Etat de la partie (10.1.2)
	# 			gamestate = self.choose_gamestate("ALL")
	# 			self.send_gamestate(index,gamestate)

	# 			break

	# 		elif(data.get("type") == "SKIP_PHASE"):

	# 			# Envoi vers le client : Acceptation (10.2.1)
	# 			self.send_signal(index,"ACCEPT")

	# 			# Envoi vers le client : Etat de la partie (10.2.2)
	# 			gamestate = self.choose_gamestate("EMPTY")
	# 			self.send_gamestate(index,gamestate)

	# 			break
			
	# 		elif(data.get("type") == "CONCEDE"):

	# 			self.concede(index)

	# 			break

	# 		else:

	# 			# Envoi vers le client : Refus (10.3)
	# 			self.send_signal(index,"DECLINE")

	def draw_phase(self, index):

		data = None
		gamestate = None

		while True:

			# Envoi vers le client : Signal de jeu (11)
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action (12)
			data = self.recv_action(index)

			if(data.get("type") == "DRAW_CARD"):

				# Envoi vers le client : Acceptation (13.1.1)
				self.send_signal(index,"ACCEPT")

				# Pioche
				self.__players[index][PLAYER].draw_card(1)

				# Envoi vers le client : Etat de la partie (13.1.2)
				gamestate = self.choose_gamestate([[index,"DECK","HAND"]])
				self.send_gamestate(index,gamestate)

				self.__log.write(f"Joueur {index+1} se décide à piocher")

				break
			
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus (13.2)
				self.send_signal(index,"DECLINE")

				self.__log.write(f"Joueur {index+1} dit n'importe quoi")

	def main_phase(self, index, land_played):

		data = None
		gamestate = None
		is_accepted = False
		card = None
		card_name = ""

		while True:

			# Envoi vers le client : Signal de jeu
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action
			data = self.recv_action(index)

			if(data.get("type") == "PLAY_CARD"):

				# Engagement des cartes
				is_accepted,land_played = self.__players[index][PLAYER].engage(data["hand_position"],land_played,self.__log)

				if(is_accepted):

					# Récupération de la carte
					card = self.__players[index][PLAYER].get_board().get_hand()[data["hand_position"]]

					# Envoi vers le client : Acceptation
					self.send_signal(index,"ACCEPT")

					# Envoi vers le client : Etat de la partie
					gamestate = self.choose_gamestate("EMPTY")
					self.send_gamestate(index,gamestate)

					# Vérification que la carte possède un effet
					if(len(card.get_effect()) > 0):

						self.__log.write(f"Joueur {index+1} doit sélectionner des cibles pour les effets de cette carte")

						is_accepted = self.use_effect(index,"HAND",data["hand_position"],"play")

					if(is_accepted):

						# Mise à jour du mana du joueur
						self.__players[index][PLAYER].consume_mana(card.get_mana_cost(),self.__log)

						# Récupération du nom de la carte
						card_name = card.get_name()

						# Déplacement de la carte
						if(card.get_type() == "Land"):

							# Invocation sur le terrain	
							is_accepted = self.__players[index][PLAYER].move("HAND",data["hand_position"],"LAND_ZONE")

							if(is_accepted):

								self.__log.write(f"Joueur {index+1} pose le terrain {card_name}")	
								
						elif(card.get_type() == "Creature"):

							# Invocation sur le terrain	
							is_accepted = self.__players[index][PLAYER].move("HAND",data["hand_position"],"BATTLE_ZONE")

							if(is_accepted):

								self.__log.write(f"Joueur {index+1} pose {card_name} sur le champ de bataille")	

						elif(card.get_type() in ["Artifact","Enchantment","Instant","Sorcery"]):

							# Envoi au cimetière
							is_accepted = self.__players[index][PLAYER].move("HAND",data["hand_position"],"GRAVEYARD")

					if(is_accepted):

						# Envoi vers le client : Acceptation
						self.send_signal(index,"ACCEPT")

						# Envoi vers le client : Etat de la partie
						gamestate = self.choose_gamestate("ALL")
						self.send_gamestate(index,gamestate)

					else:

						# Envoi vers le client : Refus
						self.send_signal(index,"DECLINE")	

						self.__log.write(f"Joueur {index+1} n'a pas rempli les conditions pour engager {card.get_name()}")													

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

					self.__log.write(f"Joueur {index+1} n'a pas assez de mana pour cette carte")

			elif(data.get("type") == "TAP_LAND"):

				# Tap un terrain
				is_accepted = self.__players[index][PLAYER].tap_land(data["landzone_position"],data["color"])

				if(is_accepted):

					# Envoi vers le client : Acceptation
					self.send_signal(index,"ACCEPT")

					# Envoi vers le client : Etat de la partie
					gamestate = self.choose_gamestate([[index,"MANA","LAND_ZONE"]])
					self.send_gamestate(index,gamestate)

					self.__log.write(f"Joueur {index+1} tap le terrain {self.__players[index][PLAYER].get_board().get_land_zone()[data['landzone_position']].get_name()}")

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

					self.__log.write(f"Joueur {index+1} n'a pas le droit de tap {self.__players[index][PLAYER].get_board().get_land_zone()[data['landzone_position']].get_name()} de nouveau")

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				self.__log.write(f"Joueur {index+1} termine la phase")

				break
				
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus
				self.send_signal(index,"DECLINE")

				self.__log.write(f"Joueur {index+1} dit n'importe quoi")

		return land_played
			
	def attack_phase(self, index):

		data = None
		gamestate = None
		is_accepted = False

		while True:

			# Envoi vers le client : Signal de jeu
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action
			data = self.recv_action(index)

			if(data.get("type") == "ATTACK"):

				is_accepted = self.__players[index][PLAYER].attack(data["target"],data["attacker"],len(self.__players))
				
				if(is_accepted):

					# Envoi vers le client : Acceptation
					self.send_signal(index,"ACCEPT")

					self.__log.write(f"Joueur {index+1} déclare attaquer le Joueur {data['target']+1} avec {self.__players[index][PLAYER].get_board().get_battle_zone()[data['attacker']].get_name()}")
					
					gamestate = self.choose_gamestate([[index,"BATTLE_ZONE"]])

					# Envoi vers le client : Etat de la partie
					self.send_gamestate(index,gamestate)

					# Envoi vers tous les autres clients en vie : Etat de la partie
					for player in self.__players :

						if(player[PLAYER].get_id() != index and player[PLAYER].get_life() > 0):

							self.send_signal(player[PLAYER].get_id(),"GAME_UPDATE")
							self.send_gamestate(player[PLAYER].get_id(),gamestate)

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

					self.__log.write(f"Joueur {index+1} n'a pas le droit d'attaquer le Joueur {data['target']+1} avec cette carte")

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				self.__log.write(f"Joueur {index+1} termine la phase")

				break
				
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus
				self.send_signal(index,"DECLINE")

				self.__log.write(f"Joueur {index+1} dit n'importe quoi")

	def block_phase(self, index):

		data = None
		gamestate = None
		is_accepted = False

		while True:

			# Envoi vers le client : Signal de jeu
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action
			data = self.recv_action(index)

			if(data.get("type") == "BLOCK"):

				is_accepted = self.__players[index][PLAYER].block(self.__players[data["target"]][PLAYER],data["ennemy_attacker"],data["blocker"])
				
				if(is_accepted):

					# Envoi vers le client : Acceptation
					self.send_signal(index,"ACCEPT")

					self.__log.write(f"Joueur {index+1} déclare bloquer la carte {self.__players[data['target']][PLAYER].get_board().get_battle_zone()[data['ennemy_attacker']].get_name()} du Joueur {data['target']} avec {self.__players[index][PLAYER].get_board().get_battle_zone()[data['blocker']].get_name()}")

					# Envoi vers le client : Etat de la partie
					gamestate = self.choose_gamestate([[index,"BATTLE_ZONE"]])
					self.send_gamestate(index,gamestate)

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

					self.__log.write(f"Joueur {index+1} n'a pas le droit de bloquer le Joueur {data['target']+1} avec cette carte")

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				self.__log.write(f"Joueur {index+1} termine la phase")

				break
				
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus
				self.send_signal(index,"DECLINE")

				self.__log.write(f"Joueur {index+1} dit n'importe quoi")

	def damage_phase(self, index):

		battlezone_position = 0
		updated = []
		blocked = False
		choice = []
		gamestate = None

		# Stockage du joueur attaquant
		updated.append(index)

		for card in self.__players[index][PLAYER].get_board().get_battle_zone():

			if(card.is_attacking()):

				blocked = False

				# Stockage des joueurs ciblés
				if(card.get_target() not in updated):

					updated.append(card.get_target())

				for ennemy_card in self.__players[card.get_target()][PLAYER].get_board().get_battle_zone():

					if(ennemy_card.get_blocking() == battlezone_position):

						# Application des dommages mutuels
						ennemy_card.damage(card.power())
						card.damage(ennemy_card.power())

						self.__log.write(f"La carte {card.get_name()}(J{index+1}) inflige {card.power()} dommage(s) à {ennemy_card.get_name()}(J{card.get_target()+1})")
						self.__log.write(f"La carte {ennemy_card.get_name()}(J{card.get_target()+1}) inflige {ennemy_card.power()} dommage(s) à {card.get_name()}(J{index+1})")

						blocked = True

				if(not blocked):

					# Application des dommages direct
					self.__players[card.get_target()][PLAYER].damage(card.power())

					self.__log.write(f"Joueur {index+1} inflige {card.power()} dommage(s) direct au Joueur {card.get_target()+1}")

			battlezone_position += 1

		# Déplacement au cimetière les cartes anéanties
		for player in self.__players:

			battlezone_position = 0

			for card in player[PLAYER].get_board().get_battle_zone()[:]:

				if(card.toughness() <= 0):

					self.__players[player[PLAYER].get_id()][PLAYER].move("BATTLE_ZONE",battlezone_position,"GRAVEYARD")

					self.__log.write(f"La carte {card.get_name()} a été détruite, elle est envoyée au cimetière")

				else:

					battlezone_position += 1

		# Préparation de l'update de jeu en fonction des joueurs ciblés
		for player_id in updated:

			choice.append([player_id,"LIFE","BATTLE_ZONE","GRAVEYARD"])

		gamestate = self.choose_gamestate(choice)

		# Envoi à tous les clients en vie : Etat de jeu
		for player in self.__players:

			if(player[PLAYER].get_life() > 0):
				
				self.send_signal(player[PLAYER].get_id(),"GAME_UPDATE")
				self.send_gamestate(player[PLAYER].get_id(),gamestate)

	def end_phase(self, index):

		# Vérification si le joueur n'a plus de vie
		if(self.__players[index][PLAYER].get_life() <= 0):

			# Mise à mort du joueur
			self.kill_player(index)

		else:

			# Application des soins
			self.__players[index][PLAYER].cleanup()

			self.__log.write(f"Les créatures du Joueur {index+1} reçoivent des soins")
		



# elif "move" in card.get_effect()[0].get_target():

# 	if "tapped" in card.get_effect()[0].get_target():
	
# 		pass
	
# 		#regarde mes carte creature en tapped
	
# 	card.get_effect()[0].effect(player1,2)

# elif "land" in card.get_effect()[0].get_target():
	
# 	land = None
	
# 	if "tapped" in card.get_effect()[0].get_target():
	
# 		while (b == True or y == -1):
	
# 			y = input("choisi ton index de land tapped")
	
# 			if y.isnumeric():
	
# 				y = int(y)
	
# 				if player1.get_board().get_land_zone()[y].get_tapped() == True:
	
# 					land = player1.get_board().get_land_zone()[y]
# 					b = False
	
# 				elif y == -1:
	
# 					print("Error")
# 					break
	
# 	else:
	
# 		y = input("choisi l'index de la carte land")
	
# 		if y.isnumeric():
	
# 			y = int(y)
# 			land = player1.get_board().get_land_zone()[y]
	
# 	card.get_effect()[0].effect(land)

