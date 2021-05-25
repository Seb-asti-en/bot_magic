import socket, pickle, sys, os
from deckmanager import DeckManager
from player import Player

DEBUG = False

SOCKET = 0
PLAYER = 1
PLAYER_LIFE = 10

DEFAULT_DECK = "Black"

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

class Game:

	def __init__(self, socket, slots = 2):

		self.__socket = socket
		self.__deckmanager = DeckManager()
		self.__slots = slots
		self.__players = []
		self.__dead_players = []

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

			for player_choice in choice: 

				player_state = [player_choice[ID],None,None,None,None,None,None,None,None]	

				player_state[LIFE] = self.__players[player_state[ID]][PLAYER].get_life()
				player_state[MANA] = self.__players[player_state[ID]][PLAYER].get_mana_pool()
				player_state[DECK] = self.__players[player_state[ID]][PLAYER].get_board().get_deck()
				player_state[HAND] = self.__players[player_state[ID]][PLAYER].get_board().get_hand()
				player_state[BATTLE_ZONE] = self.__players[player_state[ID]][PLAYER].get_board().get_battle_zone()
				player_state[LAND_ZONE] = self.__players[player_state[ID]][PLAYER].get_board().get_land_zone()
				player_state[GRAVEYARD] = self.__players[player_state[ID]][PLAYER].get_board().get_graveyard()
				player_state[EXILE] = self.__players[player_state[ID]][PLAYER].get_board().get_exile()

				gamestate.append(player_state)

		elif(choice == "EMPTY"):

			for player_choice in choice: 

				player_state = [player_choice[ID],None,None,None,None,None,None,None,None]

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

	def concede(self, index):

		gamestate = None

		# Envoi vers le client : Acceptation
		self.send_signal(index,"ACCEPT")
		
		# On met la vie du joueur à 0
		self.__players[index][PLAYER].set_life(0)

		# Envoi vers le client : Etat de la partie
		gamestate = self.choose_gamestate([[index,"LIFE"]])
		self.send_gamestate(index,gamestate)
		
		# Mise à mort du joueur
		self.kill_player(index)

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

		# Mise en écoute de la socket TCP
		self.__socket.listen(self.__slots)

		# Connexions des joueurs
		while not self.is_full():
			self.__players.append([self.__socket.accept()[0],None])

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

	def start(self):

		gamestate = None

		# Initialisation de la partie
		for player in self.__players:

			# Envoi vers le player : ID Player (1)
			self.send_signal(player[PLAYER].get_id(),str(player[PLAYER].get_id()))

			# Envoi vers le player : Liste de Players (2)
			gamestate = self.choose_gamestate("INIT")
			print(gamestate)
			self.send_gamestate(player[PLAYER].get_id(),gamestate)

		# Phase Mulligan
		for player in self.__players:

			# Rafraichissement de l'écran
			self.clear_terminal()			
		
			# Exécution de la phase
			print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Mulligan")
			self.mulligan(player[PLAYER].get_id())

	def mulligan(self, index):

		data = None
		mulligan_count = 0
		gamestate = None

		# Mélange initial du deck
		self.__players[index][PLAYER].get_board().get_deck().shuffle()

		# Pioche 7 cartes
		self.__players[index][PLAYER].draw_card(7)

		while True:

			# DEBUG
			self.__players[index][PLAYER].debug_print_hand()

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
			
			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (5.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (5.2.2)
				gamestate = self.choose_gamestate([[index,"DECK","HAND"]])
				self.send_gamestate(index,gamestate)

				break
			
			elif(data.get("type") == "CONCEDE"):

				# Envoi vers le client : Fin de partie (5.3)
				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus (5.4)
				self.send_signal(index,"DECLINE")

				continue

	def turn(self): 

		data = None

		# Rafraichissement de l'écran
		self.clear_terminal()

		while self.players_alive() > 1:

			for player in self.__players:

				print("Tour du joueur", player[PLAYER].get_id()+1)

				# Vérification si le joueur est encore en vie
				if (self.players_alive() > 1) and (player[PLAYER].get_life() > 0):

					print("Le joueur " + str(player[PLAYER].get_id()+1) + " est en vie (" + str(player[PLAYER].get_life()) + "HP)")

					# Phase de départ
					self.start_phase(player[PLAYER].get_id())

					# # Phase Effet 1
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 1")
					# self.effect_phase(player[PLAYER].get_id())

					# # Phase Ephémère 1
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Ephémères 1")
					# self.instant_phase(player[PLAYER].get_id())

					# Phase de pioche
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase de pioche")
					self.draw_phase(player[PLAYER].get_id())

					# # Phase Effet 2
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 2")
					# for ennemy in self.__players:

					# 	if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

					# 		print("L'ennemi", ennemy[PLAYER].get_id()+1, "peut activer un effet")

					# 		# Phase Effet 2 par ennemy
					# 		self.effect_phase(ennemy[PLAYER].get_id())

					# Phase Principale
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase principale (1)")
					self.main_phase(player[PLAYER].get_id())

					# Phase d'Attaque (Déclaration des monstres attaquants)
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase d'attaque")
					self.attack_phase(player[PLAYER].get_id())
					
					# # Phase Éphémère 2
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Éphémères 2")
					# for ennemy in self.__players:

					# 	if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

					# 		print("L'ennemi", ennemy[PLAYER].get_id()+1, "peut activer un effet")

					# 		# Phase Éphémère 2 par ennemy
					# 		self.instant_phase(ennemy[PLAYER].get_id())

					# Phase Blocage (Ennemi déclare les monstres bloquants)
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase de blocage")
					for ennemy in self.__players:

						if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

							print("L'ennemi", ennemy[PLAYER].get_id()+1, "peut bloquer des cartes")

							# Phase de blocage par ennemy
							self.block_phase(ennemy[PLAYER].get_id())

					# # Phase Effet 3
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 3")
					# self.effect_phase(player[PLAYER].get_id())

					# # Phase Ephémère 3
					# print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Ephémères 3")
					# self.instant_phase(player[PLAYER].get_id())

			 		# Phase Dommages (Appliquer les dommages de combat (prévenir du décès avec une requête))
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Résolution des dégats")
					self.damage_phase(player[PLAYER].get_id())
					
					# Phase Secondaire
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase principale (2)")
					self.main_phase(player[PLAYER].get_id())

					# Phase de fin
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase de fin")
					self.end_phase(player[PLAYER].get_id())

		# Envoi des résultats
		for player in self.__players:

			if(player[PLAYER].get_life() > 0):
				
				# Envoi vers le client : Signal de mort (24.1)
				self.send_signal(player[PLAYER].get_id(),"VICTORY")

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

	def effect_phase(self, index):

		data = None
		gamestate = None

		while True:

			# Envoi vers le client : Signal de jeu (5)
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action (6)
			data = self.recv_action(index)

			if(data.get("type") == "USE_EFFECT"):

				# Envoi vers le client : Acceptation (7.1.1)
				self.send_signal(index,"ACCEPT")

				# TODO : Activation des effets

				# Envoi vers le client : Etat de la partie (7.1.2)
				gamestate = self.choose_gamestate("ALL")
				self.send_gamestate(index,gamestate)

				break

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (7.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (7.2.2)
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				break
			
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus (7.3)
				self.send_signal(index,"DECLINE")

	def instant_phase(self, index):

		data = None
		gamestate = None

		while True:

			# Envoi vers le client : Signal de jeu (8)
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action (9)
			data = self.recv_action(index)

			if(data.get("type") == "INSTANT"):

				# Envoi vers le client : Acceptation (10.1.1)
				self.send_signal(index,"ACCEPT")

				# TODO : Activation des ephémères

				# Envoi vers le client : Etat de la partie (10.1.2)
				gamestate = self.choose_gamestate("ALL")
				self.send_gamestate(index,gamestate)

				break

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (10.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (10.2.2)
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				break
			
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus (10.3)
				self.send_signal(index,"DECLINE")

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

				break
			
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus (13.2)
				self.send_signal(index,"DECLINE")

	def main_phase(self, index):

		data = None
		gamestate = None
		is_accepted = False

		while True:

			# Envoi vers le client : Signal de jeu
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action
			data = self.recv_action(index)

			if(data.get("type") == "PLAY_CARD"):

				# Engagement des cartes
				is_accepted = self.__players[index][PLAYER].engage(data["hand_position"])
				
				if(is_accepted):

					# Envoi vers le client : Acceptation
					self.send_signal(index,"ACCEPT")

					# Envoi vers le client : Etat de la partie
					gamestate = self.choose_gamestate([[index,"HAND","MANA","BATTLE_ZONE","LAND_ZONE"]])
					self.send_gamestate(index,gamestate)

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

			elif(data.get("type") == "TAP_LAND"):

				# Tap un terrain
				is_accepted = self.__players[index][PLAYER].tap_land(data["landzone_position"],data["color"])

				if(is_accepted):

					# Envoi vers le client : Acceptation
					self.send_signal(index,"ACCEPT")

					# Envoi vers le client : Etat de la partie
					gamestate = self.choose_gamestate([[index,"MANA","LAND_ZONE"]])
					self.send_gamestate(index,gamestate)

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				break
				
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus
				self.send_signal(index,"DECLINE")
			
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

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				break
				
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus
				self.send_signal(index,"DECLINE")

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

					# Envoi vers le client : Etat de la partie
					gamestate = self.choose_gamestate([[index,"BATTLE_ZONE"]])
					self.send_gamestate(index,gamestate)

				else:

					# Envoi vers le client : Refus
					self.send_signal(index,"DECLINE")

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie
				gamestate = self.choose_gamestate("EMPTY")
				self.send_gamestate(index,gamestate)

				break
				
			elif(data.get("type") == "CONCEDE"):

				self.concede(index)

				break

			else:

				# Envoi vers le client : Refus
				self.send_signal(index,"DECLINE")

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

						blocked = True

				if(not blocked):

					# Application des dommages direct
					self.__players[card.get_target()][PLAYER].damage(card.power())

			battlezone_position += 1

		# Déplacement au cimetière les cartes anéanties
		for player in self.__players:

			battlezone_position = 0

			for card in player[PLAYER].get_board().get_battle_zone()[:]:

				if(card.toughness() <= 0):

					print("Player",player[PLAYER].get_id(),"moved card",battlezone_position,"to graveyard")
					self.__players[player[PLAYER].get_id()][PLAYER].move("BATTLE_ZONE",battlezone_position,"GRAVEYARD")

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

