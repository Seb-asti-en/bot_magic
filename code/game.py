import socket, pickle, sys, os
from deckmanager import DeckManager
from player import Player

DEBUG = False

SOCKET = 0
PLAYER = 1
LIFE = 10

DEFAULT_DECK = "Test_Tristan"

class Game:

	def __init__(self, socket, slots = 3):

		self.__socket = socket
		self.__deckmanager = DeckManager()
		self.__slots = slots
		self.__players = []

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

	# Retourne le nombre de joueurs en vie
	def players_alive(self):

		alive = 0

		for player in self.__players:

			if(player[PLAYER].get_life() > 0): 

				alive += 1

		return alive

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

	# TODO : (à modifier plus tard selon le format JSON)
	def send_gamestate(self, index):

		serialized_data = None

		# Sérialisation 
		serialized_data = pickle.dumps(self.__players[index][PLAYER])

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
			player[PLAYER] = Player(player_id,LIFE,deck)

			# Incrémentation du compteur définissant l'identifiant du joueur
			player_id += 1

	def start(self):

		# Initialisation de la partie
		for player in self.__players:

			# Envoi vers le player : Objet Player (1)
			self.send_gamestate(player[PLAYER].get_id())

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

		# Mélange initial du deck
		self.__players[index][PLAYER].get_board().get_deck().shuffle()

		# Pioche 7 cartes
		self.__players[index][PLAYER].draw_card(7)

		while True:

			# DEBUG
			self.__players[index][PLAYER].debug_print_hand()

			# Envoi vers le player : Signal de jeu (2)
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action (3)
			data = self.recv_action(index)

			# Continuer à mulligan ?
			if( (data.get("type") == "MULLIGAN") and (mulligan_count < 7) ):

				# Envoi vers le client : Acceptation (4.1.1)
				self.send_signal(index,"ACCEPT")

				# Défausse de la main
				self.__players[index][PLAYER].get_board().empty_hand()
				
				# Mélange du deck
				self.__players[index][PLAYER].get_board().get_deck().shuffle()

				# Envoi vers le client : Etat de la partie (4.1.2)
				self.send_gamestate(index)

				mulligan_count += 1

				# Pioche (7-n) cartes
				self.__players[index][PLAYER].draw_card(7 - mulligan_count)
			
			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (4.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (4.2.2)
				self.send_gamestate(index)

				break

			else:

				# Envoi vers le client : Refus (4.3)
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

					# # Dégagement des cartes
					# player[PLAYER].untap()

					# Phase Effet 1
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 1")
					self.effect_phase(player[PLAYER].get_id())

					# Phase Ephémère 1
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Ephémères 1")
					self.instant_phase(player[PLAYER].get_id())

					# Phase de pioche
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase de pioche")
					self.draw_phase(player[PLAYER].get_id())

					# Phase Effet 2
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase Effets 2")
					for ennemy in self.__players:

						if (ennemy[PLAYER].get_id() != player[PLAYER].get_id()) and (ennemy[PLAYER].get_life() > 0):

							print("L'ennemi", ennemy[PLAYER].get_id()+1, "peut activer un effet")

							# Phase Effet 2 par ennemy
							self.effect_phase(ennemy[PLAYER].get_id())

					# Phase Principale
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase principale (1)")
					self.main_phase(player[PLAYER].get_id())

					# Attaque ?

						# Déclaration des monstres attaquants

						# Ennemi engage éphémère (peut boucler)

						# Ennemi déclare les monstres bloquants

				 		# Activation d'une ou plusieurs capacités (peut boucler)

				 		# Engager éphémère (peut boucler)

				 		# Appliquer les dommages de combat (prévenir du décès avec une requête)
					
					# Phase Secondaire
					print("[PLAYER " + str(player[PLAYER].get_id()+1) + "] Phase principale (2)")
					self.main_phase(player[PLAYER].get_id())

				 	# On retire de la vie au joueur
					player[PLAYER].set_life(player[PLAYER].get_life() - 10)

					# On vérifie s'il est en vie
					if(player[PLAYER].get_life() <= 0):

						# Envoi vers le client : Signal de mort (23)
						self.send_signal(player[PLAYER].get_id(),"DEATH")

		# Envoi des résultats
		for player in self.__players:

			if(player[PLAYER].get_life() > 0):
				
				# Envoi vers le client : Signal de mort (24.1)
				self.send_signal(player[PLAYER].get_id(),"VICTORY")

			else:
				
				# Envoi vers le client : Signal de mort (24.2)
				self.send_signal(player[PLAYER].get_id(),"DEATH")

	def effect_phase(self, index):

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
				self.send_gamestate(index)

				break

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (7.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (7.2.2)
				self.send_gamestate(index)

				break

			else:

				# Envoi vers le client : Refus (7.3)
				self.send_signal(index,"DECLINE")

	def instant_phase(self, index):

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
				self.send_gamestate(index)

				break

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (10.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (10.2.2)
				self.send_gamestate(index)

				break

			else:

				# Envoi vers le client : Refus (10.3)
				self.send_signal(index,"DECLINE")

	def draw_phase(self, index):

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
				self.send_gamestate(index)

				break

			else:

				# Envoi vers le client : Refus (13.2)
				self.send_signal(index,"DECLINE")

	def main_phase(self, index):

		while True:

			# Envoi vers le client : Signal de jeu (17)
			self.send_signal(index,"PLAY")

			# Réception depuis le client : Requête d'action (18)
			data = self.recv_action(index)

			if(data.get("type") == "PLAY_CARD"):

				# Envoi vers le client : Acceptation (19.1.1)
				self.send_signal(index,"ACCEPT")

				# TODO : Engagement des cartes

				# Envoi vers le client : Etat de la partie (19.1.2)
				self.send_gamestate(index)

				break

			elif(data.get("type") == "SKIP_PHASE"):

				# Envoi vers le client : Acceptation (19.2.1)
				self.send_signal(index,"ACCEPT")

				# Envoi vers le client : Etat de la partie (19.2.2)
				self.send_gamestate(index)

				break

			else:

				# Envoi vers le client : Refus (19.3)
				self.send_signal(index,"DECLINE")
