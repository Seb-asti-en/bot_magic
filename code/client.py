#!/usr/bin/env python3

import socket, pickle
from card import Card

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

<<<<<<< Updated upstream
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
    


	# Create an instance of ProcessData() to send to server.
	variable = Card()
	# Pickle the object and send it to the server
	data_string = pickle.dumps(variable)
	s.send(data_string)
=======
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
	socket_client.connect((HOST, PORT))
>>>>>>> Stashed changes

	card = Card("hello", 3)
	data_string = pickle.dumps(card)
	socket_client.send(data_string)

	print ('Data Sent to Server')

	data = socket_client.recv(4096)
	fff = pickle.loads(data).get_name()
	print('Received', fff)

	socket_client.close()



