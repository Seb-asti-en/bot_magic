from client import Client

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
	client.get_result(result)

	# Déconnexion du serveur
	client.disconnect()

	# Nettoyage en sortie
	client.clear_terminal()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)
