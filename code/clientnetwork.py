#!/usr/bin/env python3

import socket, pickle
from card import Card
from network import Network

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000         # The port used by the server

def main():
	network = Network(HOST, PORT)
	network.connect()

	card = Card()
	network.send(card)

	print ('Data Sent to Server')

	data = network.recv(4096)
	rcard = pickle.loads(data)
	print('Received', rcard.get_name())

if __name__ == "__main__":
	main()