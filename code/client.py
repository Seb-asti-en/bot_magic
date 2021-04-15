#!/usr/bin/env python3

import socket, pickle
from card import Card

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
		socket_client.connect((HOST, PORT))

		card = Card()
		data_string = pickle.dumps(card)
		socket_client.send(data_string)

		print ('Data Sent to Server')

		data = socket_client.recv(4096)
		fff = pickle.loads(data).get_name()
		print('Received', fff)

		socket_client.close()

if __name__ == "__main__":
	main()

