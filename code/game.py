import socket, pickle, sys, os
from player import Player
from deckmanager import DeckManager

SOCKET = 0
PLAYER = 1
LIFE = 20
SEGMENT_SIZE = 65536

BLEU = '\x1b[6;30;44m'
ROUGE = '\x1b[6;30;41m'
ORANGE = '\x1b[6;30;43m'
RESET = '\x1b[0m'

DECK1 = "White"
DECK2 = "Black"
DECKTEST = "Test_Tristan"

class Game:

	#constructeur
	def __init__(self, socket, slots = 2):
		self.__socket = socket
		self.__deckmanager = DeckManager()
		self.__slots = slots
		self.__players = []

	#Getters
	def get_socket(self):
		return self.__socket
	
	#Methodes
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
			self.__deckmanager.add(DECKTEST)
			deck = self.__deckmanager.copy_deck(0)

			# Création de l'objet Player en lui passant le deck
			player[PLAYER] = Player(player_id,LIFE,deck)

			# Incrémentation du compteur définissant l'identifiant du joueur
			player_id += 1

	def start(self):

		data = None
		serialized_data = None


		self.test()

		# # Initialisation de la partie
		# for player in self.__players:

		# 	# Sérialisation
		# 	serialized_data = pickle.dumps(player[PLAYER])

		# 	# Envoi vers le player : Objet Player (1)
		# 	player[SOCKET].send(serialized_data)

		# # Phase Mulligan
		# for player in self.__players:

		# 	# Réponse
		# 	data = "PHASE_START"

		# 	# Rafraichissement de l'écran
		# 	self.clear_terminal()			

		# 	# Sérialisation
		# 	serialized_data = pickle.dumps(data)

		# 	# Envoi vers le player : Démarrage de la phase (2)
		# 	player[SOCKET].send(serialized_data)
		
		# 	# Exécution de la phase
		# 	self.mulligan(player[PLAYER].get_id())

	def turn(self): 

		return

		data = None
		serialized_data = None

		while self.players_alive() > 1:

			for player in self.__players:

				# Vérification si le joueur est encore en vie
				if player[PLAYER].get_life() > 0:

					# # Dégagement des cartes
					# player[PLAYER].untap()

					# Réception depuis le client : Requête d'action (3)
					serialized_data = player[SOCKET].recv(SEGMENT_SIZE)

					# Désérialisation
					data = pickle.loads(serialized_data)

					if(data.get("type") == "USE_EFFECT"):

						# Activation d'une ou plusieurs capacités (peut boucler)
						self.effect_phase(player[PLAYER].get_id(),data)

						serialized_data = player[SOCKET].recv(SEGMENT_SIZE)

						# Désérialisation
						data = pickle.loads(serialized_data)

					if(data.get("type") == "INSTANT"):

						# Engager éphémère (peut boucler)
						self.instant_phase(player[PLAYER].get_id(),data)

						serialized_data = player[SOCKET].recv(SEGMENT_SIZE)

						# Désérialisation
						data = pickle.loads(serialized_data)

					# Pioche
					self.draw_phase(player[PLAYER].get_id(),data)

					# Ennemi activation d'une ou plusieurs capacités (peut boucler)
					for ennemy in self.__players:

						if(ennemy[PLAYER].get_id() != player[PLAYER].get_id()):

							serialized_data = ennemy[SOCKET].recv(SEGMENT_SIZE)

							# Désérialisation
							data = pickle.loads(serialized_data)

							self.effect_phase(ennemy[PLAYER].get_id(),data)

					# Jouer monstres ou terrain ou éphémère (peut boucler si éphémère) (1 terrain max par tour)
					self.main_phase(player[PLAYER].get_id(),data)

					# Attaque ?

						# Déclaration des monstres attaquants

						# Ennemi engage éphémère (peut boucler)

						# Ennemi déclare les monstres bloquants

				 		# Activation d'une ou plusieurs capacités (peut boucler)

				 		# Engager éphémère (peut boucler)

				 		# Appliquer les dommages de combat

				 	# Jouer monstres ou terrain ou éphémère (peut boucler si éphémère) (1 terrain max par tour)

	def mulligan(self, index):

		mulligan_count = 0
		data = None
		serialized_data = None
		response = ""

		# Mélange initial du deck
		self.__players[index][PLAYER].get_board().get_deck().shuffle()

		# Pioche 7 cartes
		self.__players[index][PLAYER].draw_card(7)

		while True:

			# DEBUG
			self.__players[index][PLAYER].debug_print_hand()

			# Réception depuis le client : Requête d'action (3)
			serialized_data = self.__players[index][SOCKET].recv(SEGMENT_SIZE)

			# Désérialisation
			data = pickle.loads(serialized_data)

			# Continuer à mulligan ?
			if( (data.get("type") == "MULLIGAN") and (mulligan_count < 7) ):

				# Réponse
				response = "ACCEPT"

				# Sérialisation
				serialized_data = pickle.dumps(response)

				# Envoi vers le client : Acceptation (4)
				self.__players[index][SOCKET].send(serialized_data)

				# Défausse de la main
				self.__players[index][PLAYER].get_board().empty_hand()
				
				# Mélange du deck
				self.__players[index][PLAYER].get_board().get_deck().shuffle()

				# Sérialisation 
				# TODO : (à modifier plus tard selon le format JSON)
				serialized_data = pickle.dumps(self.__players[index][PLAYER])

				# Envoi vers le client : Etat de la partie (5)
				self.__players[index][SOCKET].send(serialized_data)

				mulligan_count += 1

				# Pioche (7-n) cartes
				self.__players[index][PLAYER].draw_card(7 - mulligan_count)
			
			elif(data.get("type") == "SKIP_PHASE"):

				# Réponse
				response = "ACCEPT"

				# Sérialisation
				serialized_data = pickle.dumps(response)

				# Envoi vers le client : Acceptation (4)
				self.__players[index][SOCKET].send(serialized_data)

				# Sérialisation 
				# TODO : (à modifier plus tard selon le format JSON)
				serialized_data = pickle.dumps(self.__players[index][PLAYER])

				# Envoi vers le client : Etat de la partie (5)
				self.__players[index][SOCKET].send(serialized_data)

				break

			else:

				# Réponse
				response = "DECLINE"

				# Sérialisation
				serialized_data = pickle.dumps(response)

				# Envoi vers le client : Refus (4)
				self.__players[index][SOCKET].send(serialized_data)

				continue

	def effect_phase(self, index, request):
		pass

	def instant_phase(self, index, request):
		pass

	def draw_phase(self, index, request):
		pass

	def main_phase(self, index, request):
		pass


	def debug_print_all(self,Player1,Player2):
		print("___________________________________________________________________________________________")
		print("|",len(Player2.get_board().get_graveyard()),"|","      ","|",Player2.get_life(),"|","      ","|",len(Player2.get_board().get_deck().get_cards()),"|")
		print("graveyard","    ","vie","       ","deck")
		print("")
		#hand j2
		#	for i in range(len(Player2.get_board().get_hand())):
		#		print("|",i,"|",end='  ')
		Player2.debug_print_hand()
		print("          hand")
		print("")
		print("|",len(Player2.get_board().get_land_zone()),"|")
		print("land_zone")
		print("")
		#battlezone j2
		i=0
		for card in Player2.get_board().get_battle_zone():
			if Player2.get_board().get_battle_zone()[i].get_istarget() == True:
				print('|'+ORANGE,card._name,RESET+'|',end='  ')	
			elif Player2.get_board().get_battle_zone()[i].get_isattack() == True:
				print('|'+ROUGE,card._name,RESET+'|',end='  ')
			elif Player2.get_board().get_battle_zone()[i].get_isblocked() == True:
				print('|'+BLEU,card._name,RESET+'|',end='  ')
			else:
				print("|",card._name,"|",end='  ')
			print("")	
			print("|",card.get_damage(),",",card.get_life(),"|")
			i+=1
		print("")
		print("          battle_zone")
		#battlezone j1
		i=0
		for card in Player1.get_board().get_battle_zone():
			if Player1.get_board().get_battle_zone()[i].get_istarget() == True:
				print('|'+ORANGE,card._name,RESET+'|',end='  ')		
			elif Player1.get_board().get_battle_zone()[i].get_isattack() == True:
				print('|'+ROUGE,card._name,RESET+'|',end='  ')
			elif Player1.get_board().get_battle_zone()[i].get_isblocked() == True:
				print('|'+BLEU,card._name,RESET+'|',end='  ')
			else:
				print("|",card._name,"|",end='  ')
			print("")
			print("|",card.get_damage(),",",card.get_life(),"|")
			i= i+1
			
		print("")
		print("")
		print("land_zone")
		print("|",len(Player1.get_board().get_land_zone()),"|")
		print("")
		#hand j1
		print("          hand")


		#	for i in range(len(Player1.get_board().get_hand())):
		#		print("|",i,"|",end='  ')
		Player1.debug_print_hand()

		print("")

		print("")
		print("graveyard","    ","vie","       ","deck")
		print("|",len(Player1.get_board().get_graveyard()),"|","      ","|",Player1.get_life(),"|","      ","|",len(Player1.get_board().get_deck().get_cards()),"|")
		print("__________________________________________________________________________________________")




	def recovery(self,Player1,Player2):
		pass

	##
	# tue les cartes qui on plus de vie 
	# @param Player1 le joueur1
	# @param Player2 le joueur2
	##
	def killing(self,Player1,Player2):
		i=0
		for card in Player1.get_board().get_battle_zone():
			if card.get_life() <= 0 :
				Player1.to_graveyard("BATTLE_ZONE", i)
			else:
				i+=1

		i=0
		for card in Player2.get_board().get_battle_zone():
			if card.get_life() <= 0 :
				Player2.to_graveyard("BATTLE_ZONE", i)
			else:
				i+=1


	def test(self):
		print('|'+BLEU+'BLEU'+RESET+'|')
		print('|'+ROUGE+'ROUGE'+RESET+'|')

		self.__deckmanager.add(DECK2)
		Player2  = Player(1,20,self.__deckmanager.copy_deck(0))
		Player1  = Player(2,20,self.__deckmanager.copy_deck(0))

		#pioche
		Player1.draw_card(9)
		Player2.draw_card(9)
		self.debug_print_all(Player1,Player2)

	
			#clear la carte avant de faire le graveyard

		#jouer
		Player1.play_card(6)
		Player1.play_card(1)
		Player1.play_card(6)
		
		Player2.play_card(1)
		Player2.play_card(5)

	#	Player2.choice_attack(0)
	#	Player1.choice_block(Player2,0,1)

	#	Player1.defense(Player2, 0, 1)
	#	self.killing(Player1,Player2)

		#afterblessing

		#	Player2.to_graveyard("BATTLE_ZONE", 0)
		#	self.debug_print_all(self.__players[0][PLAYER])
		
		#	print("attack")
		#	print(Player1.get_board().get_battle_zone()[0]._isattack)
		#	print("block")
		#	print(Player1.get_board().get_battle_zone()[0]._isblocked)
		
		#	Player2.block(0)
		self.debug_print_all(Player1,Player2)




