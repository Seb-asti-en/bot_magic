#!/usr/bin/env python3

import socket, pickle
from card import Card

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
    


	# Create an instance of ProcessData() to send to server.
	variable = Card()
	# Pickle the object and send it to the server
	data_string = pickle.dumps(variable)
	s.send(data_string)


	print ('Data Sent to Server')


	data = s.recv(4096)
	fff = pickle.loads(data).get_name()
	print('Received', fff)


	s.close()



