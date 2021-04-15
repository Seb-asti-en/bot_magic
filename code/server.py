#!/usr/bin/env python3

import socket, pickle, sys
from card import Card

def main():
	if len(sys.argv) != 3:
		print("Usage : %s hostServer portServer" % sys.argv[0])
		print("Où :")
		print("  hostServer : adresse IPv4 du serveur")
		print("  portServer : numéro de port d'écoute du serveur")
		sys.exit(-1)

	host = str(sys.argv[1])
	
	port = int(sys.argv[2])

	if port < 1024:
		print("Port invalide")
		sys.exit(-1)

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
		socket_server.bind((host, port))
		socket_server.listen(5)
		conn, address = socket_server.accept()
		
		with conn:
			print('Connected by', address)
			
			while True:
				data = conn.recv(4096)
				if not data:
					break
				data_variable = pickle.loads(data)
				print(data_variable)
				conn.send(data)
					
			conn.close()
			
		socket_server.close()

		print('Data received from client')

if __name__ == "__main__":
	main()