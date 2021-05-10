from game import Game
from player import Player

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
	deckmanager.add("White")
	deckmanager.add("Black")

	# Création des joueurs (à ta sauce aussi, c'est qu'un exemple)
	player1 = Player(1,20,deckmanager.copy_deck(0))
	player2 = Player(2,20,deckmanager.copy_deck(1))

	# Tout ton code (ici tu mets tout ton exécution principale)
	print("Hello World !")

# Et là après tu peux ajouter d'autres fonctions
