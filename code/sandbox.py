from game import Game
from player import Player

NOIR = '\x1b[6;37;40m'
ROUGE = '\x1b[6;30;41m'
ORANGE = '\x1b[6;30;43m'
BLEU = '\x1b[6;30;44m'
BLANC = '\x1b[6;30;47m'
RESET = '\x1b[0m'

DECK1 = "White"
DECK2 = "Black"
DECKTEST = "Test_Tristan"

def main():

	game = None
	deckmanager = None
	player1 = None
	player2 = None

	# Création d'un objet Game
	game = Game("NO_SOCKET")

	# Récupération du DeckManager au sein de Game 
	deckmanager = game.get_deckmanager()

	# Ajout de deux decks (tu peux mettre ce que tu veux bâtard)
	deckmanager.add(DECKTEST)
	deckmanager.add(DECKTEST)

	# Création des joueurs (à ta sauce aussi, c'est qu'un exemple)
	player1 = Player(1,20,deckmanager.copy_deck(0))
	player2 = Player(2,20,deckmanager.copy_deck(1))

	#pioche
	player1.draw_card(7)
	player2.draw_card(7)

	b = False
	debug_print_all(player1,player2)
	while(b == False):
		index = int(input("saisir un index pour jouer une carte : "))
		b = player1.play_card(index)
	
	b = False
	while(b == False):
		index = int(input("saisir un index pour jouer une carte : "))
		b = player2.play_card(index)
	
	debug_print_all(player1,player2)

	b = False
	debug_print_all(player1,player2)
	while(b == False):
		index = int(input("saisir un index pour jouer une carte : "))
		b = player1.play_card(index)
	
	b = False
	while(b == False):
		index = int(input("saisir un index pour jouer une carte : "))
		b = player2.play_card(index)
	
	debug_print_all(player1,player2)

	#attaque du joueur1
	index = int(input("player 1: saisir l'index de l'attaque : "))
	print("La carte qui attaque : ",player1.get_board().get_battle_zone()[index].get_name())
	player1.choice_attack(index)
	debug_print_all(player1,player2)

	#blockage du joueur2
	index_block = int(input("player 2 : saisir l'index du blockeur : "))
	print("La carte qui block : ",player2.get_board().get_battle_zone()[index_block].get_name())
	index_attk = int(input("player 2: saisir l'index de l'attaqueur : "))
	print("La carte qui attaque : ",player1.get_board().get_battle_zone()[index_attk].get_name())
	player2.choice_block(player1, index_block, index_attk)
	debug_print_all(player1,player2)

	#attaque
	player1.attack(player2, index_attk, index_block)
	debug_print_all(player1,player2)

	#attribution damage
	killing(player1,player2)
	print("BLESSURE")
	#affichage
	debug_print_all(player1,player2)

	#soin
	recovery(player1, player2)

	print("RECOVERY")

	#affichage
	debug_print_all(player1,player2)

	player1.untap()
	player2.untap()
	debug_print_all(player1,player2)


def debug_print_all(player1,player2):
	print("___________________________________________________________________________________________")
	print("|",len(player2.get_board().get_graveyard()),"|","      ","|",player2.get_life(),"|","      ","|",len(player2.get_board().get_deck().get_cards()),"|")
	print("graveyard","    ","vie","       ","deck")
	print("")
	
	player2.debug_print_hand()
	print("|",len(player2.get_board().get_land_zone()),"|")
	print("land_zone")
	print("")
	
	#battlezone j2
	i=0
	for card in player2.get_board().get_battle_zone():
		if player2.get_board().get_battle_zone()[i].get_istarget() == True:
			print('|'+ORANGE,card._name,RESET+'|,"[",card.get_mana_cost(),"]"',end='  ')	
		elif player2.get_board().get_battle_zone()[i].get_isattack() == True:
			print('|'+ROUGE,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')
		elif player2.get_board().get_battle_zone()[i].get_isblocked() == True:
			print('|'+BLEU,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')
		elif player2.get_board().get_battle_zone()[i]._issummoning_sickness == True:	
			print('|'+NOIR,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')
		else:
			print("|",card._name,"[",card.get_mana_cost(),"]","|",end='  ')
		print("")	
		print("|",card.get_effect().get_list_effects(),"|")
		print("|",card.get_damage(),",",card.get_life(),"|")
		i+=1

	print("")
	print("          battle_zone")
	print("")

	#battlezone j1
	i=0
	for card in player1.get_board().get_battle_zone():
		if player1.get_board().get_battle_zone()[i].get_istarget() == True:
			print('|'+ORANGE,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')		
		elif player1.get_board().get_battle_zone()[i].get_isattack() == True:
			print('|'+ROUGE,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')
		elif player1.get_board().get_battle_zone()[i].get_isblocked() == True:
			print('|'+BLEU,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')
		elif player1.get_board().get_battle_zone()[i]._issummoning_sickness == True:	
			print('|'+NOIR,card._name,RESET+'|',"[",card.get_mana_cost(),"]",end='  ')
		else:
			print("|",card._name,"[",card.get_mana_cost(),"]","|",end='  ')
		print("")
		print("|",card.get_effect().get_list_effects(),"|")
		print("|",card.get_damage(),",",card.get_life(),"|")
		i= i+1
		
	
	print("")
	print("land_zone")
	player1.debug_print_land_zone()
	print("")

	player1.debug_print_hand()

	print("graveyard","    ","vie","       ","deck")
	print("|",len(player1.get_board().get_graveyard()),"|","      ","|",player1.get_life(),"|","      ","|",len(player1.get_board().get_deck().get_cards()),"|")
	print("__________________________________________________________________________________________")



##
#soigne les blessures des creatures 
# @param player1 le joueur1
# @param player2 le joueur2 
##
def recovery(player1,player2):
	for card in player1.get_board().get_battle_zone():
		card.set_life(card.get_tmp_life())
		card.set_damage(card.get_tmp_damage())
		card._isattack = False
		card._istarget = False
		card._isblocked = False
	for card in player2.get_board().get_battle_zone():
		card.set_life(card.get_tmp_life())
		card.set_damage(card.get_tmp_damage())
		card._isattack = False
		card._istarget = False
		card._isblocked = False				
	
##
# tue les cartes qui on plus de vie 
# @param player1 le joueur1
# @param player2 le joueur2
##
def killing(player1,player2):
	i=0
	for card in player1.get_board().get_battle_zone():
		if card.get_life() <= 0 :
			player1.to_graveyard("BATTLE_ZONE", i)
		else:
			i+=1

	i=0
	for card in player2.get_board().get_battle_zone():
		if card.get_life() <= 0:
			player2.to_graveyard("BATTLE_ZONE", i)
		else:
			i+=1
