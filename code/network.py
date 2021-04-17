import socket
import pickle


class TCPNetwork:
	def __init__(self, host = 'localhost', port = 5000):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__addr = (host, port)
		
	def connect(self):
		try:
			self.client.connect(self.__addr)
		except:
			pass

	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
		except socket.error as e:
			print(e)

	def recv(self, size = 4096):
		return pickle.loads(self.client.recv(size))


class NetworkUDP:
	def __init__(self, host = 'localhost', port = 5000):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__addr = (host, port)
		
	def connect(self):
		try:
			self.client.connect(self.__addr)
		except:
			pass

	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
		except socket.error as e:
			print(e)

	def recv(self, size = 4096):
		return pickle.loads(self.client.recv(size))
